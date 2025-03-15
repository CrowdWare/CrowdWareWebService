from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from stripe_checkout import app as stripe_app # Import der ersten Flask-App
from nocode import app  as nocode_app # Import der zweiten Flask-App
from crowdware import app  as crowdware_app
app = Flask(__name__)

# Dispatcher für mehrere Flask-Apps
application = DispatcherMiddleware(app, {
    '/stripe': stripe_app,
    '/nocode': nocode_app,
    '/crowdware': crowdware_app
})

@app.route('/')
def hello_world():
    print("jemand hat hello world geladen")
    return 'Hello from Flask!'