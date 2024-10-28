from ..DB.db_conn import Database
class Model:
    
    def __init__(self):
        child = (self.__class__.__name__).lower()
        last = child[-1]
        if last == "y":
            self._table = child[:-1] + "ies"
        elif last == "s":
            self._table = child + "es"
        else:
            self._table = child + "s"

    async def all(self):
        try:
            conn = Database()
            cursor = conn.getCursor()
            query = f"SELECT * FROM {self._table}"
            cursor.execute(query)
            rs = cursor.fetchall()
            return rs
        except Exception as e:
            raise e
        finally:
            conn.close()
            
    async def find(self, id):
        try:
            conn = Database()
            conn.row_factory()
            cursor = conn.getCursor()
            query = f"SELECT * FROM {self._table} WHERE id = ?"
            values = (id,)
            cursor.execute(query, values)
            rs =  cursor.fetchone()
            return dict(rs) if rs else None
        except Exception as e:
            raise e
        finally:
            conn.close()

    async def where(self, field, value):
        try:
            conn = Database()
            conn.row_factory()
            cursor = conn.getCursor()
            query = f"SELECT * FROM {self._table} WHERE {field} = ?"
            values = (value,)
            cursor.execute(query, values)
            rs =  cursor.fetchall()
            for i, r in enumerate(rs):
                rs[i] = dict(r)
            return rs
        except Exception as e:
            raise e
        finally:
            conn.close()

    async def create(self, data):
        try:
            conn = Database()
            cursor = conn.getCursor()
            keys = ", ".join(data.keys())
            values = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {self._table} ({keys}) VALUES ({values})"
            cursor.execute(query, list(data.values()))
            conn.commit()
            rs =  True 
            return rs
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    async def update(self, id, data):
        try:
            conn = Database()
            cursor = conn.getCursor()
            query = f"UPDATE {self._table} SET "
            query += ", ".join([f"{key} = ?" for key in data.keys()])
            query += f" WHERE id = {id}"
            values = list(data.values())
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            print('error')
            conn.rollback()
            raise e
        finally:
            conn.close()

    async def delete(self, id):
        try:
            conn = Database()
            cursor = conn.getCursor()
            query = f"DELETE FROM {self._table} WHERE id = %s"
            values = (id,)
            cursor.execute(query, values)
            return cursor.rowcount
        except Exception as e:
            raise e
