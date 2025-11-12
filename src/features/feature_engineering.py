"""
Feature Engineering Pipeline
Main pipeline that orchestrates all feature calculations and creates final dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from typing import Tuple

from engagement_features import calculate_all_users_engagement
from islamic_calendar_features import calculate_all_users_islamic
from content_features import calculate_all_users_content


def calculate_social_features(user_id: str, total_events: int) -> dict:
    """
    Calculate social features (simulated for demo)
    In production, these would come from real social interaction data

    Args:
        user_id: User identifier
        total_events: Total number of events for the user

    Returns:
        Dictionary with 4 social features
    """
    # Simulate based on engagement level
    np.random.seed(hash(user_id) % 2**32)  # Deterministic per user

    if total_events > 100:
        friends_count = int(np.random.exponential(20))
        shares_sent = int(np.random.exponential(10))
        comments_made = int(np.random.exponential(8))
    elif total_events > 20:
        friends_count = int(np.random.exponential(5))
        shares_sent = int(np.random.exponential(2))
        comments_made = int(np.random.exponential(1))
    else:
        friends_count = 0
        shares_sent = 0
        comments_made = 0

    # Days since last social (random between 0-30)
    days_since_last_social = np.random.randint(0, min(31, total_events + 1))

    return {
        'friends_count': min(500, friends_count),
        'shares_sent': min(200, shares_sent),
        'comments_made': min(300, comments_made),
        'days_since_last_social': days_since_last_social
    }


def engineer_all_features(
    as_of_date: datetime = datetime(2024, 11, 10),
    data_dir: str = 'data',
    verbose: bool = True
) -> pd.DataFrame:
    """
    Complete feature engineering pipeline

    Args:
        as_of_date: Date to calculate features as of
        data_dir: Base directory for data files
        verbose: Whether to print progress

    Returns:
        DataFrame with all engineered features
    """
    print("=" * 60)
    print("BARAKAH RETAIN - FEATURE ENGINEERING PIPELINE")
    print("=" * 60)

    # Load data
    print("\n[1/7] Loading data...")
    events_path = os.path.join(data_dir, 'raw', 'sample_events.csv')
    profiles_path = os.path.join(data_dir, 'raw', 'sample_profiles.csv')

    events_df = pd.read_csv(events_path, parse_dates=['event_timestamp'])
    profiles_df = pd.read_csv(profiles_path, parse_dates=['signup_date', 'last_active'])

    print(f"  Loaded {len(profiles_df)} users and {len(events_df)} events")

    # Get list of all users
    all_users = profiles_df['user_id'].tolist()

    # Calculate engagement features (10 features)
    print(f"\n[2/7] Calculating engagement features...")
    engagement_features = calculate_all_users_engagement(
        events_df, all_users, as_of_date, verbose=verbose
    )

    # Calculate Islamic calendar features (8 features)
    print(f"\n[3/7] Calculating Islamic calendar features...")
    islamic_features = calculate_all_users_islamic(
        events_df, profiles_df, all_users, as_of_date, verbose=verbose
    )

    # Calculate content features (10 features)
    print(f"\n[4/7] Calculating content features...")
    content_features = calculate_all_users_content(
        events_df, all_users, verbose=verbose
    )

    # Calculate social features (4 features)
    print(f"\n[5/7] Calculating social features...")
    social_features_list = []
    event_counts = events_df.groupby('user_id').size()

    for i, user_id in enumerate(all_users):
        if verbose and (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1}/{len(all_users)} users...")

        total_events = event_counts.get(user_id, 0)
        social_feats = calculate_social_features(user_id, total_events)
        social_feats['user_id'] = user_id
        social_features_list.append(social_feats)

    social_features = pd.DataFrame(social_features_list)

    # Merge all features
    print(f"\n[6/7] Merging all features...")
    features_df = engagement_features.copy()
    features_df = features_df.merge(islamic_features, on='user_id', how='left')
    features_df = features_df.merge(content_features, on='user_id', how='left')
    features_df = features_df.merge(social_features, on='user_id', how='left')

    # Add profile features
    features_df = features_df.merge(
        profiles_df[['user_id', 'signup_date', 'subscription_type', 'location', 'is_churned']],
        on='user_id',
        how='left'
    )

    # Calculate days_since_signup
    features_df['days_since_signup'] = (
        as_of_date - features_df['signup_date']
    ).dt.days

    # Handle categorical variables
    print(f"\n[7/7] Encoding categorical variables...")

    # One-hot encode favorite_content_type
    content_dummies = pd.get_dummies(
        features_df['favorite_content_type'],
        prefix='content'
    )
    features_df = pd.concat([features_df, content_dummies], axis=1)

    # One-hot encode subscription_type
    subscription_dummies = pd.get_dummies(
        features_df['subscription_type'],
        prefix='subscription'
    )
    features_df = pd.concat([features_df, subscription_dummies], axis=1)

    # One-hot encode location
    location_dummies = pd.get_dummies(
        features_df['location'],
        prefix='location'
    )
    features_df = pd.concat([features_df, location_dummies], axis=1)

    # Drop original categorical columns and signup_date
    features_df = features_df.drop([
        'favorite_content_type',
        'subscription_type',
        'location',
        'signup_date'
    ], axis=1)

    # Fill any remaining NaN values
    features_df = features_df.fillna(0)

    print(f"\n{'=' * 60}")
    print(f"FEATURE ENGINEERING COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total users: {len(features_df)}")
    print(f"Total features: {len(features_df.columns) - 2}")  # Exclude user_id and is_churned
    print(f"Churned users: {features_df['is_churned'].sum()} ({features_df['is_churned'].mean()*100:.1f}%)")
    print(f"Active users: {(~features_df['is_churned']).sum()} ({(~features_df['is_churned']).mean()*100:.1f}%)")

    return features_df


def save_features(
    features_df: pd.DataFrame,
    output_dir: str = 'data/processed',
    model_dir: str = 'data/models'
) -> Tuple[str, str]:
    """
    Save engineered features and feature configuration

    Args:
        features_df: DataFrame with all features
        output_dir: Directory to save processed data
        model_dir: Directory to save model artifacts

    Returns:
        Tuple of (features_path, config_path)
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # Save features
    features_path = os.path.join(output_dir, 'features.csv')
    features_df.to_csv(features_path, index=False)
    print(f"\nFeatures saved: {features_path}")

    # Save feature configuration
    feature_cols = [col for col in features_df.columns if col not in ['user_id', 'is_churned']]

    feature_config = {
        'feature_columns': feature_cols,
        'target_column': 'is_churned',
        'num_features': len(feature_cols),
        'categorical_features': [col for col in feature_cols if col.startswith(('content_', 'subscription_', 'location_'))],
        'numerical_features': [col for col in feature_cols if not col.startswith(('content_', 'subscription_', 'location_'))]
    }

    config_path = os.path.join(model_dir, 'feature_config.json')
    with open(config_path, 'w') as f:
        json.dump(feature_config, f, indent=2)
    print(f"Feature config saved: {config_path}")

    return features_path, config_path


if __name__ == "__main__":
    # Run the complete pipeline
    features_df = engineer_all_features(verbose=True)

    # Display sample
    print(f"\n{'-' * 60}")
    print("SAMPLE FEATURES (first 5 rows, first 15 columns):")
    print(f"{'-' * 60}")
    print(features_df.iloc[:5, :15])

    print(f"\n{'-' * 60}")
    print("FEATURE STATISTICS:")
    print(f"{'-' * 60}")
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns[:10]
    print(features_df[numeric_cols].describe())

    # Save features
    save_features(features_df)

    print(f"\n{'=' * 60}")
    print("Feature engineering pipeline completed successfully!")
    print(f"{'=' * 60}")
