from flask import Flask, render_template, request, jsonify
import os
import numpy as np
from datetime import datetime
import joblib

app = Flask(__name__)
app.secret_key = 'house-price-prediction-secret-key'

# Global variables
model = None
scaler = None
model_loaded = False

def load_model():
    """Load the trained model and scaler"""
    global model, scaler, model_loaded
    try:
        model_path = 'model/saved_models/house_price_model.pkl'
        scaler_path = 'model/saved_models/scaler.pkl'
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            model_loaded = True
            print("✅ Model loaded successfully!")
        else:
            print("⚠️ Model files not found. Please train the model first.")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")

# Load model on startup
load_model()

@app.route('/')
def index():
    """Home page - Main prediction interface"""
    return render_template('index.html', 
                         model_loaded=model_loaded,
                         current_year=datetime.now().year)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    if not model_loaded:
        return render_template('index.html', 
                             error="⚠️ Model is not loaded. Please contact administrator.",
                             model_loaded=model_loaded,
                             current_year=datetime.now().year)
    
    try:
        # Get and validate form data
        bedrooms = float(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        area = float(request.form['area'])
        
        # Input validation
        if bedrooms < 1 or bedrooms > 10:
            raise ValueError("Bedrooms must be between 1 and 10")
        if bathrooms < 0.5 or bathrooms > 8:
            raise ValueError("Bathrooms must be between 0.5 and 8")
        if area < 300 or area > 50000:
            raise ValueError("Area must be between 300 and 50,000 sq.ft.")
        
        # Make prediction
        features = np.array([[bedrooms, bathrooms, area]])
        features_scaled = scaler.transform(features)
        predicted_price = model.predict(features_scaled)[0]
        
        # Format price in Indian Rupees
        if predicted_price >= 10000000:  # 1 Crore+
            formatted_price = f"₹{predicted_price/10000000:.2f} Crore"
        elif predicted_price >= 100000:  # 1 Lakh+
            formatted_price = f"₹{predicted_price/100000:.2f} Lakh"
        else:
            formatted_price = f"₹{predicted_price:,.0f}"
        
        # Price per sq.ft.
        price_per_sqft = predicted_price / area
        
        return render_template('result.html',
                             price=formatted_price,
                             price_raw=predicted_price,
                             price_per_sqft=f"₹{price_per_sqft:,.0f}",
                             bedrooms=bedrooms,
                             bathrooms=bathrooms,
                             area=area,
                             current_year=datetime.now().year)
    
    except ValueError as e:
        return render_template('index.html', 
                             error=str(e),
                             model_loaded=model_loaded,
                             current_year=datetime.now().year)
    except Exception as e:
        return render_template('index.html', 
                             error=f"Prediction error: {str(e)}",
                             model_loaded=model_loaded,
                             current_year=datetime.now().year)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic access"""
    if not model_loaded:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        bedrooms = float(data['bedrooms'])
        bathrooms = float(data['bathrooms'])
        area = float(data['area'])
        
        features = np.array([[bedrooms, bathrooms, area]])
        features_scaled = scaler.transform(features)
        predicted_price = model.predict(features_scaled)[0]
        
        # Format based on value
        if predicted_price >= 10000000:
            formatted = f"₹{predicted_price/10000000:.2f} Cr"
        elif predicted_price >= 100000:
            formatted = f"₹{predicted_price/100000:.2f} L"
        else:
            formatted = f"₹{predicted_price:,.0f}"
        
        return jsonify({
            'success': True,
            'predicted_price': float(predicted_price),
            'formatted_price': formatted,
            'price_per_sqft': float(predicted_price / area),
            'features': {
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area': area
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', 
                         error="Page not found. Redirected to home.",
                         model_loaded=model_loaded,
                         current_year=datetime.now().year)

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('index.html', 
                         error="Internal server error. Please try again.",
                         model_loaded=model_loaded,
                         current_year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)