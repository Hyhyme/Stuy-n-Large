from db_ops import *

def remove_item(i_id):
    db, c = open_db()
    command = "DELETE FROM Items WHERE item_id = %d" % (i_id)
    c.execute(command)
    command = "DELETE FROM Pictures WHERE item_id = %d" % (i_id)
    c.execute(command)
    close_db(db)

def get_all_items():
    db, c = open_db()
    command = "SELECT * FROM Items"
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

def get_item(item_id):
    db, c = open_db()
    command = "SELECT * FROM Items WHERE item_id = %d" % (item_id)
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

def add_item(item_name, price, description, is_selling, user_id):
    db, c = open_db()
    i_id = increment_id("Items")
    command = "INSERT INTO Items VALUES(%d, '%s', %f, '%s', %d, %i, %d)" % (i_id, item_name, price, description, 0, is_selling, user_id)
    c.execute(command)
    close_db(db)

    return i_id

# Modify to take optional parameters
def change_item(item_id, item_name, price, description):
    db, c = open_db()
    command = "UPDATE Items SET item_name = '%s', price = %f, description = '%s' WHERE item_id = %d" % (item_name, price, description, item_id)
    c.execute(command)
    close_db(db)
