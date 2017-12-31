import sqlite3   # enable control of an sqlite database
import hashlib   # allows for passwords and emails to be encrypted and decrypted

f = "data/database.db"

def open_db():
    db = sqlite3.connect(f) # open if f exists, otherwise create
    c = db.cursor()         # facilitate db ops
    return db, c

def close_db(db):
    db.commit()
    db.close()

def create_tables():
    db, c = open_db()
    c.execute("create table Users(user_id integer PRIMARY KEY, password TEXT NOT NULL, admin BOOLEAN, name TEXT, email TEXT)")
    c.execute("create table Items(item_id integer PRIMARY KEY, item_name TEXT NOT NULL, price REAL, description TEXT, status INTEGER, is_selling BOOLEAN, user_id integer)")
    c.execute("create table Pictures(picture_id PRIMARY KEY, item_id integer, path TEXT)")
    close_db(db)

def auth_user():
    db, c = open_db()
    command = "SELECT * FROM Users where username = '%s' AND password = '%s'" % (username, hashlib.md5(str(password)).hexdigest())
    user = ''
    for user in c.execute(command): # returns either 1 or 0 entries
        pass # sets user to the entry if it exists
    close_db(db)
    if user: # checks if user is an empty string
        return True # 1 result
    return False    # no results
    
def add_user():
    pass
    
def add_item():
    pass
    
def change_item():
    pass
    
def add_picture():
    pass
