import mysql.connector
import os
import sys

# Add the parent directory to Python path so config can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

def init_database():
    try:
        # Connect to MySQL server without specifying a database
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        
        cursor = conn.cursor()
        
        # Read and execute schema file
        with open('database/schema.sql', 'r') as file:
            sql_commands = file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        print("Database initialized successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_database()