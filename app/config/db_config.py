from dotenv import load_dotenv
import os

load_dotenv()
db_config = {
    'host': os.getenv("DB_HOST"),
    'db' : os.getenv("DB_NAME"),
    'user' : os.getenv("DB_USER"),
    'password' : os.getenv("DB_PASSWORD"),
    'port' : int(os.getenv("DB_PORT"))
}

 