from wtforms import Form, BooleanField, StringField, PasswordField,TextAreaField, validators
from flask_login import current_user
from blog.models import User

class RegistrationForm(Form):
    username = StringField('Username', [validators.length(min=2, max=20),validators.DataRequired()])
    email = StringField('Email', [validators.length(min=4, max=35 ),validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = StringField('Email', [validators.length(min=4, max=35 ),validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired()])

class BlogForm(Form):
    title = StringField('Title', [validators.length(min=4, max=50),validators.DataRequired()])
    content = TextAreaField('Content', [validators.DataRequired()])
