import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Smart_IOT45',
    database='healthcare_db'
)

cursor = conn.cursor()
cursor.execute("INSERT INTO patients (name, age) VALUES (%s, %s)", ("Test Patient", 30))
conn.commit()
print("Patient created with ID:", cursor.lastrowid)
cursor.close()
conn.close()