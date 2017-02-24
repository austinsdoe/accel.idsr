
from flask import Flask
app = Flask(__name__)

import flask_login
import os
from jsonapi import JSONAPI
from arcreation import ARCREATION
from databaseconnect import DBCONNECT
from flask_login import LoginManager

app.secret_key = os.urandom(24)

arcreation = ARCREATION()
jsonapi = JSONAPI()
mongo = DBCONNECT()

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(username):
    data_connect = mongo.get_db()
    u = data_connect.users.find_one({"_id": username})
    if not u:
        return None

    return User(u['_id'])

import accelidsr.views
