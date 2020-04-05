import sqlite3

class image_database (object):
    def __init__ (self, db_name):
        self.conn = sqlite3.connect (db_name)
        self.db_name = db_name
        self.cursor = self.conn.cursor ()

        self.cursor.execute ("""CREATE TABLE IF NOT EXISTS images (id integer, image_path, master_name text)""")

    def get_name (self):
        return self.name

    def set_images (self, images):
        img_list = []
        for img in images:
            img_list.append ((img['id'], img['image_path'], img['master_name']))
        self.cursor.executemany ("INSERT INTO images VALUES (?, ?, ?)", img_list)

        self.conn.commit ()
    
    def add_column (self, column_name):
        self.cursor.execute ("""ALTER TABLE images ADD COLUMN %s""" % column_name)

    def save (self):
        self.conn.commit ()
    
    def get_column_names (self):
        self.cursor.execute ('SELECT * FROM images')
        return tuple (map (lambda x: x[0], self.cursor.description))

    def update_prop (self, id, prop, val, id_name = 'id'):
        if type (id) is str:
            self.cursor.execute ("""UPDATE images SET %s = '%s' WHERE %s='%s'""" % (prop, val,id_name, str (id)))
        else:
            self.cursor.execute ("""UPDATE images SET %s = '%s' WHERE %s=%d""" % (prop, val,id_name, id))
            
        self.conn.commit ()
    
    def get_data_by_prop (self, prop_name):
        self.cursor.execute ('SELECT MIN(id) AS id, image_path, %s FROM images GROUP BY id' % prop_name)
        return self.cursor.fetchall ()

    def get_by_prop (self, field, prop_name, prop_val):
        if type (prop_val) is str:
            self.cursor.execute ("SELECT %s FROM images WHERE %s = '%s' GROUP BY %s" % (field, prop_name, prop_val, field))
        else:
            self.cursor.execute ('SELECT %s FROM images WHERE %s = %s GROUP BY %s' % (field, prop_name, prop_val, field))
        return self.cursor.fetchall ()
    def get_column_unique_values (self, column_name):
        self.cursor.execute ('SELECT %s FROM images GROUP BY %s' % (column_name, column_name))
        return self.cursor.fetchall ()

    def print (self):
        self.cursor.execute ('SELECT MIN(id) AS id, image_path, type, master_name, mindmap_type FROM images GROUP BY id')
        print (self.cursor.fetchall ())
if __name__ == '__main__':
    db = image_database ('../db/Map.db')

    db.print ()
