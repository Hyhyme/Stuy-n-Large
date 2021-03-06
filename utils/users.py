from db_ops import *
from items import remove_item

def remove_user(u_id):
    db, c = open_db()
    command = "DELETE FROM Users WHERE user_id = %d" % (u_id)
    c.execute(command)
    command = "SELECT * FROM Items WHERE user_id = %d" % (u_id)
    for i in c.execute(command):
        com = "DELETE FROM Items WHERE item_id = %d" % (i[0])
        c.execute(com)
        com = "DELETE FROM Pictures WHERE item_id = %d" % (i[0])
        c.execute(com)
    close_db(db)

def auth_user(email, password):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE email = '%s' AND password = '%s'" % (email, hashed(password))
    user = None
    for u in c.execute(command): # returns either 1 or 0 entries
        user = u # sets user to the entry if it exists
    close_db(db)
    if user: # non-empty strings are considered true, None is considered to be false
        return True # 1 result
    return False    # no results


# default display name is stuy email id
def display_name(email):
    return email.split('@')[0]

# allows user to change display name
def change_name(u_id, new_name):
    db, c = open_db()
    command = "UPDATE Users SET name = '%s' WHERE user_id = %d" % (new_name, u_id)
    c.execute(command)
    close_db(db)

# allows user to change display name
def change_pass(u_id, new_pass):
    db, c = open_db()
    command = "UPDATE Users SET password = '%s' WHERE user_id = %d" % (hashed(new_pass), u_id)
    c.execute(command)
    close_db(db)

# Returns the user id if successful, -1 otherwise
def add_user(email, password, name):
    db, c = open_db()

    if get_user_id(email):
        return -1

    u_id = increment_id("Users")
    # admin status is false by default (stored in SQL as 0)
    command = "INSERT INTO Users VALUES(%d, '%s', 0, '%s', '%s')" % (u_id, hashed(password), name, email)
    c.execute(command)
    close_db(db)

    return u_id

def get_users():
    db, c = open_db()
    command = "SELECT * FROM Users"
    d = {}
    for i in c.execute(command):
        d[i[0]] = {}
        d[i[0]]['admin'] = i[2]
        d[i[0]]['name'] = i[3]
        d[i[0]]['email'] = i[4]
    close_db(db)

    return d

def get_username(u_id):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE user_id = %d" % (u_id)
    user = None
    for u in c.execute(command):
        user = u
    close_db(db)
    return user[3]

def get_user_id(email):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE email = '%s'" % (email)
    user = None
    for u in c.execute(command):
        user = u
    close_db(db)
    if user:
        return user[0]
    return user
    
def get_user_name(email):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE email = '%s'" % (email)
    user = None
    for u in c.execute(command):
        user = u
    close_db(db)
    return user[3]

def get_user_admin(u_id):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE user_id = %d" % (u_id)
    user = None
    for u in c.execute(command):
        user = u
    close_db(db)
    return user[2]

def get_user_email(u_id):
    db, c = open_db()
    command = "SELECT * FROM Users WHERE user_id = %d" % (u_id)
    user = None
    for u in c.execute(command):
        user = u
    close_db(db)
    return user[4]

def set_user_admin(u_id, admin):
    db, c = open_db()
    admin = 1 if admin else 0
    command = "UPDATE Users SET admin = %d WHERE user_id = %d" % (admin, u_id)
    c.execute(command)
    close_db(db)
