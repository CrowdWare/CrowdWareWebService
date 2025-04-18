from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from stripe_checkout import app as stripe_app # Import der ersten Flask-App
from nocode import app  as nocode_app # Import der zweiten Flask-App
from crowdware import app  as crowdware_app
from map import app as map_app

app = Flask(__name__)
CORS(map_app)

# Dispatcher für mehrere Flask-Apps
application = DispatcherMiddleware(app, {
    '/stripe': stripe_app,
    '/nocode': nocode_app,
    '/crowdware': crowdware_app,
    '/map': map_app
})

@app.route('/')
def hello_world():
    print("jemand hat hello world geladen")
    return 'Hello from Flask!'