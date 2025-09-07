import os
import mysql.connector
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MySQL configuration - FIXED to use public URL
def get_mysql_config():
    # Try to get from MYSQL_PUBLIC_URL first (this is the accessible one)
    mysql_public_url = os.getenv('MYSQL_PUBLIC_URL')
    
    if mysql_public_url:
        try:
            parsed = urlparse(mysql_public_url)
            return {
                'host': parsed.hostname,
                'user': parsed.username,
                'password': parsed.password,
                'database': parsed.path.lstrip('/'),
                'port': parsed.port or 3306,
                'raise_on_warnings': True
            }
        except Exception as e:
            print(f"Error parsing MYSQL_PUBLIC_URL: {e}")
    
    # Try regular MYSQL_URL as fallback
    mysql_url = os.getenv('MYSQL_URL')
    if mysql_url:
        try:
            parsed = urlparse(mysql_url)
            return {
                'host': parsed.hostname,
                'user': parsed.username,
                'password': parsed.password,
                'database': parsed.path.lstrip('/'),
                'port': parsed.port or 3306,
                'raise_on_warnings': True
            }
        except Exception as e:
            print(f"Error parsing MYSQL_URL: {e}")
    
    # Final fallback to individual environment variables
    return {
        'host': os.getenv('MYSQLHOST'),
        'user': os.getenv('MYSQLUSER'),
        'password': os.getenv('MYSQLPASSWORD'),
        'database': os.getenv('MYSQLDATABASE'),
        'port': int(os.getenv('MYSQLPORT', '3306')),
        'raise_on_warnings': True
    }

MYSQL_CONFIG = get_mysql_config()
print(f"MySQL Config: { {k: v for k, v in MYSQL_CONFIG.items() if k != 'password'} }")

def get_mysql_connection():
    """Create and return MySQL connection"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print(f"✅ MySQL connection successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ MySQL Connection Error: {err}")
        print(f"Attempted connection with config: { {k: v for k, v in MYSQL_CONFIG.items() if k != 'password'} }")
        return None

def init_database():
    """Initialize the database with required tables"""
    conn = get_mysql_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Create patients table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create health_data table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT,
                heart_rate INT,
                temperature FLOAT,
                spo2 FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Insert default patient
            cursor.execute("SELECT COUNT(*) FROM patients WHERE id = 1")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO patients (name, age) VALUES (%s, %s)", ("Test Patient", 30))
            
            conn.commit()
            print("✅ Database tables created successfully!")
            
        except mysql.connector.Error as err:
            print(f"❌ MySQL Error during initialization: {err}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    else:
        print("❌ Cannot create MySQL database connection")

def execute_query(query, params=()):
    """Execute INSERT, UPDATE, DELETE queries"""
    conn = get_mysql_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except mysql.connector.Error as err:
            print(f"❌ MySQL Query Error: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return None

def fetch_all(query, params=()):
    """Fetch all rows from a query"""
    conn = get_mysql_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            print(f"❌ MySQL Fetch Error: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return []

# Initialize database on startup
init_database()

@app.route('/')
def home():
    return "Healthcare Monitoring System API is running with MySQL! 🚀"

@app.route('/api/test-db')
def test_db():
    conn = get_mysql_connection()
    if conn:
        conn.close()
        return jsonify({"message": "✅ Database connection successful!"})
    else:
        return jsonify({"error": "❌ Database connection failed"}), 500

@app.route('/api/debug-db')
def debug_db():
    """Debug endpoint to check database status"""
    try:
        conn = get_mysql_connection()
        if not conn:
            return jsonify({"error": "No database connection", "config": {k: v for k, v in MYSQL_CONFIG.items() if k != 'password'}}), 500
            
        cursor = conn.cursor(dictionary=True)
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # Check data in tables
        health_data_count = 0
        patients_count = 0
        
        table_names = [list(table.values())[0] for table in tables]
        
        if 'health_data' in table_names:
            cursor.execute("SELECT COUNT(*) as count FROM health_data")
            health_data_count = cursor.fetchone()['count']
            
        if 'patients' in table_names:
            cursor.execute("SELECT COUNT(*) as count FROM patients")
            patients_count = cursor.fetchone()['count']
            
        conn.close()
        
        return jsonify({
            "tables": table_names,
            "health_data_count": health_data_count,
            "patients_count": patients_count,
            "config": {k: v for k, v in MYSQL_CONFIG.items() if k != 'password'}
        })
    except Exception as e:
        return jsonify({"error": str(e), "config": {k: v for k, v in MYSQL_CONFIG.items() if k != 'password'}}), 500

# Keep all your existing API endpoints below...
# [Your existing /api/health-data, /api/patients endpoints here]

if __name__ == '__main__':
    print("🚀 Starting Healthcare API Server...")
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)), debug=False)