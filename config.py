import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")

DB_URL = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'