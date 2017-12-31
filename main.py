from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
