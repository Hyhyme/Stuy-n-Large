from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import auth, db
from utils.auth import logged_in

import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.jinja_env.globals.update(logged_in = logged_in)

def format_currency(value):
    return "${:,}".format(value)

app.jinja_env.filters['currency'] = format_currency


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
