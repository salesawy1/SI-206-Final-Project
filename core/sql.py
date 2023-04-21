import sqlite3

class SQLInterface:
    def __init__(self, db_name, table_name, columns=None):
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        if columns:
            self.columns = columns # { name: string, type: string }[]
        
        # honestly just call get_or_create_table() here rather than always doing it outside
        self.get_or_create_table(columns)
        
    def get_table(self):
        self.c.execute('SELECT * FROM ' + self.table_name)
        return self.c.fetchall()
    
    def create_table(self, columns):
        self.c.execute('CREATE TABLE ' + self.table_name + ' (' + ', '.join([c['name'] + ' ' + c['type'] for c in columns]) + ')')
        self.conn.commit()
        
    def get_or_create_table(self, columns=None):
        try:
            self.get_table()
        except:
            self.create_table(columns)

    def insert(self, data, limit, identifier='id'):
        # make sure we don't insert duplicates
        db_data = self.select()
        if db_data:
            db_data_ids = [d[identifier] for d in db_data]
            data = [d for d in data if d[identifier] not in db_data_ids]
        data = data[:limit]
        
        for d in data:
            self.c.execute('INSERT INTO ' + self.table_name + ' VALUES (' + ', '.join(['\'' + str(value) + '\'' for value in d.values()]) + ')')
            
        self.conn.commit()
        
        return data
 
    def update(self, column, value, condition):
        self.c.execute('UPDATE ' + self.table_name + ' SET ' + column + ' = ' + value + ' WHERE ' + condition)
        self.conn.commit()
        
    def delete(self, condition):
        self.c.execute('DELETE FROM ' + self.table_name + ' WHERE ' + condition)
        self.conn.commit()
        
    def select(self, args=None):
        if args:
            self.c.execute('SELECT * FROM ' + self.table_name + ' ' + args)
        else:
            self.c.execute('SELECT * FROM ' + self.table_name)
        data = self.c.fetchall()
        
        # remap data to be a list of dicts
        data = [dict(zip([c[0] for c in self.c.description], d)) for d in data]
        
        return data
    
    def close(self):
        self.conn.close()