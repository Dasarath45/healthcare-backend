import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQLHOST = os.getenv('MYSQLHOST', 'mysql.railway.internal')
    MYSQLUSER = os.getenv('MYSQLUSER', 'root')
    MYSQLPASSWORD = os.getenv('MYSQLPASSWORD', 'RpmwtBqkFPIrEvqbYUGifTBqvdEtdLgp')
    MYSQLDATABASE = os.getenv('MYSQLDATABASE', 'railway')
    MYSQLPORT = int(os.getenv('MYSQLPORT', '3306'))