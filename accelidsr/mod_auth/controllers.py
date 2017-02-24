from accelidsr import app
from accelidsr.mod_auth.forms import CreateUserForm
from accelidsr.mod_auth.models import User
from flask_login import current_user
from flask_login import login_user
from flask_login import LoginManager
from flask_login import login_equired

import flask_login

@mod_auth.route('/createuser', methods=['GET', 'POST'])
def createuser():
    user_to_create = User
    form = CreateUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db_connect = mongo.get_db()
            db_connect.users.insert({
                "_id":request['username'],
                "password":user_to_create.generate_hash(request['password']),
                "email":request['email'],
                "role":request['role']
            })

    return render_template('auth/createuser.html', form=form)

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # POST request. Check user credentials
        data_connect = mongo.get_db()
        username = request.form['username']
        login_request = data_connect.users.find_one({"_id": username})
        if login_request:
            user = User(login_request['_id'])
            login_user(user)
            error = 'Logged in Successfully'
            flash("Credentials are correct", category='success')

            # Redirect to the main page, which will be in charge of rendering
            # the default main page when a user is logged. Otherwise, it will
            # redirect again to the login page
            redirect('/')
        else:
            error = 'Invalid Credentials. Please try again.'
            flash("Wrong username or password", category='error')
            render_template('index.html', error = error)

@mod_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
