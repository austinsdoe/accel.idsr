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
@login_required
def createuser():
    # Only allow the creation of a new user if the current user has admin
    # privileges. Otherwise, redirect to frontpage
    if not current_user.is_admin():
        flash("Not enough privileges", category='info')
        return redirect(url_for('index'))

    # Current user is authenticated or there are no users registered in
    # the database yet, so render the form for user creation.
    if request.method == 'POST':
        form = CreateUserForm(request.form)
        if form.validate():
            import pdb;pdb.set_trace()
            db.users.insert({
                "username": form.username.data,
                "password": User.generate_hash(form.password.data),
                "role": form.role.data,
                "email":  form.email.data})
            msg = "User '{0}' successfully created".format(form.username.data)
            flash(msg, category='info')
            url = url_for('auth.users')
            return redirect(url)

    form = CreateUserForm()
    return render_template('auth/createuser.html', form=form)

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    # If no users are available in the database yet, create a new admin/admin
    # user by default
    firstaccess = ''
    if db.users.find().count() == 0:
        db.users.insert({
            'username': 'admin',
            'password': User.generate_hash('admin'),
            'email': 'admin@example.com',
            'role': 'admin',
        })
        firstaccess = 'Congrats! This is the first time you load the ' \
                      'application. Use admin/admin to access with super ' \
                      'privileges.'

    next = utils.get_redirect_target()
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Login and validate the user.
        username = request.form['username']
        password = request.form['password']
        hashpass = User.generate_hash(password)
        user = db.users.find_one({"username": username})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(id=str(user['_id']),
                            username=user['username'],
                            role=user['role'])
            login_user(user_obj)
            flash("Logged in successfully", category='info')

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not utils.is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))

        flash("Invalid Credentials. Please try again.", category='error')
    return render_template('auth/login.html', form=form,
                           firstaccess=firstaccess)


@mod_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@mod_auth.route('/users')
@login_required
def users():
    # Only allow the creation of a new user if the current user has admin
    # privileges. Otherwise, redirect to frontpage
    if not current_user.is_admin():
        flash("Not enough privileges", category='info')
        return redirect(url_for('index'))
    users = db.users.find()
    urltemplate = 'auth/users.html'
    return render_template(urltemplate, users=users)
