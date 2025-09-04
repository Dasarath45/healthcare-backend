from flask import Flask, request, jsonify
from flask_cors import CORS
from models import PatientModel, SensorDataModel, DeviceModel
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize models
patient_model = PatientModel()
sensor_model = SensorDataModel()
device_model = DeviceModel()

@app.route('/')
def home():
    return jsonify({"message": "Healthcare Monitoring System API"})

# ESP32 endpoint for both pulse and temperature sensors
@app.route('/api/sensor', methods=['POST'])
def receive_sensor_data():
    try:
        # Get data regardless of Content-Type
        if request.content_type and 'application/json' in request.content_type:
            data = request.get_json()
        else:
            # Handle form data or any other content type
            data = {
                'patient_id': request.form.get('patient_id', request.args.get('patient_id')),
                'pulse_rate': request.form.get('pulse_rate', request.args.get('pulse_rate')),
                'temperature': request.form.get('temperature', request.args.get('temperature')),
                'device_id': request.form.get('device_id', request.args.get('device_id'))
            }
        
        # Convert string values to appropriate types
        patient_id = int(data.get('patient_id', 0))
        pulse_rate = int(data.get('pulse_rate', 0))
        device_id = data.get('device_id', 'unknown')
        
        # Handle temperature - convert only if provided
        temp_value = data.get('temperature')
        if temp_value is not None and temp_value != '':
            temperature = float(temp_value)
            # Validate temperature (human range: 20°C to 45°C)
            if not (20.0 <= temperature <= 45.0):
                return jsonify({"error": "Invalid temperature"}), 400
        else:
            temperature = None  # Set to NULL for database
        
        # Validate other data
        if not (0 < patient_id < 1000):
            return jsonify({"error": "Invalid patient ID"}), 400
        
        if not (30 <= pulse_rate <= 200):
            return jsonify({"error": "Invalid pulse rate"}), 400
        
        # Store sensor data (both pulse rate and temperature)
        sensor_id = sensor_model.create(
            patient_id, pulse_rate, temperature, None
        )
        
        # Update device status
        if device_id != 'unknown':
            device_model.register(device_id, patient_id)
            device_model.update_status(device_id, 'active')
        
        if sensor_id:
            return jsonify({"id": sensor_id, "message": "Sensor data received"}), 201
        return jsonify({"error": "Failed to store data"}), 500
        
    except Exception as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400

# Keep the old endpoint for backward compatibility
@app.route('/api/sensor/pulse', methods=['POST'])
def receive_pulse_data():
    # This now redirects to the main sensor endpoint
    return receive_sensor_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)