from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from crowdfund import app  as crowdfund_app

app = Flask(__name__)

# Dispatcher für mehrere Flask-Apps
application = DispatcherMiddleware(app, {
    '/crowdfund': crowdfund_app
})

@app.route('/')
def hello_world():
    print("jemand hat hello world geladen")
    return 'Hello from Flask!'