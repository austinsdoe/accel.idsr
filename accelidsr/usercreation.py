from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length


class CreateUserForm(Form):

    username = StringField('username', validators=[DataRequired(), Length(min=6,max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=20)])
    email = StringField("Email", validators=[DataRequired("Please enter your email address."), Email()])
    role = SelectField('User Role', choices=["clerk", "admin", "superuser"])
    submit = SubmitField("Submit")

