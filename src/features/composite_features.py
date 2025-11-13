"""
Composite feature engineering for Telco Customer Churn
Creates 4 composite risk and satisfaction features
"""

import pandas as pd
import numpy as np


def engineer_composite_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer composite risk and satisfaction features
    
    Creates:
    - high_risk_profile: True if ALL: monthly_contract + electronic_check + <3 services + <12 tenure
    - service_satisfaction_score: Composite score (0-1) based on services
    - contract_value_ratio: Contract length vs monthly charges
    - churn_likelihood_segment: Categorical ('Very High', 'High', 'Medium', 'Low')
    
    Args:
        df: DataFrame with all engineered features
    
    Returns:
        DataFrame with composite features added
    """
    print("[INFO] Engineering composite features...")
    
    df_features = df.copy()
    
    # 1. high_risk_profile: True if ALL conditions met
    df_features['high_risk_profile'] = (
        (df_features['is_monthly_contract'] == 1) &
        (df_features['PaymentMethod'] == 'Electronic check') &
        (df_features['total_services'] < 3) &
        (df_features['tenure_months'] < 12)
    ).astype(int)
    print(f"  high_risk_profile: {df_features['high_risk_profile'].sum()} high-risk customers")
    
    # 2. service_satisfaction_score: Composite score (0-1)
    score = np.zeros(len(df_features))
    
    # Internet type contribution
    score += (df_features['internet_type'] == 'Fiber optic').astype(int) * 0.2
    score += (df_features['internet_type'] == 'DSL').astype(int) * 0.1
    
    # Security services (0-3 services, max 0.3)
    score += (df_features['security_services_count'] / 3) * 0.3
    
    # Streaming services (0-2 services, max 0.2)
    score += (df_features['streaming_services_count'] / 2) * 0.2
    
    # Tech support
    score += df_features['has_tech_support'] * 0.15
    
    # Service penetration (0-1, max 0.15)
    score += df_features['service_penetration_rate'] * 0.15
    
    # Ensure score is in 0-1 range
    df_features['service_satisfaction_score'] = np.clip(score, 0, 1)
    print(f"  service_satisfaction_score: range {df_features['service_satisfaction_score'].min():.2f}-{df_features['service_satisfaction_score'].max():.2f}")
    print(f"    Mean: {df_features['service_satisfaction_score'].mean():.2f}")
    
    # 3. contract_value_ratio: Contract length vs monthly charges
    contract_length_months = {
        'Month-to-month': 1,
        'One year': 12,
        'Two year': 24
    }
    
    df_features['contract_length_months'] = df_features['Contract'].map(contract_length_months)
    
    # Ratio = contract_length / (monthly_charges / 10)
    # Higher ratio = better value proposition
    df_features['contract_value_ratio'] = np.where(
        df_features['monthly_charges'] > 0,
        df_features['contract_length_months'] / (df_features['monthly_charges'] / 10),
        0
    )
    print(f"  contract_value_ratio: range {df_features['contract_value_ratio'].min():.2f}-{df_features['contract_value_ratio'].max():.2f}")
    
    # 4. churn_likelihood_segment: Based on historical patterns
    def get_churn_segment(row):
        # Very High: monthly_contract AND tenure < 12 AND fiber_optic
        if (row['is_monthly_contract'] == 1 and 
            row['tenure_months'] < 12 and 
            row['internet_type'] == 'Fiber optic'):
            return 'Very High'
        
        # High: monthly_contract AND (tenure < 24 OR electronic_check)
        elif (row['is_monthly_contract'] == 1 and 
              (row['tenure_months'] < 24 or row['PaymentMethod'] == 'Electronic check')):
            return 'High'
        
        # Medium: monthly_contract OR tenure < 12
        elif (row['is_monthly_contract'] == 1 or row['tenure_months'] < 12):
            return 'Medium'
        
        # Low: long contract (1-2 year) AND tenure > 24
        else:
            return 'Low'
    
    df_features['churn_likelihood_segment'] = df_features.apply(get_churn_segment, axis=1)
    print(f"  churn_likelihood_segment distribution:")
    print(f"    {df_features['churn_likelihood_segment'].value_counts().to_dict()}")
    
    print(f"[SUCCESS] Created 4 composite features")
    
    return df_features

