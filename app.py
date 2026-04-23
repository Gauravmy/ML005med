"""
Flask ML Web Application
Full-stack app combining Flask, SQLite, ML Model, Real-time API, and responsive UI
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import joblib
import os
import requests
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['DATABASE'] = 'students.db'

# ==================== DATABASE SETUP ====================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with students table"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            study_hours REAL NOT NULL,
            attendance REAL NOT NULL,
            prediction INTEGER NOT NULL,
            prediction_label TEXT NOT NULL,
            temperature REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()
    db.close()

# Initialize database on startup
init_db()

# ==================== LOAD ML MODEL ====================

def load_model():
    """Load trained ML model and scaler"""
    try:
        if os.path.exists('models/model.pkl') and os.path.exists('models/scaler.pkl'):
            model = joblib.load('models/model.pkl')
            scaler = joblib.load('models/scaler.pkl')
            return model, scaler
        else:
            print("Warning: Model files not found. Please run train_model.py first.")
            return None, None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

model, scaler = load_model()

# ==================== GET REAL-TIME DATA ====================

def get_weather_data():
    """
    Fetch real-time weather data from OpenWeatherMap API
    Free API - no key required for demo
    Returns temperature or default value if API fails
    """
    try:
        # Using wttr.in as FREE weather API (no API key required)
        response = requests.get('https://wttr.in/New%20York?format=j1', timeout=5)
        if response.status_code == 200:
            data = response.json()
            current_temp = data['current_condition'][0]['temp_C']
            description = data['current_condition'][0]['description']
            return {'temperature': current_temp, 'description': description}
    except Exception as e:
        print(f"Error fetching weather: {e}")
    
    # Return default data if API fails
    return {'temperature': 25, 'description': 'Weather data unavailable'}

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    """Home page"""
    weather = get_weather_data()
    return render_template('index.html', weather=weather)

@app.route('/students')
def get_students():
    """Get all students from database"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM students ORDER BY timestamp DESC')
        students = [dict(row) for row in cursor.fetchall()]
        db.close()
        return jsonify({'success': True, 'students': students})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/form')
def form_page():
    """Form page - returns the form section"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make prediction using ML model
    Input: name, study_hours, attendance
    Output: prediction (0=Fail, 1=Pass) and weather data
    """
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        study_hours = float(data.get('study_hours', 0))
        attendance = float(data.get('attendance', 0))
        
        # Validate inputs
        if not name or study_hours < 0 or attendance < 0 or attendance > 100:
            return jsonify({'success': False, 'error': 'Invalid input values'})
        
        # Check if model is loaded
        if model is None or scaler is None:
            return jsonify({'success': False, 'error': 'ML model not loaded. Run train_model.py'})
        
        # Prepare data for prediction
        input_data = [[study_hours, attendance]]
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_label = 'PASS' if prediction == 1 else 'FAIL'
        
        # Get real-time temperature
        weather = get_weather_data()
        temperature = weather['temperature']
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'prediction_label': prediction_label,
            'temperature': temperature,
            'weather_description': weather['description']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Prediction error: {str(e)}'})

@app.route('/save', methods=['POST'])
def save_student():
    """Save student data and prediction to database"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        study_hours = float(data.get('study_hours', 0))
        attendance = float(data.get('attendance', 0))
        prediction = int(data.get('prediction', 0))
        prediction_label = data.get('prediction_label', 'UNKNOWN')
        temperature = data.get('temperature')
        
        # Validate inputs
        if not name:
            return jsonify({'success': False, 'error': 'Name is required'})
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO students (name, study_hours, attendance, prediction, prediction_label, temperature)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, study_hours, attendance, prediction, prediction_label, temperature))
        db.commit()
        student_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            'success': True,
            'message': f'Student "{name}" saved successfully!',
            'student_id': student_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Save error: {str(e)}'})

@app.route('/delete/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student record"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        db.commit()
        db.close()
        return jsonify({'success': True, 'message': 'Student deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download-data', methods=['GET'])
def download_data():
    """Get all data as JSON for export"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM students ORDER BY timestamp DESC')
        students = [dict(row) for row in cursor.fetchall()]
        db.close()
        return jsonify({'success': True, 'data': students, 'count': len(students)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    """
    Run Flask app
    Debug mode: True for development, False for production
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
