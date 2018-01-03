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
    c.execute("CREATE TABLE Users(user_id integer PRIMARY KEY, password TEXT NOT NULL, admin BOOLEAN, name TEXT, email TEXT)")
    c.execute("CREATE TABLE Items(item_id integer PRIMARY KEY, item_name TEXT NOT NULL, price REAL, description TEXT, status INTEGER, is_selling BOOLEAN, user_id integer)")
    c.execute("CREATE TABLE Pictures(picture_id PRIMARY KEY, item_id integer, path TEXT)")
    close_db(db)

def auth_user(email, password):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE email = '%s' AND password = '%s'" % (hashed(email), hashed(password))
    user = None
    for u in c.execute(command): # returns either 1 or 0 entries
        user = u # sets user to the entry if it exists
    close_db(db)
    if user: # non-empty strings are considered true, None is considered to be false
        return True # 1 result
    return False    # no results

# helper function for incrementing id numbers
# returns next id number to be used
def increment_id(table):
    db, c = open_db()
    command = "SELECT * FROM %s" % (table)
    id = 0
    for user in c.execute(command):
        id+=1
    close_db(db)
    return id

# default display name is stuy email id
def display_name(email):
    return email.split('@')[0]

# allows user to change display name
def change_name(u_id, new_name):
    db, c = open_db()
    command = "UPDATE Users SET name = '%s' WHERE user_id = %d" % (new_name, u_id)
    c.execute(command)
    close_db(db)

# Returns the user id if successful, -1 otherwise
def add_user(email, password, name):
    db, c = open_db()

    if get_user_id(email):
        return -1

    u_id = increment_id("Users")
    # admin status is false by default (stored in SQL as 0)
    command = "INSERT INTO Users VALUES(%d, '%s', 0, '%s', '%s')" % (u_id, hashed(password), name, hashed(email))
    c.execute(command)
    close_db(db)

    return u_id

def add_item(item_id, item_name, price, description, status, user_id):
    db, c = open_db()
    command = "INSERT INTO Items VALUES(%d, '%s', %d, '%s', %d, %d, %d)" % (increment_id("Items"), item_name, price, description, status, user_id)
    c.execute(command)
    close_db(db)
    
def change_item(item_id, item_name, price, description):
    db, c = open_db()
    command = "UPDATE Items SET item_name = '%s', price = %d, description = '%s' WHERE item_id = %d" % (item_name, price, description, item_id)
    c.execute(command)
    close_db(db)
    
# tentative
def add_picture(item_id, path):
    db, c = open_db()
    command = "INSERT INTO Pictures VALUES(%d, %d, '%s')" % (increment_id("Pictures"), item_id, path)
    close_db(db)

def get_user_id(email):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE email = '%s'" % (hashed(email))
    user = None
    for u in c.execute(command):
        user = u
    close_db(db)
    return user[0]

def get_user_name(email):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE email = '%s'" % (hashed(email))
    user = None
    for u in c.execute(command):
        user = u
    close_db(db)
    return user[3]

def hashed(foo):
    return hashlib.md5(str(foo)).hexdigest()

if __name__ == '__main__':
    create_tables()
