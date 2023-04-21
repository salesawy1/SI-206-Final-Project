import sqlite3

class SQLInterface:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        
    def get_table(self, table_name):
        self.c.execute('SELECT * FROM ' + table_name)
        return self.c.fetchall()
    
    def create_table(self, table_name, columns):
        self.c.execute('CREATE TABLE ' + table_name + ' (' + ', '.join([c['name'] + ' ' + c['type'] for c in columns]) + ')')
        self.conn.commit()
        
    def get_or_create_table(self, table_name, columns):
        try:
            self.get_table(table_name)
        except:
            self.create_table(table_name, columns)

    def insert(self, table_name, columns, values, limit):
        self.c.execute('SELECT ' + columns + ' FROM ' + table_name)
        existing = [v[0] for v in self.c.fetchall()]
        values = [v for v in values if v not in existing]
        if len(values) > limit:
            values = values[:limit]
        self.c.executemany('INSERT INTO ' + table_name + ' (' + columns + ') VALUES (?)', [(v,) for v in values])
        self.conn.commit()
 
    def update(self, table_name, column, value, condition):
        self.c.execute('UPDATE ' + table_name + ' SET ' + column + ' = ' + value + ' WHERE ' + condition)
        self.conn.commit()
        
    def delete(self, table_name, condition):
        self.c.execute('DELETE FROM ' + table_name + ' WHERE ' + condition)
        self.conn.commit()
        
    def select(self, table_name, columns, condition):
        self.c.execute('SELECT ' + columns + ' FROM ' + table_name + ' WHERE ' + condition)
        return self.c.fetchall()
    
    def close(self):
        self.conn.close()