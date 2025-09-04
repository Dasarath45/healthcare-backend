import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Smart_IOT45')
    MYSQL_DB = os.getenv('MYSQL_DB', 'healthcare_db')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))