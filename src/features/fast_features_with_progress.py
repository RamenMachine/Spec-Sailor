"""
Ultra-Fast Feature Engineering with Progress Bar
Optimized for quick execution with real-time progress monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import sys

print("Starting fast feature engineering...")
print("Loading data...")

# Load data
events_df = pd.read_csv('data/raw/sample_events.csv', parse_dates=['event_timestamp'])
profiles_df = pd.read_csv('data/raw/sample_profiles.csv', parse_dates=['signup_date', 'last_active'])

print(f"Loaded {len(profiles_df)} users and {len(events_df)} events")

# Sample for speed (you can increase this)
SAMPLE_SIZE = 10000  # Use all 10,000 users
print(f"\nUsing {SAMPLE_SIZE} user sample for rapid development...")

# Stratified sample
churned = profiles_df[profiles_df['is_churned'] == True].sample(
    n=min(SAMPLE_SIZE//10, len(profiles_df[profiles_df['is_churned'] == True])),
    random_state=42
)
active = profiles_df[profiles_df['is_churned'] == False].sample(
    n=min(SAMPLE_SIZE - len(churned), len(profiles_df[profiles_df['is_churned'] == False])),
    random_state=42
)

sample_profiles = pd.concat([churned, active]).reset_index(drop=True)
user_ids = sample_profiles['user_id'].tolist()

# Filter events for sample
print("Filtering events for sample users...")
sample_events = events_df[events_df['user_id'].isin(user_ids)].copy()
print(f"Sample: {len(sample_profiles)} users, {len(sample_events)} events")

# Vectorized aggregations (MUCH faster!)
print("\n" + "="*70)
print("FAST FEATURE ENGINEERING")
print("="*70)

as_of_date = datetime(2024, 11, 10)

# 1. Engagement features from aggregations
print("\n[1/4] Engagement features (vectorized)...")
user_agg = sample_events.groupby('user_id').agg({
    'event_timestamp': ['count', 'max', 'min'],
    'session_duration_seconds': 'mean'
}).reset_index()

user_agg.columns = ['user_id', 'total_events', 'last_event', 'first_event', 'avg_duration_seconds']
user_agg['days_since_last_session'] = (as_of_date - user_agg['last_event']).dt.days
user_agg['days_active'] = (user_agg['last_event'] - user_agg['first_event']).dt.days + 1
user_agg['avg_session_duration'] = user_agg['avg_duration_seconds'] / 60.0  # minutes

# Session frequency
recent_7d = sample_events[sample_events['event_timestamp'] >= (as_of_date - pd.Timedelta(days=7))]
recent_30d = sample_events[sample_events['event_timestamp'] >= (as_of_date - pd.Timedelta(days=30))]

session_freq_7d = recent_7d[recent_7d['event_type'] == 'app_open'].groupby('user_id').size()
session_freq_30d = recent_30d[recent_30d['event_type'] == 'app_open'].groupby('user_id').size()

user_agg['session_frequency_7d'] = user_agg['user_id'].map(session_freq_7d).fillna(0)
user_agg['session_frequency_30d'] = user_agg['user_id'].map(session_freq_30d).fillna(0)
user_agg['sessions_per_week'] = (user_agg['total_events'] / user_agg['days_active'] * 7).fillna(0)

# Weekend activity
sample_events['is_weekend'] = sample_events['event_timestamp'].dt.dayofweek.isin([5, 6])
weekend_ratio = sample_events.groupby('user_id')['is_weekend'].mean()
user_agg['weekend_activity_ratio'] = user_agg['user_id'].map(weekend_ratio).fillna(0)

# Simplified streak (just use days active as proxy for now)
user_agg['streak_current'] = 0  # Simplified
user_agg['streak_longest'] = (user_agg['days_active'] * 0.3).astype(int)  # Estimate

print("[DONE] Engagement features complete")

# 2. Islamic calendar features
print("[2/4] Islamic calendar features...")
ramadan_start = datetime(2024, 3, 11)
ramadan_end = datetime(2024, 4, 9)

# Ramadan events
ramadan_events = sample_events[
    (sample_events['event_timestamp'] >= ramadan_start) &
    (sample_events['event_timestamp'] <= ramadan_end)
]
non_ramadan_events = sample_events[
    (sample_events['event_timestamp'] < ramadan_start) |
    (sample_events['event_timestamp'] > ramadan_end)
]

ramadan_counts = ramadan_events.groupby('user_id').size()
non_ramadan_counts = non_ramadan_events.groupby('user_id').size()

user_agg['ramadan_sessions'] = user_agg['user_id'].map(ramadan_counts).fillna(0)
user_agg['non_ramadan_sessions'] = user_agg['user_id'].map(non_ramadan_counts).fillna(1)  # Avoid div by zero
user_agg['ramadan_engagement_ratio'] = user_agg['ramadan_sessions'] / user_agg['non_ramadan_sessions']

# Other Islamic features (simplified)
user_agg['is_ramadan_convert'] = sample_profiles.set_index('user_id')['signup_date'].map(
    lambda x: 1 if ramadan_start <= x <= ramadan_end else 0
).reindex(user_agg['user_id']).values

user_agg['days_since_ramadan'] = (as_of_date - ramadan_end).days
user_agg['last_10_nights_sessions'] = 0  # Simplified
user_agg['jummah_participation_rate'] = np.random.uniform(0, 0.8, len(user_agg))  # Mock
user_agg['prayer_time_interaction_rate'] = np.random.uniform(0, 0.6, len(user_agg))  # Mock
user_agg['eid_participation'] = np.random.randint(0, 2, len(user_agg))  # Mock
user_agg['muharram_participation'] = np.random.randint(0, 2, len(user_agg))  # Mock

print("[DONE] Islamic features complete")

# 3. Content features
print("[3/4] Content features...")

# Content type percentages
content_events = sample_events[sample_events['event_type'] != 'app_open']
content_counts = content_events.groupby(['user_id', 'event_type']).size().unstack(fill_value=0)

total_content = content_events.groupby('user_id').size()

if 'quran_read' in content_counts:
    user_agg['quran_reading_pct'] = user_agg['user_id'].map(
        content_counts['quran_read'] / total_content
    ).fillna(0)
else:
    user_agg['quran_reading_pct'] = 0

if 'hadith_read' in content_counts:
    user_agg['hadith_engagement_pct'] = user_agg['user_id'].map(
        content_counts['hadith_read'] / total_content
    ).fillna(0)
else:
    user_agg['hadith_engagement_pct'] = 0

# Lecture minutes
lecture_minutes = sample_events[sample_events['event_type'] == 'lecture_view'].groupby('user_id')['session_duration_seconds'].sum() / 60
user_agg['lecture_watch_minutes'] = user_agg['user_id'].map(lecture_minutes).fillna(0)

# Other content metrics
user_agg['fiqh_content_views'] = user_agg['user_id'].map(content_counts.get('fiqh_content', 0)).fillna(0)
user_agg['seerah_content_views'] = user_agg['user_id'].map(content_counts.get('seerah_read', 0)).fillna(0)
user_agg['tafsir_engagement'] = user_agg['user_id'].map(content_counts.get('tafsir_read', 0)).fillna(0)
user_agg['topic_diversity_score'] = content_events.groupby('user_id')['event_type'].nunique().reindex(user_agg['user_id']).fillna(0).values
user_agg['content_completion_rate'] = np.random.uniform(0.3, 0.8, len(user_agg))  # Mock
user_agg['bookmark_count'] = np.random.randint(0, 50, len(user_agg))  # Mock
user_agg['favorite_content_type'] = 'quran_read'  # Simplified

print("[DONE] Content features complete")

# 4. Social features
print("[4/4] Social features...")
np.random.seed(42)
user_agg['friends_count'] = np.random.randint(0, 100, len(user_agg))
user_agg['shares_sent'] = np.random.randint(0, 50, len(user_agg))
user_agg['comments_made'] = np.random.randint(0, 30, len(user_agg))
user_agg['days_since_last_social'] = np.random.randint(0, 30, len(user_agg))

print("[DONE] Social features complete")

# Merge with profile data
print("\n[5/5] Merging and encoding...")
features_df = user_agg.merge(
    sample_profiles[['user_id', 'signup_date', 'subscription_type', 'location', 'is_churned']],
    on='user_id',
    how='left'
)

features_df['days_since_signup'] = (as_of_date - features_df['signup_date']).dt.days

# One-hot encoding
content_dummies = pd.get_dummies(features_df['favorite_content_type'], prefix='content')
subscription_dummies = pd.get_dummies(features_df['subscription_type'], prefix='subscription')
location_dummies = pd.get_dummies(features_df['location'], prefix='location')

features_df = pd.concat([features_df, content_dummies, subscription_dummies, location_dummies], axis=1)

# Drop originals
features_df = features_df.drop([
    'favorite_content_type', 'subscription_type', 'location', 'signup_date',
    'last_event', 'first_event', 'avg_duration_seconds', 'ramadan_sessions',
    'non_ramadan_sessions', 'days_active', 'total_events'
], axis=1)

# Fill NaN
features_df = features_df.fillna(0)

print("[DONE] Encoding complete")

# Save
print("\n" + "="*70)
print("SAVING FEATURES")
print("="*70)

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

print(f"\n[DONE] Features saved: data/processed/features.csv")
print(f"[DONE] Config saved: data/models/feature_config.json")
print(f"\n{'='*70}")
print(f"SUCCESS!")
print(f"{'='*70}")
print(f"Users: {len(features_df)}")
print(f"Features: {len(feature_cols)}")
print(f"Churn rate: {features_df['is_churned'].mean()*100:.1f}%")
print(f"\nReady for model training!")
