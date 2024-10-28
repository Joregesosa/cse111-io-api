import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('app/DB/io_db.sqlite')
        
    def getCursor(self):
        cursor = self.conn.cursor()
        return cursor
    
    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()
        
    def row_factory(self):
         self.conn.row_factory = sqlite3.Row