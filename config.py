import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQLHOST', 'mysql.railway.internal')  # Internal host
    MYSQL_USER = os.getenv('MYSQLUSER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD', 'RpmwtBqkFPIrEvqbYUGiFTBqvdEtdLgp')
    MYSQL_DB = os.getenv('MYSQLDATABASE', 'railway')
    MYSQL_PORT = int(os.getenv('MYSQLPORT', '3306'))