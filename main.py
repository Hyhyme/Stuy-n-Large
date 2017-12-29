from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return 'hi'
