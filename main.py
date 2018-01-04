from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug import secure_filename
import time

from utils import auth, db
from utils.auth import logged_in

import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.jinja_env.globals.update(logged_in = logged_in)
app.jinja_env.globals.update(username = db.get_username)

def format_currency(value):
    return "${:,}".format(value)

app.jinja_env.filters['currency'] = format_currency

UPLOAD_FOLDER = 'data/img'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    session['u_id'] = 'test'
    if logged_in():
        items = {
            0: {'name': 'banana', 'price': 2, 'description': 'Brand new!', 'status': 0, 'is_selling': True, 'user_id': 0},
            1: {'name': 'Physics Textbook', 'price': 1200, 'description': 'Get a head start on your AP Physics C class with this amazing textbook!', 'status': 0, 'is_selling': True, 'user_id': 0},
            2: {'name': 'banana', 'price': 2, 'description': 'Brand new!', 'status': 0, 'is_selling': True, 'user_id': 0},
            3: {'name': 'banana', 'price': 2, 'description': 'Brand new!', 'status': 0, 'is_selling': True, 'user_id': 0},
            4: {'name': 'Physics Textbook', 'price': 1200, 'description': 'Get a head start on your AP Physics C class with this amazing textbook!', 'status': 0, 'is_selling': True, 'user_id': 0},
            5: {'name': 'banana', 'price': 2, 'description': 'Brand new!', 'status': 0, 'is_selling': True, 'user_id': 0}
        }
        return render_template('index_logged_in.html', items = items)
    return render_template('index.html')

@app.route('/filter')
def filter():
    return 'hi'

@app.route('/profile')
def profile():
    return 'hi'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    session['u_id'] = 0
    if not logged_in():
        flash('You are not logged in.')
        return redirect('index')
    if request.method == 'POST':
        f = request.files.getlist('pictures[]')

        for pic in f:
            if not allowed_file(pic.filename):
                flash('Pictures must be in .jpg or .jpeg format.')
                return redirect('upload')

        i = 0
        for pic in f:
            timestamp = str(time.time()).replace(".", "_")
            filename = str(session['u_id']) + '_' + timestamp + '_' + str(i) + '.jpg'
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            i += 1

        return redirect('profile')
    return render_template('upload.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if logged_in():
        flash('You are already logged in!')
        return redirect('index')
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not password1 == password2:
            flash('Passwords do not match.')
            return redirect('create')

        email = request.form.get('email')
        if not email.endswith('@stuy.edu'):
            flash('Email is invalid.')
            return redirect('create')

        fname = request.form.get('fname')
        name = fname + ' ' + request.form.get('lname')

        if not auth.add_user(email, password1, name):
            flash('Email already in use.')
            return redirect('login')

        flash('Welcome ' + fname + '!')
        return redirect('index')

    return render_template('create.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        flash('You are already logged in!')
        return redirect('index')
    if request.method == 'POST':
        email = request.form.get('email')
        if auth.login(email, request.form.get('password')):
            flash('Welcome back, ' + db.get_user_name(email) + '!')
            return redirect('index')
        else:
            flash('Invalid credentials, please try again.')
            return redirect('login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if logged_in():
        flash('You have been logged out.')
        auth.logout()
    else:
        flash('You are not logged in!')
    return redirect('index')


if __name__ == '__main__':
    app.debug = True
    app.run()
