"""
Billing and contract feature engineering for Telco Customer Churn
Creates 12 billing-related features
"""

import pandas as pd
import numpy as np


def engineer_billing_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer billing and contract features
    
    Creates:
    - contract_type: Keep original (Month-to-month, One year, Two year)
    - is_monthly_contract: True if Month-to-month
    - has_paperless_billing: Binary flag
    - payment_method: Keep original 4 categories
    - is_electronic_payment: True if electronic/automatic payment
    - is_manual_payment: True if Mailed check
    - monthly_charges: Already exists
    - total_charges: Already exists
    - charges_per_service: MonthlyCharges / total_services
    - is_high_value_customer: True if MonthlyCharges > 80
    - payment_reliability_score: Based on payment method (0.6-1.0)
    - billing_risk_score: Composite risk score (0-1)
    
    Args:
        df: DataFrame with customer data
    
    Returns:
        DataFrame with billing features added
    """
    print("[INFO] Engineering billing features...")
    
    df_features = df.copy()
    
    # 1. contract_type: Keep original
    df_features['contract_type'] = df_features['Contract']
    print(f"  contract_type distribution:")
    print(f"    {df_features['contract_type'].value_counts().to_dict()}")
    
    # 2. is_monthly_contract: True if Month-to-month
    df_features['is_monthly_contract'] = (df_features['Contract'] == 'Month-to-month').astype(int)
    print(f"  is_monthly_contract: {df_features['is_monthly_contract'].sum()} customers")
    
    # 3. has_paperless_billing: Convert to binary
    df_features['has_paperless_billing'] = (df_features['PaperlessBilling'] == 'Yes').astype(int)
    print(f"  has_paperless_billing: {df_features['has_paperless_billing'].sum()} customers")
    
    # 4. payment_method: Keep original
    df_features['payment_method'] = df_features['PaymentMethod']
    print(f"  payment_method distribution:")
    print(f"    {df_features['payment_method'].value_counts().to_dict()}")
    
    # 5. is_electronic_payment: True if electronic/automatic
    electronic_methods = [
        'Electronic check',
        'Bank transfer (automatic)',
        'Credit card (automatic)'
    ]
    df_features['is_electronic_payment'] = df_features['PaymentMethod'].isin(electronic_methods).astype(int)
    print(f"  is_electronic_payment: {df_features['is_electronic_payment'].sum()} customers")
    
    # 6. is_manual_payment: True if Mailed check
    df_features['is_manual_payment'] = (df_features['PaymentMethod'] == 'Mailed check').astype(int)
    print(f"  is_manual_payment: {df_features['is_manual_payment'].sum()} customers")
    
    # 7. monthly_charges: Already exists, ensure numeric
    df_features['monthly_charges'] = pd.to_numeric(df_features['MonthlyCharges'], errors='coerce')
    print(f"  monthly_charges: range ${df_features['monthly_charges'].min():.2f}-${df_features['monthly_charges'].max():.2f}")
    
    # 8. total_charges: Already exists, ensure numeric
    df_features['total_charges'] = pd.to_numeric(df_features['TotalCharges'], errors='coerce')
    print(f"  total_charges: range ${df_features['total_charges'].min():.2f}-${df_features['total_charges'].max():.2f}")
    
    # 9. charges_per_service: MonthlyCharges / total_services
    # Handle division by zero (no services)
    df_features['charges_per_service'] = np.where(
        df_features['total_services'] > 0,
        df_features['monthly_charges'] / df_features['total_services'],
        0
    )
    print(f"  charges_per_service: range ${df_features['charges_per_service'].min():.2f}-${df_features['charges_per_service'].max():.2f}")
    
    # 10. is_high_value_customer: True if MonthlyCharges > 80 (top quartile)
    df_features['is_high_value_customer'] = (df_features['monthly_charges'] > 80).astype(int)
    print(f"  is_high_value_customer: {df_features['is_high_value_customer'].sum()} customers")
    
    # 11. payment_reliability_score: Based on payment method
    def get_payment_reliability(payment_method):
        if payment_method == 'Bank transfer (automatic)':
            return 1.0  # Most reliable
        elif payment_method == 'Credit card (automatic)':
            return 0.95
        elif payment_method == 'Mailed check':
            return 0.75
        elif payment_method == 'Electronic check':
            return 0.6  # Highest churn
        else:
            return 0.7  # Default
    
    df_features['payment_reliability_score'] = df_features['PaymentMethod'].apply(get_payment_reliability)
    print(f"  payment_reliability_score: range {df_features['payment_reliability_score'].min():.2f}-{df_features['payment_reliability_score'].max():.2f}")
    
    # 12. billing_risk_score: Composite risk score
    # risk = 0
    # if paperless: +0.3
    # if electronic_check: +0.5
    # if monthly_contract: +0.4
    # Normalize to 0-1
    risk = np.zeros(len(df_features))
    risk += df_features['has_paperless_billing'] * 0.3
    risk += (df_features['PaymentMethod'] == 'Electronic check').astype(int) * 0.5
    risk += df_features['is_monthly_contract'] * 0.4
    
    # Normalize to 0-1 range (max possible is 1.2)
    df_features['billing_risk_score'] = risk / 1.2
    print(f"  billing_risk_score: range {df_features['billing_risk_score'].min():.2f}-{df_features['billing_risk_score'].max():.2f}")
    print(f"    Mean: {df_features['billing_risk_score'].mean():.2f}")
    
    print(f"[SUCCESS] Created 12 billing features")
    
    return df_features

