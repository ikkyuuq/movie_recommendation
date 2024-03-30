import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_READ_ACCESS_TOKEN = os.getenv('API_READ_ACCESS_TOKEN')
BASE_IMAGE_URL = os.getenv('BASE_IMAGE_URL')
HOST = os.getenv('HOST')
DB_USER = os.getenv('MYSQL_USERNAME')
DB_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
DATABASE = os.getenv('MYSQL_DATABASE')