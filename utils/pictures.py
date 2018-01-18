from db_ops import *

def add_picture(item_id, path):
    db, c = open_db()
    p_id = increment_id("Pictures")
    command = "INSERT INTO Pictures VALUES(%d, %d, '%s')" % (p_id, item_id, path)
    c.execute(command)
    close_db(db)

    return p_id

def get_pictures(item_id):
    db, c = open_db()
    command = "SELECT * FROM Pictures WHERE item_id = %d" % (item_id)
    pictures = []
    for p in c.execute(command):
        pictures.append(p)
    close_db(db)

    return pictures

