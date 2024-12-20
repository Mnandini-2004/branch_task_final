from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import joblib

app = Flask(__name__)

# Load the saved model and scaler
try:
    model = pickle.load(open('loan_outcome_model.pkl', 'rb'))
    scaler = joblib.load('scaler.pkl')
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    raise

def engineer_datetime_features(data):
    """
    Create datetime features consistent with training pipeline
    """
    df = pd.DataFrame([data])
    
    # Convert string inputs to datetime
    datetime_cols = ['application_at', 'gps_fix_at', 'server_upload_at']
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])
    
    # Calculate time differences
    df['time_since_gps_fix'] = (df['application_at'] - df['gps_fix_at']).dt.total_seconds() / 3600
    df['upload_delay'] = (df['server_upload_at'] - df['gps_fix_at']).dt.total_seconds() / 60
    
    # Extract time features
    df['application_hour'] = df['application_at'].dt.hour
    df['application_day'] = df['application_at'].dt.day
    df['application_month'] = df['application_at'].dt.month
    df['is_weekend'] = df['application_at'].dt.dayofweek.isin([5, 6]).astype(int)
    
    # Select and order features to match training data
    final_features = [
        'user_id', 'age', 'cash_incoming_30days',
        'time_since_gps_fix', 'upload_delay',
        'application_hour', 'application_day', 'application_month',
        'is_weekend'
    ]
    
    return df[final_features]

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Service is running'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get json data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'user_id', 'application_at', 'gps_fix_at', 
            'server_upload_at', 'age', 'cash_incoming_30days'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400
        
        # Process features
        processed_features = engineer_datetime_features(data)
        
        # Scale features
        scaled_features = scaler.transform(processed_features)
        
        # Make prediction
        prediction = model.predict(scaled_features)[0]
        prediction_proba = model.predict_proba(scaled_features)[0][1]
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'probability': float(prediction_proba),
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)