#############################################################################
# Copyright (C) 2025 CrowdWare
#
# This file is part of NoCodeService.
#
#  NoCodeService is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  NoCodeService is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NoCodeService.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from flask import Flask, request, jsonify
import stripe
import json
import os
import smtplib
import uuid
from email.mime.text import MIMEText
from Crypto.Cipher import AES
import binascii
import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta
from nocode_keys import NOCODE_DB_PWD
from nocode_keys import NOCODE_DB_USER
from nocode_keys import NOCODE_DATABASE
from nocode_keys import SECRET_KEY
from nocode_keys import GMAIL_PWD
from nocode_keys import NOCODE_PRO_LINK
from nocode_keys import NOCODE_STARTER_LINK
from nocode_keys import WEB_HOOK_SECRET
from nocode_keys import STRIPE_API_KEY
from nocode_keys import GMAIL_ADDRESS
from nocode_keys import BCC_ADDRESS

app = Flask(__name__)
stripe.api_key = STRIPE_API_KEY
app.url_map.strict_slashes = False


def save_account_record(email, publisher, locale, license):
    """Function to save account details in MySQL database"""
    try:
        db_connection = mysql.connector.connect(
            host="artanidos.mysql.pythonanywhere-services.com",
            user=NOCODE_DB_USER,
            password=NOCODE_DB_PWD,
            database=NOCODE_DATABASE
        )
        cursor = db_connection.cursor()

        uuid_value = str(uuid.uuid4())
        # SQL query to insert account record
        sql = """
            INSERT INTO account (uuid, email, publisher, locale, license, date)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (uuid_value, email, publisher, locale, license))
        db_connection.commit()  # Commit the transaction
        print("Account record saved successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db_connection.rollback()  # Rollback in case of error
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()


def generate_license_key(license, publisher):
    # 3 Monate zum aktuellen Datum hinzufügen
    expiration_date = (datetime.now() + relativedelta(months=3)).strftime('%Y-%m-%d')
    license_data = f"{license}|{publisher}|{expiration_date}"
    try:
        iv = os.urandom(12)
        secretKey = SECRET_KEY.encode('utf-8')
        cipher = AES.new(secretKey, AES.MODE_GCM, iv)
        ciphertext, tag = cipher.encrypt_and_digest(license_data.encode('utf-8'))
        encryptedData = iv + ciphertext + tag
        encryptedHex = binascii.hexlify(encryptedData).decode('utf-8')
        return encryptedHex
    except ValueError as error:
        return ""


@app.route('/', methods=['GET'])
def home():
    print("Welcome to stripe")
    return "Welcome to stripe"

@app.route('/checkout', methods=['POST'])
def checkout():
    webhook_secret = WEB_HOOK_SECRET
    request_data = json.loads(request.data)
    print("checkout")
    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        print("signature: " + signature)
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            print("Exception")
            print(e)
            return jsonify({"error": str(e)}), 400
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event.get('type', 'unknown')
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        license = "FREE"
        print('🔔 Payment succeeded!')
        session = event['data']['object']

        # Extrahiere die E-Mail des Kunden
        #subscription = session["subscription"]
        payment_link = session["payment_link"]
        locale = session["locale"]
        if payment_link == NOCODE_PRO_LINK:
            license = "PRO"
        elif payment_link == NOCODE_STARTER_LINK:
            license = "STARTER"
        customer_email = session["customer_details"]["email"]
        customer_name = session["customer_details"]["name"]

        custom_fields = session['custom_fields']
        publisher_value = next(
            (field['text']['value'] for field in custom_fields if field['key'] == 'publisher'),
            None  # Default value if 'publisher' is not found
        )

        try:
            save_account_record(customer_email, publisher_value, locale, license)
            send_license_email(customer_email, locale, generate_license_key(license, publisher_value), license)
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return jsonify({"error": "Stripe error"}), 400
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({"error": "Unexpected error"}), 400

    return jsonify({"status": "success"}), 200


def send_license_email(email, locale, license_key ,license):
    sender = GMAIL_ADDRESS
    recipients = [email]
    bcc = [BCC_ADDRESS]
    if locale == "de":
        msg = MIMEText(f"Vielen Dank für Ihren Kauf!\nIhr Lizenzschlüssel lautet:\n\n{license_key}\n\nBitte kopieren sie diesen Schlüssel und öffnen den FreeBookDesigner -> Settings\nDann fügen sie den Schlüssel bitte in das Feld LicenseKey ein und klicken den Apply Button.")
        msg['Subject'] = "Ihr Lizenzschlüssel für FreeBookDesigner " + license
    else:
        msg = MIMEText(f"Thank you for the purchase!\nYour license key is:\n\n{license_key}\n\nPlease copy this key and open the FreeBookDesigner -> Settings\nThen paste in the license key and press the Apply button.")
        msg['Subject'] = "Your license key for the FreeBookDesigner " + license


    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Bcc'] = ', '.join(bcc)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, GMAIL_PWD)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
