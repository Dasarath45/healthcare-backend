import mysql.connector

print("Testing MySQL connection...")
try:
    conn = mysql.connector.connect(
        host='10.125.255.101',
        user='root',
        password='Smart_IOT45',
        database='healthcare_db'
    )
    print("✅ SUCCESS: MySQL Connection Working!")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")