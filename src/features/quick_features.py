"""
Optimized Feature Engineering for Quick Iteration
Processes a sample of users for rapid development
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from engagement_features import calculate_engagement_features
from islamic_calendar_features import calculate_islamic_features
from content_features import calculate_content_features

# Sample size for quick iteration
SAMPLE_SIZE = 5000  # Use 5000 users instead of 10000

def calculate_social_features_batch(events_df, user_ids):
    """Calculate social features for batch of users"""
    event_counts = events_df[events_df['user_id'].isin(user_ids)].groupby('user_id').size()

    features = []
    for user_id in user_ids:
        total_events = event_counts.get(user_id, 0)
        np.random.seed(hash(user_id) % 2**32)

        if total_events > 100:
            friends_count = min(500, int(np.random.exponential(20)))
            shares_sent = min(200, int(np.random.exponential(10)))
            comments_made = min(300, int(np.random.exponential(8)))
        elif total_events > 20:
            friends_count = min(500, int(np.random.exponential(5)))
            shares_sent = min(200, int(np.random.exponential(2)))
            comments_made = min(300, int(np.random.exponential(1)))
        else:
            friends_count = 0
            shares_sent = 0
            comments_made = 0

        features.append({
            'user_id': user_id,
            'friends_count': friends_count,
            'shares_sent': shares_sent,
            'comments_made': comments_made,
            'days_since_last_social': np.random.randint(0, min(31, total_events + 1))
        })

    return pd.DataFrame(features)


def quick_feature_engineering(sample_size=SAMPLE_SIZE):
    """Run optimized feature engineering on sample"""

    print("=" * 70)
    print("BARAKAH RETAIN - QUICK FEATURE ENGINEERING")
    print("=" * 70)

    # Load data
    print(f"\n[1/6] Loading data...")
    events_df = pd.read_csv('data/raw/sample_events.csv', parse_dates=['event_timestamp'])
    profiles_df = pd.read_csv('data/raw/sample_profiles.csv', parse_dates=['signup_date', 'last_active'])

    print(f"  Original: {len(profiles_df)} users, {len(events_df)} events")

    # Sample users (stratified by churn)
    churned = profiles_df[profiles_df['is_churned'] == True].sample(n=min(sample_size//10, len(profiles_df[profiles_df['is_churned'] == True])), random_state=42)
    active = profiles_df[profiles_df['is_churned'] == False].sample(n=min(sample_size - len(churned), len(profiles_df[profiles_df['is_churned'] == False])), random_state=42)

    sample_profiles = pd.concat([churned, active]).reset_index(drop=True)
    user_ids = sample_profiles['user_id'].tolist()

    # Filter events for sampled users
    sample_events = events_df[events_df['user_id'].isin(user_ids)].copy()

    print(f"  Sample: {len(sample_profiles)} users, {len(sample_events)} events")

    as_of_date = datetime(2024, 11, 10)

    # Calculate features
    print(f"\n[2/6] Engagement features...")
    engagement = []
    for i, uid in enumerate(user_ids):
        if (i + 1) % 1000 == 0:
            print(f"  {i + 1}/{len(user_ids)}")
        feats = calculate_engagement_features(sample_events, uid, as_of_date)
        feats['user_id'] = uid
        engagement.append(feats)
    engagement_df = pd.DataFrame(engagement)

    print(f"\n[3/6] Islamic calendar features...")
    islamic = []
    for i, uid in enumerate(user_ids):
        if (i + 1) % 1000 == 0:
            print(f"  {i + 1}/{len(user_ids)}")
        feats = calculate_islamic_features(sample_events, sample_profiles, uid, as_of_date)
        feats['user_id'] = uid
        islamic.append(feats)
    islamic_df = pd.DataFrame(islamic)

    print(f"\n[4/6] Content features...")
    content = []
    for i, uid in enumerate(user_ids):
        if (i + 1) % 1000 == 0:
            print(f"  {i + 1}/{len(user_ids)}")
        feats = calculate_content_features(sample_events, uid)
        feats['user_id'] = uid
        content.append(feats)
    content_df = pd.DataFrame(content)

    print(f"\n[5/6] Social features...")
    social_df = calculate_social_features_batch(sample_events, user_ids)

    print(f"\n[6/6] Merging and encoding...")
    # Merge all
    features_df = engagement_df.merge(islamic_df, on='user_id')
    features_df = features_df.merge(content_df, on='user_id')
    features_df = features_df.merge(social_df, on='user_id')
    features_df = features_df.merge(
        sample_profiles[['user_id', 'signup_date', 'subscription_type', 'location', 'is_churned']],
        on='user_id'
    )

    # Days since signup
    features_df['days_since_signup'] = (as_of_date - features_df['signup_date']).dt.days

    # One-hot encode
    content_dummies = pd.get_dummies(features_df['favorite_content_type'], prefix='content')
    subscription_dummies = pd.get_dummies(features_df['subscription_type'], prefix='subscription')
    location_dummies = pd.get_dummies(features_df['location'], prefix='location')

    features_df = pd.concat([features_df, content_dummies, subscription_dummies, location_dummies], axis=1)
    features_df = features_df.drop(['favorite_content_type', 'subscription_type', 'location', 'signup_date'], axis=1)
    features_df = features_df.fillna(0)

    print(f"\n{'=' * 70}")
    print(f"COMPLETE! {len(features_df)} users, {len(features_df.columns)-2} features")
    print(f"Churn rate: {features_df['is_churned'].mean()*100:.1f}%")
    print(f"{'=' * 70}")

    # Save
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/models', exist_ok=True)

    features_df.to_csv('data/processed/features.csv', index=False)

    feature_cols = [c for c in features_df.columns if c not in ['user_id', 'is_churned']]
    config = {
        'feature_columns': feature_cols,
        'target_column': 'is_churned',
        'num_features': len(feature_cols)
    }

    with open('data/models/feature_config.json', 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\nSaved: data/processed/features.csv")
    print(f"Saved: data/models/feature_config.json")

    return features_df


if __name__ == "__main__":
    features_df = quick_feature_engineering()
    print("\n✓ Feature engineering complete!")
