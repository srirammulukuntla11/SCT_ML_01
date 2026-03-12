import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_and_prepare_data(filepath):
    """
    Load and prepare the dataset for training
    """
    print("📂 Loading dataset...")
    df = pd.read_csv(filepath)
    
    print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\n📊 First 5 rows:")
    print(df.head())
    
    print("\n📋 Column names:")
    print(df.columns.tolist())
    
    return df

def train_model(df, target_column, feature_columns):
    """
    Train the linear regression model
    """
    print("\n🎯 Training model...")
    
    # Prepare features and target
    X = df[feature_columns]
    y = df[target_column]

    # convert price to rupees (dataset values appear to be in crores)
    print("💱 Scaling target values to rupees (1 crore = 10,000,000)")
    y = y * 1e7
    
    # Handle missing values
    print("🔧 Handling missing values...")
    X = X.fillna(X.mean())
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"📈 Training set: {X_train.shape[0]} samples")
    print(f"📉 Test set: {X_test.shape[0]} samples")
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
    
    print("\n📊 Model Performance Metrics (rupees):")
    print(f"   Mean Squared Error (MSE): ₹{mse:,.2f}")
    print(f"   Root Mean Squared Error (RMSE): ₹{rmse:,.2f}")
    print(f"   Mean Absolute Error (MAE): ₹{mae:,.2f}")
    print(f"   R² Score: {r2:.4f}")
    print(f"   Cross-validation R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Feature importance (coefficients)
    print("\n🔍 Feature Coefficients:")
    for feature, coef in zip(feature_columns, model.coef_):
        print(f"   {feature}: {coef:.2f}")
    
    return model, scaler, {
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'cv_scores': cv_scores,
        'feature_columns': feature_columns,
        'target_column': target_column
    }

def save_model(model, scaler, metrics):
    """
    Save the trained model and scaler
    """
    # Create saved_models directory if it doesn't exist
    os.makedirs('model/saved_models', exist_ok=True)
    
    # Save model and scaler
    joblib.dump(model, 'model/saved_models/house_price_model.pkl')
    joblib.dump(scaler, 'model/saved_models/scaler.pkl')
    
    # Save metrics
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv('model/saved_models/training_metrics.csv', index=False)
    
    print("\n💾 Model saved successfully!")
    print("   📍 model/saved_models/house_price_model.pkl")
    print("   📍 model/saved_models/scaler.pkl")
    print("   📍 model/saved_models/training_metrics.csv")

def main():
    """
    Main training function
    """
    print("="*50)
    print("🏠 HOUSE PRICE PREDICTION MODEL TRAINING")
    print("="*50)
    
    # IMPORTANT: Update these based on your dataset
    # Please check the column names printed above and update these variables
    DATASET_PATH = 'data/dataset.csv'  # Change this to your actual filename
    TARGET_COLUMN = 'price'  # Change this to your price column name
    # dataset.csv uses 'bedRoom' (capital R) and 'bathroom' (singular).
    # the UI expects bedrooms/bathrooms so we map them here accordingly.
    FEATURE_COLUMNS = ['bedRoom', 'bathroom', 'area']  # Adjusted to match CSV
    
    try:
        # Load data
        df = load_and_prepare_data(DATASET_PATH)
        
        # Train model
        model, scaler, metrics = train_model(df, TARGET_COLUMN, FEATURE_COLUMNS)
        
        # Save model
        save_model(model, scaler, metrics)
        
        print("\n" + "="*50)
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("="*50)
        
    except FileNotFoundError:
        print(f"\n❌ Error: Dataset not found at {DATASET_PATH}")
        print("Please make sure:")
        print("1. Your dataset file is in the 'data' folder")
        print("2. Update the DATASET_PATH variable with the correct filename")
    except KeyError as e:
        print(f"\n❌ Error: Column not found - {e}")
        print("\nPlease update the column names in the script:")
        print(f"   TARGET_COLUMN = 'your_price_column'")
        print(f"   FEATURE_COLUMNS = ['your_bedroom_col', 'your_bathroom_col', 'your_area_col']")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()