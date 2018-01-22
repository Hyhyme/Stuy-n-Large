from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug import secure_filename
import time
import json

from utils import auth, db, gmail
from utils.auth import logged_in, is_admin

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from oauth2client.client import AccessTokenCredentials
from googleapiclient import http

import os

app = Flask(__name__)
app.secret_key = 'testing secret key' #os.urandom(32)

app.jinja_env.globals.update(logged_in = logged_in)
app.jinja_env.globals.update(is_admin = is_admin)
app.jinja_env.globals.update(username = db.get_username)

def format_currency(value):
    return "${:,.2f}".format(value)

def format_boolean(value):
    return False if value == 0 or value == "0" or not value else True

def format_status(value):
    if value == 0:
        return 'Pending'
    elif value == 1:
        return 'Meeting arranged'
    elif value == 2:
        return 'Completed'
    return ''

app.jinja_env.filters['currency'] = format_currency
app.jinja_env.filters['boolean'] = format_boolean
app.jinja_env.filters['status'] = format_status

UPLOAD_FOLDER = 'static/data/img'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    if logged_in():
        return redirect(url_for('market'))
    return render_template('index.html')

@app.route('/market')
def market():
    items = None
    if request.args.get('query'):
        items = db.get_items_search(request.args.get('query'))
    else:
        items = db.get_all_items()
    return render_template('index_logged_in.html', items = items)

@app.route('/profile')
def profile():
    if not logged_in():
        flash('You are not logged in.')
        return redirect(url_for('index'))
    user = session['u_id']
    ## make a dict where all Uitems = items where items['u_id'] == session['u_id']
    items = db.get_all_items()
    Uitems = {}
    for i in items:
        if items[i]['user_id'] == user:
            Uitems[i] = items[i]
    return render_template("profile.html", items = Uitems, user=user )

@app.route('/item')
def item():
    return render_template("item_page.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not logged_in():
        flash('You are not logged in.')
        return redirect(url_for('index'))
    if request.method == 'POST':

        is_selling = True if request.form.get('type') == 'sell' else False

        item = request.form.get('item')
        price = request.form.get('price')
        description = request.form.get('description')

        if not item or not price or not description:
            flash('You must fill out all fields.')
            return redirect(url_for('upload'))

        price = float(price)

        if price < 0:
            flash('Price must be greater than $0.')
            return redirect(url_for('upload'))

        if price > 9999.99:
            flash('Price must be less than $10,000.')
            return redirect(url_for('upload'))

        i_id = db.add_item(item, price, description, is_selling, int(session['u_id']))

        # handle uploaded images
        f = request.files.getlist('pictures[]')

        if not f:
            flash('You must upload a picture.')
            return redirect(url_for('upload'))

        for pic in f:
            if not allowed_file(pic.filename):
                flash('Pictures must be in .jpg or .jpeg format.')
                return redirect(url_for('upload'))

        i = 0
        for pic in f:
            timestamp = str(time.time()).replace(".", "_")
            filename = str(session['u_id']) + '_' + timestamp + '_' + str(i) + '.jpg'

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pic.save(path)
            db.add_picture(i_id, path.strip('static/'))
            i += 1

        return redirect(url_for('profile'))
    return render_template('upload.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if logged_in():
        flash('You are already logged in!')
        return redirect(url_for('index'))

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
            return redirect(url_for('create'))

        if not password1 == password2:
            flash('Passwords do not match.')
            return redirect(url_for('create'))


        if not email.endswith('@stuy.edu'):
            flash('Email is invalid.')
            return redirect(url_for('create'))

        if not terms:
            flash('Please read and accept the terms of service')
            return redirect(url_for('create'))

        if not auth.add_user(email, password1, name):
            flash('Email already in use.')
            return redirect(url_for('login'))

        flash('Welcome ' + fname + '!')
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/delete', methods = ['GET','POST'])
def delete():
    if not logged_in():
        flash('You are not logged in.')
        return redirect('index')
    if request.method == 'GET':
        db.delete_item(request.args.get('itemid'))
    return redirect('index')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        flash('You are already logged in!')
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        if auth.login(email, request.form.get('password')):
            flash('Welcome back, ' + db.get_user_name(email) + '!')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if logged_in():
        flash('You have been logged out.')
        auth.logout()
    else:
        flash('You are not logged in!')
    return redirect(url_for('index'))

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    seller_email = None
    email_body = None

    if request.method == 'POST':
        seller_email = db.get_user_email(int(request.args.get('u_id')))
        email_body = request.form.get('email')
    else:
        seller_email = session['seller_email']
        email_body = session['email_body']

    if 'credentials' not in session:
        session['seller_email'] = seller_email
        session['email_body'] = email_body
        return redirect(url_for('authorize'))

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials']
    )

    service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)
    message = gmail.create_message("me", seller_email, "Item Inquiry", email_body)
    gmail.send_message(service, "me", message)

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = gmail.credentials_to_dict(credentials)

    flash('Email sent!')
    return redirect(url_for('index'))

@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        gmail.CLIENT_SECRETS_FILE, scopes=gmail.SCOPES
    )

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true'
    )

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        gmail.CLIENT_SECRETS_FILE, scopes=gmail.SCOPES, state=state
    )
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = gmail.credentials_to_dict(credentials)

    return redirect(url_for('send_email'))

@app.route('/admin')
def admin():
    if is_admin():
        users = db.get_users()
        items = db.get_all_items()
        pictures = db.get_all_pictures()
        return render_template('admin.html', users = users, items = items, pictures = pictures)
    else:
        flash('You must be an admin to view this page.')
        return redirect(url_for('index'))


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
        return json.dumps(db.get_all_items())
    for f in filters:
        for item in FILTERS[f]:
            items[item] = FILTERS[f][item]
    return json.dumps(items)

@app.route('/api/get_items')
def get_items():
    return json.dumps(db.get_all_items())

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


# Non-view routes
@app.route('/admin/remove_user')
def remove_user():
    if is_admin():
        u_id = request.args.get('u_id')
        db.remove_user(int(u_id))
        flash('User removed.')
    else:
        flash('You must be an admin to perform this action.')
    return redirect(url_for('admin'))

@app.route('/admin/remove_item')
def remove_item():
    if is_admin():
        i_id = request.args.get('i_id')
        db.remove_item(int(i_id))
        flash('Item removed.')
    else:
        flash('You must be an admin to perform this action.')
    return redirect(url_for('admin'))

@app.route('/admin/remove_picture')
def remove_picture():
    if is_admin():
        p_id = request.args.get('p_id')
        db.remove_picture(int(p_id))
        flash('Picture removed.')
    else:
        flash('You must be an admin to perform this action.')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.debug = True
    app.run()
