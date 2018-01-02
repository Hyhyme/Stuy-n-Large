from flask import session
import db

def logged_in():
    return 'u_id' in session

# Username is email
def add_user(username, password):
    u_id = db.add_user(username, password)
    if u_id != -1:
        login(username, password)
        return True
    return False

def login(username, password):
    if db.auth_user(username, password):
        session['u_id'] = u_id
        return True
    return False
