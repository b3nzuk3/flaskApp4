from blog import app
from flask import render_template, url_for


@app.route('/')
@app.route('/home')
def home():
    post = 'Hello World'

    return render_template('home.html', post = post)
