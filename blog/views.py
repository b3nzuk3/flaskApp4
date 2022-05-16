from blog import app
from flask import render_template, url_for, request
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
        flash('Thanks for Registration')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
