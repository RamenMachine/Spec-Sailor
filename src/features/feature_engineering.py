"""
Master feature engineering pipeline for Telco Customer Churn
Orchestrates all feature engineering steps and one-hot encoding
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from features.demographic_features import engineer_demographic_features
from features.tenure_features import engineer_tenure_features
from features.service_features import engineer_service_features
from features.billing_features import engineer_billing_features
from features.composite_features import engineer_composite_features


def engineer_all_features(df: pd.DataFrame, save_path: str = None, save_config: bool = True) -> tuple[pd.DataFrame, pd.Series]:
    """
    Master feature engineering pipeline
    
    Steps:
    1. Engineer demographic features
    2. Engineer tenure features
    3. Engineer service features
    4. Engineer billing features
    5. Engineer composite features
    6. One-hot encode categorical variables
    7. Prepare target variable
    8. Drop original raw columns
    
    Args:
        df: Cleaned DataFrame from data_cleaner
        save_path: Path to save engineered features (default: data/processed/features_engineered.csv)
        save_config: Whether to save feature config JSON
    
    Returns:
        Tuple of (features_df, target_series)
    """
    print("=" * 60)
    print("FEATURE ENGINEERING PIPELINE")
    print("=" * 60)
    
    original_shape = df.shape
    print(f"\n[INFO] Starting with {original_shape[0]} customers, {original_shape[1]} columns")
    
    # Step 1-5: Engineer all feature groups
    print("\n[STEP 1] Engineering demographic features...")
    df_features = engineer_demographic_features(df)
    
    print("\n[STEP 2] Engineering tenure features...")
    df_features = engineer_tenure_features(df_features)
    
    print("\n[STEP 3] Engineering service features...")
    df_features = engineer_service_features(df_features)
    
    print("\n[STEP 4] Engineering billing features...")
    df_features = engineer_billing_features(df_features)
    
    print("\n[STEP 5] Engineering composite features...")
    df_features = engineer_composite_features(df_features)
    
    # Step 6: One-hot encode categorical variables
    print("\n[STEP 6] One-hot encoding categorical variables...")
    
    categorical_columns = [
        'household_type',      # 3 categories
        'tenure_group',         # 5 categories
        'internet_type',        # 3 categories
        'contract_type',        # 3 categories
        'payment_method',       # 4 categories
        'churn_likelihood_segment'  # 4 categories
    ]
    
    # Check which columns exist
    existing_categorical = [col for col in categorical_columns if col in df_features.columns]
    print(f"  Encoding {len(existing_categorical)} categorical columns: {existing_categorical}")
    
    # One-hot encode
    df_encoded = pd.get_dummies(
        df_features,
        columns=existing_categorical,
        prefix=existing_categorical,
        drop_first=False  # Keep all categories for interpretability
    )
    
    print(f"  After encoding: {df_encoded.shape[1]} columns")
    
    # Step 7: Prepare target variable
    print("\n[STEP 7] Preparing target variable...")
    if 'Churn' in df_encoded.columns:
        target = (df_encoded['Churn'] == 'Yes').astype(int)
        churn_rate = target.mean()
        print(f"  Target: Churn (Yes=1, No=0)")
        print(f"  Churn rate: {churn_rate:.1%}")
        print(f"  Non-churners: {(target == 0).sum()}, Churners: {(target == 1).sum()}")
    else:
        raise ValueError("Churn column not found in DataFrame")
    
    # Step 8: Drop original raw columns that were encoded
    print("\n[STEP 8] Dropping original raw columns...")
    
    columns_to_drop = [
        # Original demographic columns
        'gender', 'SeniorCitizen', 'Partner', 'Dependents',
        # Original service columns
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        # Original contract/billing columns
        'Contract', 'PaperlessBilling', 'PaymentMethod',
        # Original numeric columns (we have engineered versions)
        'tenure', 'MonthlyCharges', 'TotalCharges',
        # Target column (we have it as separate series)
        'Churn'
    ]
    
    # Only drop columns that exist
    existing_drop = [col for col in columns_to_drop if col in df_encoded.columns]
    df_final = df_encoded.drop(columns=existing_drop)
    
    print(f"  Dropped {len(existing_drop)} original columns")
    print(f"  Final feature count: {df_final.shape[1]}")
    
    # Keep customerID for tracking
    if 'customerID' in df_final.columns:
        customer_ids = df_final['customerID'].copy()
        df_final = df_final.drop(columns=['customerID'])
    else:
        customer_ids = None
    
    # Final shape
    final_shape = df_final.shape
    print(f"\n[INFO] Final shape: {final_shape}")
    print(f"  Features: {final_shape[1]}")
    print(f"  Samples: {final_shape[0]}")
    
    # Save feature config
    if save_config:
        config_path = Path("data/models/feature_config.json")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        feature_config = {
            'total_features': final_shape[1],
            'feature_names': df_final.columns.tolist(),
            'categorical_encoded': existing_categorical,
            'target_name': 'Churn',
            'churn_rate': float(churn_rate),
            'sample_count': int(final_shape[0])
        }
        
        with open(config_path, 'w') as f:
            json.dump(feature_config, f, indent=2)
        
        print(f"\n[INFO] Saved feature config to: {config_path}")
    
    # Save engineered features
    if save_path is None:
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        save_path = processed_dir / "features_engineered.csv"
    
    # Add customerID and target back for saving
    df_to_save = df_final.copy()
    if customer_ids is not None:
        df_to_save.insert(0, 'customerID', customer_ids)
    df_to_save['Churn'] = target.values
    
    df_to_save.to_csv(save_path, index=False)
    print(f"[SUCCESS] Saved engineered features to: {save_path}")
    
    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 60)
    
    return df_final, target

