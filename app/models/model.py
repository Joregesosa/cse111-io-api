from config.db_conn import connection

class Model():
 
    def __init__(self):
        child = (self.__class__.__name__).lower()
        last = child[-1]
        if last == "y":
            self._table = child[:-1] + "ies"
        elif last == "s":
            self._table = child + "es"
        else:
            self._table = child + "s"
            
        self.cursor = connection.cursor(dictionary=True)
        
    def all(self):
        try:
            query = f"SELECT * FROM {self._table}"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
    
    def find(self, id):
        try:
            query = f"SELECT * FROM {self._table} WHERE id = %s"
            values = (id,)
            self.cursor.execute(query, values)
            return self.cursor.fetchone()
        except Exception as e:
            raise e
    
    def where(self, field, value):
        try:
            query = f"SELECT * FROM {self._table} WHERE {field} = %s"
            values = (value,)
            self.cursor.execute(query, values)
            return self.cursor.fetchall 

        except Exception as e:
            raise e
    
    def create(self, data):
        try:
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {self._table} ({keys}) VALUES ({values})"
            self.cursor.execute(query, list(data.values()))
            connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            raise e
    
    def update(self, id, data):
        try:
            query = f"UPDATE {self._table} SET "
            query += ', '.join([f"{key} = %s" for key in data.keys()])
            query += f" WHERE id = {id}"
            self.cursor.execute(query, list(data.values()))
            connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            raise e
    
    def delete(self, id):
        try:
            query = f"DELETE FROM {self._table} WHERE id = {id}"
            self.cursor.execute(query)
            connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            raise e
    
 
