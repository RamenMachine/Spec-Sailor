"""
Data loader for Telco Customer Churn dataset
Downloads and loads the Kaggle Telco Customer Churn dataset
"""

import pandas as pd
import os
from pathlib import Path


def load_telco_data(url: str = None, save_path: str = None) -> pd.DataFrame:
    """
    Download and load Telco Customer Churn dataset from Kaggle
    
    Args:
        url: URL to download dataset from (default: Kaggle dataset URL)
        save_path: Path to save raw data (default: data/raw/telco_churn_raw.csv)
    
    Returns:
        DataFrame with raw Telco customer data
    """
    if url is None:
        url = "https://raw.githubusercontent.com/carlosfab/dsnp2/master/datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    
    if save_path is None:
        # Create data/raw directory if it doesn't exist
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        save_path = raw_dir / "telco_churn_raw.csv"
    
    print(f"[INFO] Downloading Telco Customer Churn dataset from: {url}")
    
    try:
        # Download and load the dataset
        df = pd.read_csv(url)
        
        print(f"[INFO] Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        print(f"[INFO] Columns: {list(df.columns)}")
        
        # Save to local file
        df.to_csv(save_path, index=False)
        print(f"[INFO] Saved raw data to: {save_path}")
        
        # Display basic info
        print(f"\n[INFO] Dataset Shape: {df.shape}")
        print(f"[INFO] Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        print(f"[INFO] Duplicate rows: {duplicates}")
        
        # Display first few rows
        print(f"\n[INFO] First 5 rows:")
        print(df.head())
        
        # Display unique values for categorical columns
        print(f"\n[INFO] Unique values per categorical column:")
        for col in df.select_dtypes(include=['object']).columns:
            unique_count = df[col].nunique()
            print(f"  {col}: {unique_count} unique values")
            if unique_count <= 10:
                print(f"    Values: {df[col].unique().tolist()}")
        
        return df
        
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        raise


if __name__ == "__main__":
    # Test the loader
    df = load_telco_data()
    print(f"\n[SUCCESS] Loaded {len(df)} customers from Telco dataset")

