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

from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
import smtplib
import uuid
import bcrypt
import hashlib
from email.mime.text import MIMEText
from datetime import datetime
import mysql.connector
from crowdware_keys import CROWDWARE_DB_PWD
from crowdware_keys import CROWDWARE_DB_USER
from crowdware_keys import CROWDWARE_DATABASE

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    print("Welcome to NoCode")
    return "Welcome to NoCode"

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
    filter_param = request.args.get('filter')
    item_locale = request.args.get('locale')
    uuid_list = request.args.getlist('uuid')
    exclude_list_raw = request.args.getlist('exclude')

    if not item_type:
        return jsonify({'error': 'Missing required parameter: type'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT item.uuid, item.type, item.name, item.description, item.locale,
                   item.date, item.url, item.pictureurl, account.publisher
            FROM item
            JOIN account ON item.account = account.uuid
            WHERE item.type = %s AND item.locale = %s
        """
        params = [item_type, item_locale]

        # ✅ Nur bestimmte UUIDs laden
        if uuid_list:
            placeholders = ','.join(['%s'] * len(uuid_list))
            query += f" AND item.uuid IN ({placeholders})"
            params.extend(uuid_list)

        # ✅ Bestimmte UUIDs ausschließen (z. B. via notInList)
        excluded_uuids = []
        for e in exclude_list_raw:
            if e.startswith("uuid:"):
                excluded_uuids.append(e.split(":", 1)[1])

        if excluded_uuids:
            placeholders = ','.join(['%s'] * len(excluded_uuids))
            query += f" AND item.uuid NOT IN ({placeholders})"
            params.extend(excluded_uuids)

        # ✅ Optionaler Zusatzfilter
        if filter_param == "new":
            query += " ORDER BY item.date DESC LIMIT 3"

        cursor.execute(query, tuple(params))
        items = cursor.fetchall()

        cursor.close()
        conn.close()

        # Formatierung der Datum-Felder
        for item in items:
            if item['date']:
                item['date'] = item['date'].isoformat()

        return jsonify(items)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/items', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON body'}), 400

        required_fields = ['type', 'name', 'description', 'locale', 'url', 'pictureurl', 'account']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        new_uuid = str(uuid.uuid4())
        date_now = datetime.utcnow()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO item (uuid, type, name, description, locale, date, url, pictureurl, account)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            new_uuid,
            data['type'],
            data['name'],
            data['description'],
            data['locale'],
            date_now,
            data['url'],
            data['pictureurl'],
            data['account']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'uuid': new_uuid})

    except Exception as e:
        return jsonify({'error': str(e)}), 500