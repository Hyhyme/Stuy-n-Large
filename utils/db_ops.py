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

def hashed(foo):
    return hashlib.md5(str(foo)).hexdigest()
