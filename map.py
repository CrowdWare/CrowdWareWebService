from flask import Flask, request, send_from_directory, jsonify
from heatmap import add_spot
from flask_cors import CORS
import time

recent_clicks = {}

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    print("Welcome to map")
    return "Welcome to map"


@app.route("/wake", methods=["POST"])
def wake():
    try:
        # IP extrahieren (ggf. über Proxy Header absichern)
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        print(f"Received IP: {ip}")

        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        now = time.time()

        # Nur 1x pro 24h pro IP
        if ip in recent_clicks and now - recent_clicks[ip] < 86400:
            return {"status": "ignored", "message": "Already clicked today"}, 200

        recent_clicks[ip] = now

        # IP → Geolocation (z. B. mit ip-api.com)
        import requests
        r = requests.get(f"http://ip-api.com/json/{ip}")
        geo = r.json()

        lat = geo.get("lat")
        lon = geo.get("lon")

        if lat is None or lon is None:
            return {"error": "Could not locate IP"}, 400

        print(f"Wake via IP: {lat}, {lon}")
        # Punkt setzen hier...
        add_spot(lat, lon)

        return {"status": "ok"}, 200

    except Exception as e:
        return {"error": "Server error", "details": str(e)}, 500

@app.route("/map.png")
def serve_map():
    return send_from_directory("static", "map.png")