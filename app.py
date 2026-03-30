from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
import json

app = Flask(__name__)

# Load models and artifacts globally at startup
MODEL_DIR = 'models'
try:
    reg_model = joblib.load(os.path.join(MODEL_DIR, 'linear_model.pkl'))
    clf_model = joblib.load(os.path.join(MODEL_DIR, 'classifier_model.pkl'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    
    with open(os.path.join(MODEL_DIR, 'metrics.json'), 'r') as f:
        model_metrics = json.load(f)
        
    print("Models loaded successfully.")
except Exception as e:
    print(f"Warning: Models not fully loaded. Run ml_pipeline.py first. Error: {e}")
    reg_model, clf_model, scaler, model_metrics = None, None, None, {}

# Helper to process form input into scaled DataFrame
def process_input(data):
    # Ensure order matches training features:
    # ['study_hours_per_week', 'attendance_percentage', 'previous_exam_score', 
    # 'assignments_completed', 'sleep_hours', 'extracurricular_hours', 
    # 'parent_education_level', 'internet_access']
    
    features = {
        'study_hours_per_week': [float(data.get('study_hours_per_week', 0))],
        'attendance_percentage': [float(data.get('attendance_percentage', 0))],
        'previous_exam_score': [float(data.get('previous_exam_score', 0))],
        'assignments_completed': [int(data.get('assignments_completed', 0))],
        'sleep_hours': [float(data.get('sleep_hours', 0))],
        'extracurricular_hours': [float(data.get('extracurricular_hours', 0))],
        'parent_education_level': [int(data.get('parent_education_level', 1))],
        'internet_access': [int(data.get('internet_access', 0))]
    }
    df = pd.DataFrame(features)
    scaled_features = scaler.transform(df)
    return scaled_features

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict-score', methods=['POST'])
def predict_score():
    if not reg_model or not scaler:
        return jsonify({'error': 'Model not trained yet'}), 500
        
    try:
        data = request.json
        X_test = process_input(data)
        
        # Predict uses [0] to extract single value from array
        prediction = reg_model.predict(X_test)[0]
        prediction = min(max(prediction, 0.0), 100.0) # Clamp 0-100
        
        return jsonify({
            'success': True,
            'predicted_score': round(prediction, 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict-grade', methods=['POST'])
def predict_grade():
    if not clf_model or not scaler:
        return jsonify({'error': 'Model not trained yet'}), 500
        
    try:
        data = request.json
        X_test = process_input(data)
        
        prediction = clf_model.predict(X_test)[0]
        
        # Get probability distributions
        probabilities = clf_model.predict_proba(X_test)[0]
        classes = clf_model.classes_
        prob_dict = {str(c): round(float(p)*100, 1) for c, p in zip(classes, probabilities)}
        
        return jsonify({
            'success': True,
            'predicted_grade': str(prediction),
            'probabilities': prob_dict
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/model-metrics', methods=['GET'])
def get_metrics():
    if not model_metrics:
        return jsonify({'error': 'Metrics not found. Train model first.'}), 404
        
    return jsonify(model_metrics)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
