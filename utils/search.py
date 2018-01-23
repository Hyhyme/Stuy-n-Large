from db_ops import *
from pictures import get_pictures

def get_items_search(query):
    db, c = open_db()
    command = "SELECT * FROM Items WHERE item_name LIKE '%%%s%%'" % (query)
    d = {}
    for i in c.execute(command):
        d[i[0]] = {}
        d[i[0]]['name'] = i[1]
        d[i[0]]['price'] = i[2]
        d[i[0]]['description'] = i[3]
        d[i[0]]['status'] = i[4]
        d[i[0]]['is_selling'] = True if i[5] == 1 else False
        d[i[0]]['user_id'] = i[6]
        d[i[0]]['images'] = get_pictures(i[0])
    close_db(db)

    return d

def get_items_price(lower, upper):
    db, c = open_db()
    command = "SELECT * FROM Items WHERE price >= %f AND price < %f" % (lower, upper)
    d = {}
    for i in c.execute(command):
        d[i[0]] = {}
        d[i[0]]['name'] = i[1]
        d[i[0]]['price'] = i[2]
        d[i[0]]['description'] = i[3]
        d[i[0]]['status'] = i[4]
        d[i[0]]['is_selling'] = True if i[5] == 1 else False
        d[i[0]]['user_id'] = i[6]
        d[i[0]]['images'] = get_pictures(i[0])
    close_db(db)

    return d

def get_items_is_selling(is_selling):
    db, c = open_db()
    command = "SELECT * FROM Items WHERE is_selling = %d" % (is_selling)
    d = {}
    for i in c.execute(command):
        d[i[0]] = {}
        d[i[0]]['name'] = i[1]
        d[i[0]]['price'] = i[2]
        d[i[0]]['description'] = i[3]
        d[i[0]]['status'] = i[4]
        d[i[0]]['is_selling'] = True if i[5] == 1 else False
        d[i[0]]['user_id'] = i[6]
        d[i[0]]['images'] = get_pictures(i[0])
    close_db(db)

    return d

def get_items_status(status):
    db, c = open_db()
    command = "SELECT * FROM Items WHERE status = %d" % (status)
    d = {}
    for i in c.execute(command):
        d[i[0]] = {}
        d[i[0]]['name'] = i[1]
        d[i[0]]['price'] = i[2]
        d[i[0]]['description'] = i[3]
        d[i[0]]['status'] = i[4]
        d[i[0]]['is_selling'] = True if i[5] == 1 else False
        d[i[0]]['user_id'] = i[6]
        d[i[0]]['images'] = get_pictures(i[0])
    close_db(db)

    return d

def remove_user_items(d, u_id):
    available_items = {}
    for item in d:
        if d[item]['user_id'] != u_id:
            available_items[item] = d[item]
    return available_items
