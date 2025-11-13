"""
Data cleaning module for Telco Customer Churn dataset
Handles missing values, data type conversions, and standardization
"""

import pandas as pd
import numpy as np
from pathlib import Path


def clean_telco_data(df: pd.DataFrame, save_path: str = None) -> pd.DataFrame:
    """
    Clean the Telco Customer Churn dataset
    
    Cleaning steps:
    1. Handle TotalCharges column (convert string to numeric, handle nulls)
    2. Standardize SeniorCitizen column
    3. Handle "No internet service" and "No phone service" values
    4. Validate data quality
    
    Args:
        df: Raw DataFrame from load_telco_data()
        save_path: Path to save cleaned data (default: data/processed/telco_churn_cleaned.csv)
    
    Returns:
        Cleaned DataFrame
    """
    print("[INFO] Starting data cleaning...")
    original_shape = df.shape
    print(f"[INFO] Original shape: {original_shape}")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Step 1: Handle TotalCharges column
    print("\n[INFO] Step 1: Handling TotalCharges column...")
    print(f"  TotalCharges dtype: {df_clean['TotalCharges'].dtype}")
    print(f"  TotalCharges sample values: {df_clean['TotalCharges'].head(10).tolist()}")
    
    # Convert to numeric, coercing errors to NaN
    df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'], errors='coerce')
    
    # Count nulls (these are the empty strings that couldn't be converted)
    null_count = df_clean['TotalCharges'].isna().sum()
    print(f"  Found {null_count} null values in TotalCharges")
    
    # Drop rows with null TotalCharges (only 11 rows, 0.16% of data)
    if null_count > 0:
        df_clean = df_clean.dropna(subset=['TotalCharges'])
        print(f"  Dropped {null_count} rows with null TotalCharges")
    
    # Step 2: Standardize SeniorCitizen column
    print("\n[INFO] Step 2: Standardizing SeniorCitizen column...")
    print(f"  Current values: {df_clean['SeniorCitizen'].unique()}")
    # Keep as binary (0/1) for modeling - it's already in the right format
    print(f"  Keeping SeniorCitizen as binary (0/1) for modeling")
    
    # Step 3: Handle "No internet service" and "No phone service"
    print("\n[INFO] Step 3: Handling 'No internet service' and 'No phone service'...")
    
    # Columns that may contain "No internet service"
    internet_service_columns = [
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies'
    ]
    
    # Columns that may contain "No phone service"
    phone_service_columns = ['MultipleLines']
    
    # Replace "No internet service" with "No"
    for col in internet_service_columns:
        if col in df_clean.columns:
            before = (df_clean[col] == 'No internet service').sum()
            df_clean[col] = df_clean[col].replace('No internet service', 'No')
            after = (df_clean[col] == 'No internet service').sum()
            if before > 0:
                print(f"  {col}: Replaced {before} 'No internet service' with 'No'")
    
    # Replace "No phone service" with "No"
    for col in phone_service_columns:
        if col in df_clean.columns:
            before = (df_clean[col] == 'No phone service').sum()
            df_clean[col] = df_clean[col].replace('No phone service', 'No')
            after = (df_clean[col] == 'No phone service').sum()
            if before > 0:
                print(f"  {col}: Replaced {before} 'No phone service' with 'No'")
    
    # Step 4: Validate data quality
    print("\n[INFO] Step 4: Validating data quality...")
    
    # Check for remaining nulls
    nulls_per_column = df_clean.isnull().sum()
    if nulls_per_column.sum() > 0:
        print(f"  WARNING: Found nulls in columns:")
        for col, count in nulls_per_column[nulls_per_column > 0].items():
            print(f"    {col}: {count} nulls")
    else:
        print("  ✓ No null values remaining")
    
    # Check for duplicates
    duplicates = df_clean.duplicated().sum()
    if duplicates > 0:
        print(f"  WARNING: Found {duplicates} duplicate rows")
    else:
        print("  ✓ No duplicate rows")
    
    # Check data types
    print(f"\n  Data types:")
    print(f"    Numeric columns: {df_clean.select_dtypes(include=[np.number]).columns.tolist()}")
    print(f"    Categorical columns: {df_clean.select_dtypes(include=['object']).columns.tolist()}")
    
    # Check value ranges for numeric columns
    print(f"\n  Numeric column ranges:")
    for col in df_clean.select_dtypes(include=[np.number]).columns:
        min_val = df_clean[col].min()
        max_val = df_clean[col].max()
        print(f"    {col}: {min_val} to {max_val}")
    
    # Final shape
    final_shape = df_clean.shape
    print(f"\n[INFO] Final shape: {final_shape}")
    print(f"[INFO] Removed {original_shape[0] - final_shape[0]} rows")
    
    # Save cleaned data
    if save_path is None:
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        save_path = processed_dir / "telco_churn_cleaned.csv"
    
    df_clean.to_csv(save_path, index=False)
    print(f"[SUCCESS] Saved cleaned data to: {save_path}")
    
    return df_clean


if __name__ == "__main__":
    # Test the cleaner
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from data.data_loader import load_telco_data
    
    print("=" * 60)
    print("Testing Data Cleaning Pipeline")
    print("=" * 60)
    
    # Load data
    df_raw = load_telco_data()
    
    # Clean data
    df_clean = clean_telco_data(df_raw)
    
    print(f"\n[SUCCESS] Cleaning complete!")
    print(f"  Original: {df_raw.shape}")
    print(f"  Cleaned: {df_clean.shape}")

