from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length


class CreateUserForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=4, max=20)])

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4, max=20)])

    email = StringField(
        "Email",
        validators=[DataRequired("Please enter your email address."),
                    Email()])

    role = SelectField(
        'Role',
        choices=[('admin', 'Administrator'), ('user', 'User')],
        validators=[DataRequired(), ], )

    submit = SubmitField("Submit")


class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4)])

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4)])

    submit = SubmitField("Submit")
