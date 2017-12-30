from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.debug = True
    app.run()