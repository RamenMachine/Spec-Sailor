"""
Tenure and lifecycle feature engineering for Telco Customer Churn
Creates 8 tenure-related features
"""

import pandas as pd
import numpy as np


def engineer_tenure_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer tenure and lifecycle features
    
    Creates:
    - tenure_months: Already exists (0-72)
    - tenure_years: tenure_months / 12
    - tenure_group: Binned tenure ('0-6', '7-12', '13-24', '25-48', '49+')
    - is_new_customer: True if tenure <= 6 months
    - customer_lifetime_ratio: TotalCharges / (MonthlyCharges * tenure_months)
    - avg_monthly_spend: TotalCharges / tenure_months
    - early_lifecycle_risk: tenure < 12 AND Month-to-month contract
    - tenure_contract_mismatch: Unusual tenure/contract patterns
    
    Args:
        df: DataFrame with customer data
    
    Returns:
        DataFrame with tenure features added
    """
    print("[INFO] Engineering tenure features...")
    
    df_features = df.copy()
    
    # 1. tenure_months: Already exists, ensure it's numeric
    df_features['tenure_months'] = pd.to_numeric(df_features['tenure'], errors='coerce')
    print(f"  tenure_months: range {df_features['tenure_months'].min()}-{df_features['tenure_months'].max()}")
    
    # 2. tenure_years: tenure_months / 12, rounded to 1 decimal
    df_features['tenure_years'] = (df_features['tenure_months'] / 12).round(1)
    print(f"  tenure_years: range {df_features['tenure_years'].min()}-{df_features['tenure_years'].max()}")
    
    # 3. tenure_group: Bin tenure into categories
    def get_tenure_group(tenure):
        if tenure <= 6:
            return '0-6 months'
        elif tenure <= 12:
            return '7-12 months'
        elif tenure <= 24:
            return '13-24 months'
        elif tenure <= 48:
            return '25-48 months'
        else:
            return '49+ months'
    
    df_features['tenure_group'] = df_features['tenure_months'].apply(get_tenure_group)
    print(f"  tenure_group distribution:")
    print(f"    {df_features['tenure_group'].value_counts().to_dict()}")
    
    # 4. is_new_customer: True if tenure <= 6 months
    df_features['is_new_customer'] = (df_features['tenure_months'] <= 6).astype(int)
    print(f"  is_new_customer: {df_features['is_new_customer'].sum()} new customers")
    
    # 5. customer_lifetime_ratio: TotalCharges / (MonthlyCharges * tenure_months)
    # Should be close to 1.0 for consistent payers
    # Handle division by zero (tenure=0)
    denominator = df_features['MonthlyCharges'] * df_features['tenure_months']
    df_features['customer_lifetime_ratio'] = np.where(
        denominator > 0,
        df_features['TotalCharges'] / denominator,
        0
    )
    print(f"  customer_lifetime_ratio: range {df_features['customer_lifetime_ratio'].min():.2f}-{df_features['customer_lifetime_ratio'].max():.2f}")
    print(f"    Mean: {df_features['customer_lifetime_ratio'].mean():.2f}")
    
    # 6. avg_monthly_spend: TotalCharges / tenure_months
    # Should equal MonthlyCharges for consistent billing
    df_features['avg_monthly_spend'] = np.where(
        df_features['tenure_months'] > 0,
        df_features['TotalCharges'] / df_features['tenure_months'],
        df_features['MonthlyCharges']  # For tenure=0, use current monthly charge
    )
    print(f"  avg_monthly_spend: range ${df_features['avg_monthly_spend'].min():.2f}-${df_features['avg_monthly_spend'].max():.2f}")
    
    # 7. early_lifecycle_risk: tenure < 12 AND Month-to-month contract
    df_features['early_lifecycle_risk'] = (
        (df_features['tenure_months'] < 12) & 
        (df_features['Contract'] == 'Month-to-month')
    ).astype(int)
    print(f"  early_lifecycle_risk: {df_features['early_lifecycle_risk'].sum()} high-risk customers")
    
    # 8. tenure_contract_mismatch: Unusual patterns
    # Short tenure with long contract OR long tenure with short contract
    df_features['tenure_contract_mismatch'] = (
        ((df_features['tenure_months'] < 12) & (df_features['Contract'] == 'Two year')) |
        ((df_features['tenure_months'] > 24) & (df_features['Contract'] == 'Month-to-month'))
    ).astype(int)
    print(f"  tenure_contract_mismatch: {df_features['tenure_contract_mismatch'].sum()} mismatched customers")
    
    print(f"[SUCCESS] Created 8 tenure features")
    
    return df_features

