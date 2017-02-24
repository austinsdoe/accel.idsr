# Setup the application
from flask import Flask
app = Flask(__name__)


from ConfigParser import ConfigParser
from database import Database
from flask import render_template
import os
import os.path

# Configurations
dirname = os.path.dirname(__file__)
cfg = ConfigParser()
cfg.read(os.path.join(dirname, "accel.idsr.ini"))

# Database setup
dbhelper = Database()
db = dbhelper.connect(cfg)

import flask_login
from jsonapi import JSONAPI
from arcreation import ARCREATION
from flask_login import LoginManager

arcreation = ARCREATION()
jsonapi = JSONAPI()

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(username):
    u = db.users.find_one({"_id": username})
    if not u:
        return None

    return User(u['_id'])

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import modules as blueprints
from accelidsr.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

import accelidsr.views
