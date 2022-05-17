from blog import app
from flask import render_template, url_for, redirect, flash, request
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post

@app.route('/')
@app.route('/home')
def home():
    post = 'Hello World'

    return render_template('home.html', post = post)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username, email=form.email, password=form.password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        if request.form['email'] != 'admin@blog.com' or request.form['password'] != 'secret':
            error = 'Invalid Credentials'
        else:
            flash('You have logged in successfully', 'success')
            return redirect(url_for('home'))

    return render_template('login.html', form=form, error=error)
