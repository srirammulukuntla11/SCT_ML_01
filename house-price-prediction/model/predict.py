import joblib
import numpy as np
import pandas as pd
import os

class HousePricePredictor:
    """
    House Price Prediction Class
    """
    def __init__(self, model_path='model/saved_models/house_price_model.pkl', 
                 scaler_path='model/saved_models/scaler.pkl'):
        """
        Initialize the predictor by loading the trained model and scaler
        """
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        """Load the trained model and scaler"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                print("✅ Models loaded successfully!")
            else:
                print("⚠️ Model files not found. Please train the model first.")
        except Exception as e:
            print(f"❌ Error loading models: {str(e)}")
    
    def predict(self, bedrooms, bathrooms, area):
        """
        Predict house price based on features
        
        Args:
            bedrooms: Number of bedrooms
            bathrooms: Number of bathrooms
            area: Area in square feet
            
        Returns:
            Predicted price
        """
        if self.model is None or self.scaler is None:
            raise Exception("Models not loaded. Please train the model first.")
        
        # Create feature array
        features = np.array([[bedrooms, bathrooms, area]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        
        return prediction
    
    def predict_batch(self, features_df):
        """
        Predict prices for multiple houses
        
        Args:
            features_df: DataFrame with columns ['bedrooms', 'bathrooms', 'area']
            
        Returns:
            Array of predicted prices
        """
        if self.model is None or self.scaler is None:
            raise Exception("Models not loaded. Please train the model first.")
        
        features_scaled = self.scaler.transform(features_df)
        predictions = self.model.predict(features_scaled)
        
        return predictions
    
    def format_price_indian(self, price):
        """Format price in Indian currency style"""
        if price >= 10000000:  # 1 Crore+
            return f"₹{price/10000000:.2f} Crore"
        elif price >= 100000:  # 1 Lakh+
            return f"₹{price/100000:.2f} Lakh"
        else:
            return f"₹{price:,.0f}"

# Test the predictor
if __name__ == "__main__":
    try:
        predictor = HousePricePredictor()
        
        # Test prediction
        if predictor.model is not None:
            price = predictor.predict(3, 2, 1500)
            formatted = predictor.format_price_indian(price)
            print(f"\n🏠 Test Prediction:")
            print(f"   Bedrooms: 3")
            print(f"   Bathrooms: 2")
            print(f"   Area: 1500 sq ft")
            print(f"   Predicted Price: {formatted}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")