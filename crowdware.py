# Copyright (C) 2025 CrowdWare
#
# This file is part of CrowdWareService.
#
#  CrowdWareService is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  CrowdWareService is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with CrowdWareService.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
import smtplib
import uuid
import bcrypt
import hashlib
from email.mime.text import MIMEText
import mysql.connector
from crowdware_keys import CROWDWARE_DB_PWD
from crowdware_keys import CROWDWARE_DB_USER
from crowdware_keys import CROWDWARE_DATABASE

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    print("Welcome to crowdware")
    return "Welcome to crowdware"

def get_db_connection():
    return mysql.connector.connect(
        host="artanidos.mysql.pythonanywhere-services.com",
        user=CROWDWARE_DB_USER,
        password=CROWDWARE_DB_PWD,
        database=CROWDWARE_DATABASE
    )

@app.route('/items', methods=['GET'])
def get_items():
    item_type = request.args.get('type')
    if not item_type:
        return jsonify({'error': 'Missing required parameter: type'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT item.uuid, item.type, item.name, item.description, item.locale,
                   item.date, item.url, account.publisher
            FROM item
            JOIN account ON item.account = account.uuid
            WHERE item.type = %s
        """
        cursor.execute(query, (item_type,))
        items = cursor.fetchall()

        cursor.close()
        conn.close()

        for item in items:
            if item['date']:
                item['date'] = item['date'].isoformat()
        return jsonify(items)

    except Exception as e:
        return jsonify({'error': str(e)}), 500