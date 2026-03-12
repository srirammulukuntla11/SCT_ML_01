import pandas as pd
import numpy as np
import os

class DataPreprocessor:
    """
    Data preprocessing class for Indian housing dataset
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.cleaned_df = None
        
    def load_data(self):
        """Load the dataset"""
        print(f"Loading data from {self.filepath}...")
        self.df = pd.read_csv(self.filepath)
        print(f"✅ Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        return self.df
    
    def explore_data(self):
        """Print basic information about the dataset"""
        print("\n📊 Dataset Info:")
        print(self.df.info())
        
        print("\n📈 Basic Statistics:")
        print(self.df.describe())
        
        print("\n🔍 Missing Values:")
        print(self.df.isnull().sum())
        
        print("\n🏷️ Column Names:")
        print(self.df.columns.tolist())
    
    def clean_data(self, bedroom_col=None, bathroom_col=None, area_col=None, price_col=None):
        """
        Clean and prepare the data
        
        Args:
            bedroom_col: Name of bedroom column
            bathroom_col: Name of bathroom column
            area_col: Name of area column
            price_col: Name of price column
        """
        self.cleaned_df = self.df.copy()
        
        # If column names are provided, rename them to standard names
        if bedroom_col and bathroom_col and area_col and price_col:
            column_mapping = {
                bedroom_col: 'bedrooms',
                bathroom_col: 'bathrooms',
                area_col: 'area',
                price_col: 'price'
            }
            self.cleaned_df.rename(columns=column_mapping, inplace=True)
        
        # Select only the columns we need
        required_columns = ['bedrooms', 'bathrooms', 'area', 'price']
        available_columns = [col for col in required_columns if col in self.cleaned_df.columns]
        
        if len(available_columns) < 4:
            print(f"⚠️ Warning: Not all required columns found. Found: {available_columns}")
        
        self.cleaned_df = self.cleaned_df[available_columns]
        
        # Handle missing values
        self.cleaned_df = self.cleaned_df.dropna()
        
        # Remove outliers (using IQR method)
        for col in available_columns:
            Q1 = self.cleaned_df[col].quantile(0.25)
            Q3 = self.cleaned_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.cleaned_df = self.cleaned_df[
                (self.cleaned_df[col] >= lower_bound) & 
                (self.cleaned_df[col] <= upper_bound)
            ]
        
        # Additional validations
        self.cleaned_df = self.cleaned_df[
            (self.cleaned_df['bedrooms'] > 0) & 
            (self.cleaned_df['bedrooms'] <= 10) &
            (self.cleaned_df['bathrooms'] > 0) & 
            (self.cleaned_df['bathrooms'] <= 8) &
            (self.cleaned_df['area'] > 100) & 
            (self.cleaned_df['area'] <= 50000) &
            (self.cleaned_df['price'] > 0)
        ]
        
        print(f"\n✅ After cleaning: {len(self.cleaned_df)} rows")
        return self.cleaned_df
    
    def save_cleaned_data(self, output_path='data/cleaned_housing_data.csv'):
        """Save the cleaned dataset"""
        if self.cleaned_df is not None:
            self.cleaned_df.to_csv(output_path, index=False)
            print(f"✅ Cleaned data saved to {output_path}")
        else:
            print("⚠️ No cleaned data to save. Run clean_data() first.")

# Example usage
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = DataPreprocessor('data/dataset.csv')  # Change to your filename
    
    # Load data
    preprocessor.load_data()
    
    # Explore data
    preprocessor.explore_data()
    
    # Clean data - UPDATE THESE COLUMN NAMES BASED ON YOUR DATASET
    cleaned_df = preprocessor.clean_data(
        bedroom_col='bedrooms',  # Change to your bedroom column name
        bathroom_col='bathrooms',  # Change to your bathroom column name
        area_col='area',  # Change to your area column name
        price_col='price'  # Change to your price column name
    )
    
    # Save cleaned data
    preprocessor.save_cleaned_data()