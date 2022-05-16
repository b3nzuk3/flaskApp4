from blog import app
from flask import render_template, url_for, redirect, flash, request
from blog.forms import RegistrationForm


@app.route('/')
@app.route('/home')
def home():
    post = 'Hello World'

    return render_template('home.html', post = post)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Thanks for Registration', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
