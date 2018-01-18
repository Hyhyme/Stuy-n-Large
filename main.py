from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug import secure_filename
import time
import json

from utils import auth, db
from utils.auth import logged_in

import os

app = Flask(__name__)
app.secret_key = 'testing secret key' #os.urandom(32)

app.jinja_env.globals.update(logged_in = logged_in)
app.jinja_env.globals.update(username = db.get_username)

def format_currency(value):
    return "${:,.2f}".format(value)

app.jinja_env.filters['currency'] = format_currency

UPLOAD_FOLDER = 'static/data/img'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    if logged_in():
        return redirect('market')
    return render_template('index.html')

@app.route('/market')
def market():
    items = None
    if request.args.get('query'):
        items = db.get_items_search(request.args.get('query'))
    else:
        items = db.get_items()
    return render_template('index_logged_in.html', items = items)

@app.route('/profile')
def profile():
    if not logged_in():
        flash('You are not logged in.')
        return redirect('index')
    user = session['u_id']
    ## make a dict where all Uitems = items where items['u_id'] == session['u_id']
    items = db.get_items()
    Uitems = {}
    x=0
    for i in items:
        if items[i]['user_id'] == user:
            Uitems[x] = items[i]
            x+=1
    return render_template("profile.html", items = Uitems)

@app.route('/item')
def item():
    return render_template("item_page.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not logged_in():
        flash('You are not logged in.')
        return redirect('index')
    if request.method == 'POST':

        is_selling = True if request.form.get('type') == 'sell' else False

        item = request.form.get('item')
        price = request.form.get('price')
        description = request.form.get('description')

        if not item or not price or not description:
            flash('You must fill out all fields.')
            return redirect('upload')

        price = float(price)

        if price < 0:
            flash('Price must be greater than $0.')
            return redirect('upload')

        if price > 9999.99:
            flash('Price must be less than $10,000.')
            return redirect('upload')

        i_id = db.add_item(item, price, description, is_selling, int(session['u_id']))

        # handle uploaded images
        f = request.files.getlist('pictures[]')

        if not f:
            flash('You must upload a picture.')
            return redirect('upload')

        for pic in f:
            if not allowed_file(pic.filename):
                flash('Pictures must be in .jpg or .jpeg format.')
                return redirect('upload')

        i = 0
        for pic in f:
            timestamp = str(time.time()).replace(".", "_")
            filename = str(session['u_id']) + '_' + timestamp + '_' + str(i) + '.jpg'

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pic.save(path)
            db.add_picture(i_id, path.strip('static/'))
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
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        name = fname + ' ' + lname
        terms = request.form.get('terms')

        if (password1 == '' or password2 == '' or fname == '' or lname == '' or email == ''):

            flash('Please fill in all fields')
            return redirect('create')

        if not password1 == password2:
            flash('Passwords do not match.')
            return redirect('create')


        if not email.endswith('@stuy.edu'):
            flash('Email is invalid.')
            return redirect('create')

        if not terms:
            flash('Please read and accept the terms of service')
            return redirect('create')

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

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    return request.form.get("email")


# API routes
FILTERS = {
    'selling': db.get_items_is_selling(True),
    'looking_for': db.get_items_is_selling(False),
    'under_5': db.get_items_price(0, 4.99),
    '5_10': db.get_items_price(5, 9.99),
    '10_15': db.get_items_price(10, 14.99),
    'over_15': db.get_items_price(15, 9999.99),
    'book': db.get_items_search('book')
}

@app.route('/api/get_items_filters')
def get_items_filters():
    items = {}
    filters = request.args.get('filters').split(',')
    if filters == ['']:
        return json.dumps(db.get_items())
    for f in filters:
        for item in FILTERS[f]:
            items[item] = FILTERS[f][item]
    return json.dumps(items)

@app.route('/api/get_items')
def get_items():
    return json.dumps(db.get_items())

@app.route('/api/get_item_template')
def get_item_template():
    i_id = request.args.get('i_id')
    items = db.get_item(int(i_id))
    return render_template('item.html', items = items, item = items.keys()[0])

@app.route('/api/get_item_modal')
def get_item_modal():
    i_id = request.args.get('i_id')
    item = db.get_item(int(i_id))
    return render_template('item_modal.html', item = item)

if __name__ == '__main__':
    app.debug = True
    app.run()
