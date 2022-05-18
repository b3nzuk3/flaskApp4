from blog import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from blog.forms import RegistrationForm, LoginForm, BlogForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    post = 'Hello World'

    return render_template('home.html', post = post)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful please try again', 'danger')
    return render_template('login.html', form=form, error=error)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/newblog', methods=['GET', 'POST'])
@login_required
def newblog():
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data, content=form.content.data, user_id='user.id')
        db.session.add(post)
        db.session.commit()
        flash('Blog created', 'success')
        return redirect(url_for('home'))
    return render_template('newblog.html', form=form,)

@app.route("/account")
def account():

    return render_template('account.html')
