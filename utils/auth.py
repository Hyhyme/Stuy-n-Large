from flask import session
import db

def logged_in():
    return 'u_id' in session

def add_user(email, password, name):
    u_id = db.add_user(email, password, name)
    if u_id != -1:
        login(email, password)
        return True
    return False

def login(email, password):
    if db.auth_user(email, password):
        session['u_id'] = db.get_user_id(email)
        return True
    return False
