"""
Demographic feature engineering for Telco Customer Churn
Creates 6 demographic features from customer attributes
"""

import pandas as pd
import numpy as np


def engineer_demographic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer demographic features from customer data
    
    Creates:
    - is_senior: Binary (0/1) from SeniorCitizen
    - has_partner: Binary (0/1) from Partner
    - has_dependents: Binary (0/1) from Dependents
    - is_male: Binary (0/1) from gender
    - family_size: Integer (1-3) = 1 + has_partner + has_dependents
    - household_type: Categorical ('single', 'couple', 'family')
    
    Args:
        df: DataFrame with original customer data
    
    Returns:
        DataFrame with demographic features added
    """
    print("[INFO] Engineering demographic features...")
    
    df_features = df.copy()
    
    # 1. is_senior: Convert SeniorCitizen to boolean (keep as 0/1)
    df_features['is_senior'] = df_features['SeniorCitizen'].astype(int)
    print(f"  Created is_senior: {df_features['is_senior'].sum()} seniors")
    
    # 2. has_partner: Convert Partner 'Yes'/'No' to 1/0
    df_features['has_partner'] = (df_features['Partner'] == 'Yes').astype(int)
    print(f"  Created has_partner: {df_features['has_partner'].sum()} with partner")
    
    # 3. has_dependents: Convert Dependents 'Yes'/'No' to 1/0
    df_features['has_dependents'] = (df_features['Dependents'] == 'Yes').astype(int)
    print(f"  Created has_dependents: {df_features['has_dependents'].sum()} with dependents")
    
    # 4. is_male: Convert gender to binary (Male=1, Female=0)
    df_features['is_male'] = (df_features['gender'] == 'Male').astype(int)
    print(f"  Created is_male: {df_features['is_male'].sum()} males")
    
    # 5. family_size: Calculate as 1 (self) + has_partner + has_dependents
    df_features['family_size'] = 1 + df_features['has_partner'] + df_features['has_dependents']
    print(f"  Created family_size: range {df_features['family_size'].min()}-{df_features['family_size'].max()}")
    print(f"    Distribution: {df_features['family_size'].value_counts().sort_index().to_dict()}")
    
    # 6. household_type: Categorize as 'single', 'couple', or 'family'
    def get_household_type(row):
        if row['has_dependents'] == 1:
            return 'family'
        elif row['has_partner'] == 1:
            return 'couple'
        else:
            return 'single'
    
    df_features['household_type'] = df_features.apply(get_household_type, axis=1)
    print(f"  Created household_type:")
    print(f"    Distribution: {df_features['household_type'].value_counts().to_dict()}")
    
    print(f"[SUCCESS] Created 6 demographic features")
    
    return df_features

