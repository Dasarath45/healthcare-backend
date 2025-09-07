import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQLHOST = os.getenv('MYSQLHOST', 'trolley.proxy.rlwy.net')  # Changed default to PUBLIC host
    MYSQLUSER = os.getenv('MYSQLUSER', 'root')
    MYSQLPASSWORD = os.getenv('MYSQLPASSWORD', 'RpmwtBqKfPIrEvqbYUGifTBqvdEtdLgp')  # Fixed typo in default
    MYSQLDATABASE = os.getenv('MYSQLDATABASE', 'railway')
    MYSQLPORT = int(os.getenv('MYSQLPORT', '35987'))  # Changed default to PUBLIC port