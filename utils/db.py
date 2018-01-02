import sqlite3   # enable control of an sqlite database
import hashlib   # allows for passwords and emails to be encrypted and decrypted

f = "../data/database.db"

def open_db():
    db = sqlite3.connect(f) # open if f exists, otherwise create
    c = db.cursor()         # facilitate db ops
    return db, c

def close_db(db):
    db.commit()
    db.close()

def create_tables():
    db, c = open_db()
    c.execute("CREATE TABLE Users(user_id integer PRIMARY KEY, password TEXT NOT NULL, admin BOOLEAN, name TEXT, email TEXT)")
    c.execute("CREATE TABLE Items(item_id integer PRIMARY KEY, item_name TEXT NOT NULL, price REAL, description TEXT, status INTEGER, is_selling BOOLEAN, user_id integer)")
    c.execute("CREATE TABLE Pictures(picture_id PRIMARY KEY, item_id integer, path TEXT)")
    close_db(db)

def auth_user(email, password):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE email = '%s' AND password = '%s'" % (hashlib.md5(str(email)).hexdigest(), hashlib.md5(str(password)).hexdigest())
    user = ''
    for user in c.execute(command): # returns either 1 or 0 entries
        pass # sets user to the entry if it exists
    close_db(db)
    if user: # checks if user is an empty string
        return True # 1 result
    return False    # no results

# helper function for incrementing user id
# returns next id number to be used
def increment_id():
    db, c = open_db()
    command = "SELECT * FROM Users"
    id = 0
    for user in c.execute(command):
        id+=1
    close_db(db)
    return id

# default display name is stuy email id
def display_name(email):
    return email.split('@')[0]

# unfinished - needs to check if user is logged in
# allows user to change display name
def change_name(name):
    db, c = open_db()
    pass
    close_db(db)

# Returns the user id if successful, -1 otherwise
def add_user(email, password, name):
    db, c = open_db()

    if get_user(email):
        return -1

    hashed_email = hashlib.md5(str(email)).hexdigest()
    hashed_password = hashlib.md5(str(password)).hexdigest()
    u_id = increment_id()
    # admin status is false by default (stored in SQL as 0)
    command = "INSERT INTO Users VALUES(%d, '%s', 0, '%s', '%s')" % (u_id, hashed_password, name, hashed_email)
    c.execute(command)
    close_db(db)

    return u_id

def add_item():
    pass
    
def change_item():
    pass
    
def add_picture():
    pass

def get_user(email):
    pass

#print add_user('bob1@stuy.edu', '123')
#print increment_id()
