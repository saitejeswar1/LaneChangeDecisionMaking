from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware 
# use to combine each Flask app into a larger one that is dispatched based on prefix
from flask_app_2 import app as flask_app_2
from flask_app_3 import app as flask_app_3

app  = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(flask_app_3,{'/flask_app_2': flask_app_2})

if __name__ == "__main__":
    app.run(debug = True)
    