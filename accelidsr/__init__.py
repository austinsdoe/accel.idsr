# Setup the application
from flask import Flask
app = Flask(__name__)


from bson import ObjectId
from ConfigParser import ConfigParser
from database import Database
from flask import render_template
import os
import os.path

# Flask-WTF CSRF infrastructure requires a csfr token
app.secret_key = os.urandom(24)

# Configurations
dirname = os.path.dirname(__file__)
cfg = ConfigParser()
cfg.read(os.path.join(dirname, "accel.idsr.ini"))

# Database setup
mongo = Database()
db = mongo.connect(cfg)

import flask_login
from jsonapi import JSONAPI
from flask_login import LoginManager

# Import modules as blueprints
from accelidsr.mod_auth.models import User
from accelidsr.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

lm = LoginManager()
lm.init_app(app)
# Fall-back page if the user is not logged in and the request view has the
# login_required decorator
lm.login_view = "auth.login"

@lm.user_loader
def load_user(user_id):
    """ Used by LoginManager (session manager by Flask) to reload the user
        object from the user ID stored in the session.
        It should take the unicode ID of a user, and return the corresponding
        user object.
        It should return None (not raise an exception) if the ID is not valid.
        (In that case, the ID will manually be removed from the session and
        processing will continue.)
        :param: user_id the id of the user to be loaded
        :return: the User for the specificed id or None if no user found.
    """
    u = db.users.find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    return User(user_id)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


import accelidsr.views
