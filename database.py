import mysql.connector
from mysql.connector import Error
import os

def create_connection():
    """Create a database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            database=os.environ.get('MYSQL_DB'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            port=os.environ.get('MYSQL_PORT', 3306)
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query, data=None):
    """Execute a single query"""
    cursor = None
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
            
        # For INSERT, UPDATE, DELETE operations
        if query.strip().lower().startswith(('insert', 'update', 'delete')):
            connection.commit()
            
        return cursor
    except Error as e:
        print(f"Error executing query: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def fetch_all(connection, query, data=None):
    """Fetch all results from a query"""
    cursor = None
    try:
        cursor = execute_query(connection, query, data)
        if cursor:
            return cursor.fetchall()
        return None
    except Error as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def fetch_one(connection, query, data=None):
    """Fetch a single result from a query"""
    cursor = None
    try:
        cursor = execute_query(connection, query, data)
        if cursor:
            return cursor.fetchone()
        return None