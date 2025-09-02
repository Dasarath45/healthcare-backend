CREATE DATABASE IF NOT EXISTS healthcare_db;
USE healthcare_db;

CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    pulse_rate INT,
    temperature FLOAT DEFAULT NULL,
    oxygen_level FLOAT DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50) UNIQUE NOT NULL,
    patient_id INT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    last_seen TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE SET NULL
);