from flask import Flask, jsonify, request
from flask_cors import CORS
from database import create_connection, execute_query, fetch_all, fetch_one
import os

app = Flask(__name__)
CORS(app)

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "message": "Healthcare Backend API is running"})

# Sensor data endpoint - GET all data and POST new data
@app.route('/api/sensor', methods=['GET', 'POST'])
def sensor_data():
    connection = create_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        if request.method == 'GET':
            # Fetch all sensor data
            query = "SELECT * FROM sensor_data ORDER BY timestamp DESC"
            results = fetch_all(connection, query)
            
            if results is None:
                return jsonify({"error": "Failed to fetch data"}), 500
                
            sensor_data = []
            for row in results:
                sensor_data.append({
                    "id": row[0],
                    "patient_id": row[1],
                    "heart_rate": row[2],
                    "temperature": row[3],
                    "timestamp": row[4]
                })
                
            return jsonify(sensor_data)
            
        elif request.method == 'POST':
            # Insert new sensor data
            data = request.json
            query = """
                INSERT INTO sensor_data (patient_id, heart_rate, temperature)
                VALUES (%s, %s, %s)
            """
            values = (data['patient_id'], data['heart_rate'], data['temperature'])
            
            cursor = execute_query(connection, query, values)
            if cursor and cursor.lastrowid:
                return jsonify({
                    "message": "Data inserted successfully",
                    "id": cursor.lastrowid
                }), 201
            else:
                return jsonify({"error": "Failed to insert data"}), 500
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()

# Get sensor data for a specific patient
@app.route('/api/sensor/patient/<int:patient_id>', methods=['GET'])
def get_patient_data(patient_id):
    connection = create_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        query = "SELECT * FROM sensor_data WHERE patient_id = %s ORDER BY timestamp DESC"
        results = fetch_all(connection, query, (patient_id,))
        
        if results is None:
            return jsonify({"error": "Failed to fetch data"}), 500
            
        sensor_data = []
        for row in results:
            sensor_data.append({
                "id": row[0],
                "patient_id": row[1],
                "heart_rate": row[2],
                "temperature": row[3],
                "timestamp": row[4]
            })
            
        return jsonify(sensor_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))