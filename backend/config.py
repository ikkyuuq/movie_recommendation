import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_READ_ACCESS_TOKEN = os.getenv('API_READ_ACCESS_TOKEN')
BASE_IMAGE_URL = os.getenv('BASE_IMAGE_URL')
DB_URL = os.getenv('JAWSDB_URL')