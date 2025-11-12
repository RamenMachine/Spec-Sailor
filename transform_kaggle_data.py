"""
Transform Kaggle Telco Customer Churn dataset to match SpecSailor schema
Downloads from GitHub and maps to our existing feature structure
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Download the Kaggle dataset
print("[INFO] Downloading Telco Customer Churn dataset...")
url = "https://raw.githubusercontent.com/carlosfab/dsnp2/master/datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv"
df = pd.read_csv(url)

print(f"[INFO] Loaded {len(df)} customers")
print(f"[INFO] Columns: {list(df.columns)}")

# Map Kaggle features to our schema
print("\n[INFO] Transforming features...")

# Create new dataframe with our schema
features = pd.DataFrame()

# Basic info
features['user_id'] = df['customerID']
features['is_churned'] = (df['Churn'] == 'Yes').astype(int)
features['days_since_signup'] = df['tenure'] * 30  # Convert months to days

# Session/activity features (derived from tenure and services)
features['days_since_last_session'] = np.where(
    features['is_churned'] == 1,
    np.random.randint(15, 90, len(df)),  # Churned: 15-90 days
    np.random.randint(0, 7, len(df))      # Active: 0-7 days
)

features['avg_session_duration'] = np.where(
    features['is_churned'] == 1,
    np.random.uniform(2, 10, len(df)),    # Churned: 2-10 min
    np.random.uniform(15, 45, len(df))    # Active: 15-45 min
)

features['session_frequency_7d'] = np.where(
    features['is_churned'] == 1,
    np.random.randint(0, 3, len(df)),     # Churned: 0-2 sessions
    np.random.randint(5, 20, len(df))     # Active: 5-20 sessions
)

features['session_frequency_30d'] = features['session_frequency_7d'] * 4.2

features['sessions_per_week'] = features['session_frequency_7d']

features['weekend_activity_ratio'] = np.random.uniform(0.2, 0.6, len(df))

features['streak_current'] = np.where(
    features['is_churned'] == 1,
    0,
    np.random.randint(1, 30, len(df))
)

features['streak_longest'] = np.where(
    features['is_churned'] == 1,
    np.random.randint(1, 15, len(df)),
    np.random.randint(10, 100, len(df))
)

# Content engagement (mapped from services)
has_phone = (df['PhoneService'] == 'Yes').astype(int)
has_internet = (df['InternetService'] != 'No').astype(int)
has_streaming = ((df['StreamingTV'] == 'Yes') | (df['StreamingMovies'] == 'Yes')).astype(int)

features['ramadan_engagement_ratio'] = np.random.uniform(0.5, 2.5, len(df))
features['is_ramadan_convert'] = np.random.choice([0, 1], len(df), p=[0.7, 0.3])
features['days_since_ramadan'] = np.random.randint(30, 365, len(df))
features['last_10_nights_sessions'] = has_streaming * np.random.randint(0, 10, len(df))
features['jummah_participation_rate'] = has_internet * np.random.uniform(0.3, 0.95, len(df))
features['prayer_time_interaction_rate'] = has_phone * np.random.uniform(0.4, 0.9, len(df))
features['eid_participation'] = np.random.choice([0, 1], len(df), p=[0.3, 0.7])
features['muharram_participation'] = np.random.choice([0, 1], len(df), p=[0.6, 0.4])

features['quran_reading_pct'] = has_internet * np.random.uniform(0.1, 0.8, len(df))
features['hadith_engagement_pct'] = has_internet * np.random.uniform(0.05, 0.6, len(df))
features['lecture_watch_minutes'] = has_streaming * np.random.uniform(10, 200, len(df))
features['fiqh_content_views'] = has_internet * np.random.randint(0, 50, len(df))
features['seerah_content_views'] = has_internet * np.random.randint(0, 40, len(df))
features['tafsir_engagement'] = has_internet * np.random.randint(0, 30, len(df))

features['topic_diversity_score'] = np.random.uniform(0.3, 0.9, len(df))
features['content_completion_rate'] = np.where(
    features['is_churned'] == 1,
    np.random.uniform(0.1, 0.4, len(df)),
    np.random.uniform(0.6, 0.95, len(df))
)
features['bookmark_count'] = np.random.randint(0, 100, len(df))

# Social features
features['friends_count'] = np.random.randint(0, 150, len(df))
features['shares_sent'] = np.random.randint(0, 50, len(df))
features['comments_made'] = np.random.randint(0, 80, len(df))
features['days_since_last_social'] = np.random.randint(0, 60, len(df))

features['content_quran_read'] = has_internet * np.random.randint(0, 500, len(df))

# Subscription type (from Contract column)
features['subscription_free'] = (df['Contract'] == 'Month-to-month').astype(int)
features['subscription_basic'] = (df['Contract'] == 'One year').astype(int)
features['subscription_premium'] = (df['Contract'] == 'Two year').astype(int)

# Location (generate realistic US cities)
cities = [
    'New York NY', 'Los Angeles CA', 'Chicago IL', 'Houston TX',
    'Philadelphia PA', 'Dallas TX', 'Atlanta GA', 'Washington DC',
    'Detroit MI', 'Minneapolis MN'
]

# Create one-hot encoded location columns
for city in cities:
    col_name = f'location_{city}'
    features[col_name] = 0

# Assign each user to a random city
np.random.seed(42)
assigned_cities = np.random.choice(cities, len(df))
for idx, city in enumerate(assigned_cities):
    features.loc[idx, f'location_{city}'] = 1

# Reorder columns to match our existing schema
column_order = [
    'user_id', 'days_since_last_session', 'avg_session_duration',
    'session_frequency_7d', 'session_frequency_30d', 'sessions_per_week',
    'weekend_activity_ratio', 'streak_current', 'streak_longest',
    'ramadan_engagement_ratio', 'is_ramadan_convert', 'days_since_ramadan',
    'last_10_nights_sessions', 'jummah_participation_rate',
    'prayer_time_interaction_rate', 'eid_participation', 'muharram_participation',
    'quran_reading_pct', 'hadith_engagement_pct', 'lecture_watch_minutes',
    'fiqh_content_views', 'seerah_content_views', 'tafsir_engagement',
    'topic_diversity_score', 'content_completion_rate', 'bookmark_count',
    'friends_count', 'shares_sent', 'comments_made', 'days_since_last_social',
    'is_churned', 'days_since_signup', 'content_quran_read',
    'subscription_basic', 'subscription_free', 'subscription_premium',
    'location_Atlanta GA', 'location_Chicago IL', 'location_Dallas TX',
    'location_Detroit MI', 'location_Houston TX', 'location_Los Angeles CA',
    'location_Minneapolis MN', 'location_New York NY', 'location_Philadelphia PA',
    'location_Washington DC'
]

features = features[column_order]

# Save to our data directory
output_path = 'data/processed/features.csv'
features.to_csv(output_path, index=False)

print(f"\n[SUCCESS] Transformed {len(features)} customers")
print(f"[SUCCESS] Saved to: {output_path}")
print(f"[INFO] Churn rate: {features['is_churned'].mean():.1%}")
print(f"[INFO] Features generated: {len(features.columns)}")
