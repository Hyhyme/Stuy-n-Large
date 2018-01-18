from db_ops import *
from users import *
from items import *
from pictures import *

def create_tables():
    db, c = open_db()
    c.execute("CREATE TABLE Users(user_id integer PRIMARY KEY, password TEXT NOT NULL, admin BOOLEAN, name TEXT, email TEXT)")
    c.execute("CREATE TABLE Items(item_id integer PRIMARY KEY, item_name TEXT NOT NULL, price REAL, description TEXT, status INTEGER, is_selling BOOLEAN, user_id integer)")
    c.execute("CREATE TABLE Pictures(picture_id PRIMARY KEY, item_id integer, path TEXT)")
    close_db(db)

if __name__ == '__main__':
    create_tables()
