import mysql.connector
from config import Config

class Database:
    def get_connection(self):
        return mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )

class PatientModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, name, age):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO patients (name, age) VALUES (%s, %s)",
                (name, age)
            )
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM patients")
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

class SensorDataModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, patient_id, pulse_rate, temperature=None, oxygen_level=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO sensor_data 
                (patient_id, pulse_rate, temperature, oxygen_level) 
                VALUES (%s, %s, %s, %s)""",
                (patient_id, pulse_rate, temperature, oxygen_level)
            )
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"MySQL Error in create(): {err}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_by_patient(self, patient_id, limit=100):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM sensor_data 
                WHERE patient_id = %s 
                ORDER BY timestamp DESC 
                LIMIT %s""",
                (patient_id, limit)
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

class DeviceModel:
    def __init__(self):
        self.db = Database()
    
    def register(self, device_id, patient_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO devices (device_id, patient_id) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                patient_id = COALESCE(%s, patient_id),
                last_seen = CURRENT_TIMESTAMP""",
                (device_id, patient_id, patient_id)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"MySQL Error in register(): {err}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def update_status(self, device_id, status):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE devices 
                SET status = %s, last_seen = CURRENT_TIMESTAMP 
                WHERE device_id = %s""",
                (status, device_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()