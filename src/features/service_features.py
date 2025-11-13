"""
Service feature engineering for Telco Customer Churn
Creates 15 service-related features
"""

import pandas as pd
import numpy as np


def engineer_service_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer service features from customer service subscriptions
    
    Creates:
    - has_phone_service: Binary flag
    - has_multiple_lines: Binary flag
    - has_internet: Binary flag (InternetService != 'No')
    - internet_type: Categorical ('DSL', 'Fiber optic', 'No')
    - has_online_security: Binary flag
    - has_online_backup: Binary flag
    - has_device_protection: Binary flag
    - has_tech_support: Binary flag
    - has_streaming_tv: Binary flag
    - has_streaming_movies: Binary flag
    - total_services: Count of all services (0-9)
    - security_services_count: Count of security services
    - streaming_services_count: Count of streaming services
    - service_penetration_rate: total_services / 9
    - has_premium_internet: True if Fiber optic
    
    Args:
        df: DataFrame with customer data
    
    Returns:
        DataFrame with service features added
    """
    print("[INFO] Engineering service features...")
    
    df_features = df.copy()
    
    # 1. has_phone_service: Convert PhoneService to binary
    df_features['has_phone_service'] = (df_features['PhoneService'] == 'Yes').astype(int)
    print(f"  has_phone_service: {df_features['has_phone_service'].sum()} customers")
    
    # 2. has_multiple_lines: True if MultipleLines == 'Yes'
    df_features['has_multiple_lines'] = (df_features['MultipleLines'] == 'Yes').astype(int)
    print(f"  has_multiple_lines: {df_features['has_multiple_lines'].sum()} customers")
    
    # 3. has_internet: True if InternetService != 'No'
    df_features['has_internet'] = (df_features['InternetService'] != 'No').astype(int)
    print(f"  has_internet: {df_features['has_internet'].sum()} customers")
    
    # 4. internet_type: Keep as categorical
    df_features['internet_type'] = df_features['InternetService']
    print(f"  internet_type distribution:")
    print(f"    {df_features['internet_type'].value_counts().to_dict()}")
    
    # 5-9. Security and streaming services (Yes=1, No/No internet=0)
    security_services = {
        'has_online_security': 'OnlineSecurity',
        'has_online_backup': 'OnlineBackup',
        'has_device_protection': 'DeviceProtection',
        'has_tech_support': 'TechSupport',
    }
    
    streaming_services = {
        'has_streaming_tv': 'StreamingTV',
        'has_streaming_movies': 'StreamingMovies',
    }
    
    for feature_name, column_name in security_services.items():
        df_features[feature_name] = (df_features[column_name] == 'Yes').astype(int)
        print(f"  {feature_name}: {df_features[feature_name].sum()} customers")
    
    for feature_name, column_name in streaming_services.items():
        df_features[feature_name] = (df_features[column_name] == 'Yes').astype(int)
        print(f"  {feature_name}: {df_features[feature_name].sum()} customers")
    
    # 10. total_services: Sum of all service flags (0-9)
    service_columns = [
        'has_phone_service',
        'has_multiple_lines',
        'has_internet',
        'has_online_security',
        'has_online_backup',
        'has_device_protection',
        'has_tech_support',
        'has_streaming_tv',
        'has_streaming_movies',
    ]
    
    df_features['total_services'] = df_features[service_columns].sum(axis=1)
    print(f"  total_services: range {df_features['total_services'].min()}-{df_features['total_services'].max()}")
    print(f"    Mean: {df_features['total_services'].mean():.2f}")
    
    # 11. security_services_count: Sum of security services
    security_columns = ['has_online_security', 'has_online_backup', 'has_device_protection']
    df_features['security_services_count'] = df_features[security_columns].sum(axis=1)
    print(f"  security_services_count: range {df_features['security_services_count'].min()}-{df_features['security_services_count'].max()}")
    
    # 12. streaming_services_count: Sum of streaming services
    streaming_columns = ['has_streaming_tv', 'has_streaming_movies']
    df_features['streaming_services_count'] = df_features[streaming_columns].sum(axis=1)
    print(f"  streaming_services_count: range {df_features['streaming_services_count'].min()}-{df_features['streaming_services_count'].max()}")
    
    # 13. service_penetration_rate: total_services / 9 (max possible)
    df_features['service_penetration_rate'] = df_features['total_services'] / 9
    print(f"  service_penetration_rate: range {df_features['service_penetration_rate'].min():.2f}-{df_features['service_penetration_rate'].max():.2f}")
    
    # 14. has_premium_internet: True if Fiber optic
    df_features['has_premium_internet'] = (df_features['InternetService'] == 'Fiber optic').astype(int)
    print(f"  has_premium_internet: {df_features['has_premium_internet'].sum()} customers")
    
    print(f"[SUCCESS] Created 15 service features")
    
    return df_features

