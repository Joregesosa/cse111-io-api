import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('app/DB/io_db.db')
        self.cursor = self.conn.cursor()

    def getCursor(self):
        return self.cursor
    
    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()