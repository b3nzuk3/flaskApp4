from blog import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from blog.forms import RegistrationForm, LoginForm, BlogForm
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
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful please try again', 'danger')
    return render_template('login.html', form=form, error=error)

@app.route('/newblog', methods=['GET', 'POST'])
def newblog():
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data, content=form.content.data, user_id='user.id')
        db.session.add(post)
        db.session.commit()
        flash('Blog created', 'success')
        return redirect(url_for('home'))
    return render_template('newblog.html', form=form,)
