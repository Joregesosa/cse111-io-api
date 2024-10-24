import mysql.connector
from mysql.connector import Error
from config.db_config import db_config
 
try:
  connection = mysql.connector.connect(
        host=db_config['DB_HOST'],
        database=db_config['DB_NAME'],
        user=db_config['DB_USER'],
        password=db_config['DB_PASSWORD'],
        port = db_config['DB_PORT'] 
  )
except Error as e:
  print(f'An exception occurred /n{e}')