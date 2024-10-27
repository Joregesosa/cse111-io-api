from ..config.db_config import db_config
import aiomysql as aio
from aiomysql.cursors import DictCursor

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

    async def __execute(self, query, values=None) -> DictCursor:
        """ 
          Create a connection pool and execute the query and return the cursor.
        """
        pool = await aio.create_pool(**db_config)
        try:
            async with pool.acquire() as connection:
                async with connection.cursor(DictCursor) as cursor:
                    await cursor.execute(query, values)
                    if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                        await connection.commit()
                        
                    return cursor
        except Exception as e:
            raise e
        finally:
            pool.close()
            await pool.wait_closed()
         
    async def all(self):
        try:
            query = f"SELECT * FROM {self._table}"
            cursor = await self.__execute(query)
            rs = await cursor.fetchall()
            return rs
        except Exception as e:
            raise e
            
    async def find(self, id):
        try:
            query = f"SELECT * FROM {self._table} WHERE id = %s"
            values = (id,)
            cursor = await self.__execute(query, values)
            rs = await cursor.fetchone()
            return rs
        except Exception as e:
            raise e

    async def where(self, field, value):
        try:
            query = f"SELECT * FROM {self._table} WHERE {field} = %s"
            values = (value,)
            cursor = await self.__execute(query, values)
            rs = await cursor.fetchall()
            return rs

        except Exception as e:
            raise e

    async def create(self, data):
        try:
            keys = ", ".join(data.keys())
            values = ", ".join(["%s"] * len(data))
            query = f"INSERT INTO {self._table} ({keys}) VALUES ({values})"
            cursor = await self.__execute(query, list(data.values()))     
            rs =  cursor.lastrowid   
            return rs
        except Exception as e:
            raise e

    async def update(self, id, data):
        try:
            query = f"UPDATE {self._table} SET "
            query += ", ".join([f"{key} = %s" for key in data.keys()])
            query += f" WHERE id = {id}"
            cursor = await self.__execute(query, list(data.values()))
            return cursor.rowcount
        except Exception as e:
            raise e

    async def delete(self, id):
        try:
            query = f"DELETE FROM {self._table} WHERE id = %s"
            values = (id,)
            cursor = await self.__execute(query, values)
            return cursor.rowcount
        except Exception as e:
            raise e
