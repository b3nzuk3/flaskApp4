from wtforms import Form, BooleanField, StringField, PasswordField,TextAreaField,SubmitField, validators
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Email
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

class UpdateAccountForm(Form):
    username = StringField('Username',[validators.DataRequired(), validators.length(min=2, max=20)])
    email = StringField('Email',[validators.DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')




class BlogForm(Form):
    title = StringField('Title', [validators.length(min=4, max=50),validators.DataRequired()])
    content = TextAreaField('Content', [validators.DataRequired()])

class CommentForm(Form):
    content = StringField('Add a comment',[validators.DataRequired()])
    upvote = BooleanField('Upvote')
    downvote = BooleanField('Downvote')
    submit = SubmitField('Comment')
