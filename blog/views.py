import os
import secrets
from PIL import Image
from blog import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from blog.forms import RegistrationForm, LoginForm, BlogForm, UpdateAccountForm, CommentForm
from blog.models import User, Post, Comments
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template('home.html',title="Home", posts = posts)

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

    return render_template('register.html',title="Registration", form=form)

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
    return render_template('login.html', form=form,title="Login", error=error)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/newblog', methods=['GET', 'POST'])
@login_required
def newblog():
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Blog created', 'success')
        return redirect(url_for('home'))
    return render_template('newblog.html', form=form,title="blog")

@app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def blog(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comments.query.order_by(Comments.date_posted.desc()).filter_by(post_id=post_id)
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
      if form.upvote.data:
        recent = post.likes
        new = recent + 1
        post.likes = new
        db.session.commit()

      if form.downvote.data:
        recent = post.dislikes
        new = recent + 1
        post.dislikes = new
        db.session.commit()

      comment = Comments(content=form.content.data, user_comments= current_user, post_id=post_id)
      db.session.add(comment)
      db.session.commit()
      flash('You have commented', 'success')
      return redirect(url_for('blog', post_id=post_id))
    return render_template('blog.html', post=post, form=form, comments=comments)





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account',image_file=image_file, form=form)

@app.route("/about")
def about():

    return render_template('about.html',title="about")

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Pitch has been updated!', 'success')
        return redirect(url_for('blog', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newblog.html', legend ='Update pitch', form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('home'))
