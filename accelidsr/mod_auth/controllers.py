from accelidsr import utils
from accelidsr import app
from accelidsr import db
from accelidsr.mod_auth.forms import CreateUserForm
from accelidsr.mod_auth.forms import LoginForm
from accelidsr.mod_auth.models import User
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import LoginManager
from flask_login import login_required

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/createuser', methods=['GET', 'POST'])
def createuser():
    form = CreateUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        db.users.insert({
            "username":request.form['username'],
            "password":User.generate_hash(request.form['password']),
            "email":request.form['email']
        })
        return redirect(url_for('auth.login'))
    return render_template('auth/createuser.html', form=form)

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    next = utils.get_redirect_target()
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Login and validate the user.
        username = request.form['username']
        password = request.form['password']
        hashpass = User.generate_hash(password)
        user = db.users.find_one({"username": username})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(str(user['_id']))
            login_user(user_obj)
            flash("Logged in successfully", category='success')

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not utils.is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))

        flash("Invalid Credentials. Please try again.")
    return render_template('auth/login.html', form=form)

@mod_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
