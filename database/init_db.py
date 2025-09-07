import mysql.connector
import os
import sys
from config import Config

def init_database():
    conn = None
    try:
        print("🔧 Attempting to connect to MySQL server...")
        print(f"Host: {Config.MYSQL_HOST}")
        print(f"User: {Config.MYSQL_USER}")
        print(f"Port: {Config.MYSQL_PORT}")
        
        # First connect without database to create it
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        
        cursor = conn.cursor()
        print("✅ Connected to MySQL server!")
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        print(f"✅ Database '{Config.MYSQL_DB}' created/verified")
        
        # Use the database
        cursor.execute(f"USE {Config.MYSQL_DB}")
        
        # Read and execute schema file
        print("📋 Executing schema...")
        with open('database/schema.sql', 'r') as file:
            sql_commands = file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    try:
                        cursor.execute(command)
                        print(f"✓ Executed: {command[:50]}...")
                    except mysql.connector.Error as err:
                        print(f"⚠️  Skipping command: {err}")
        
        conn.commit()
        print("🎉 Database initialized successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
        print("\n🔍 TROUBLESHOOTING:")
        print("1. Is MySQL running on 10.125.255.101?")
        print("2. Check MySQL username/password")
        print("3. Check if port 3306 is open")
        print("4. Try: mysql -h 10.125.255.101 -u root -p")
        
    except FileNotFoundError:
        print("❌ schema.sql file not found in database/ folder")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    init_database()