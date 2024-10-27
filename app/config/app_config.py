from dotenv import load_dotenv
import os

load_dotenv()
app_config = {
    "APP_NAME": os.getenv("APP_NAME"),
    "APP_KEY": os.getenv("APP_KEY"),
}
