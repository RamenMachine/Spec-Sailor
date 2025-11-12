"""
Content Features Module
Calculates 10 content-related features for churn prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict


def calculate_content_features(
    events_df: pd.DataFrame,
    user_id: str
) -> Dict[str, float]:
    """
    Calculate all 10 content features for a single user

    Args:
        events_df: DataFrame with all user events
        user_id: User identifier

    Returns:
        Dictionary with 10 content features
    """
    # Filter events for this user
    user_events = events_df[events_df['user_id'] == user_id].copy()

    # Initialize features
    features = {
        'quran_reading_pct': 0.0,
        'hadith_engagement_pct': 0.0,
        'lecture_watch_minutes': 0.0,
        'fiqh_content_views': 0,
        'seerah_content_views': 0,
        'tafsir_engagement': 0,
        'topic_diversity_score': 0.0,
        'favorite_content_type': 'none',
        'content_completion_rate': 0.0,
        'bookmark_count': 0
    }

    if len(user_events) == 0:
        return features

    # Filter out app_open events for content analysis
    content_events = user_events[user_events['event_type'] != 'app_open'].copy()

    if len(content_events) == 0:
        return features

    total_events = len(content_events)

    # 1. Quran reading percentage
    quran_events = content_events[content_events['event_type'] == 'quran_read']
    features['quran_reading_pct'] = len(quran_events) / total_events

    # 2. Hadith engagement percentage
    hadith_events = content_events[content_events['event_type'] == 'hadith_read']
    features['hadith_engagement_pct'] = len(hadith_events) / total_events

    # 3. Lecture watch minutes
    lecture_events = content_events[content_events['event_type'] == 'lecture_view']
    features['lecture_watch_minutes'] = lecture_events['session_duration_seconds'].sum() / 60.0

    # 4. Fiqh content views
    fiqh_events = content_events[content_events['event_type'] == 'fiqh_content']
    features['fiqh_content_views'] = len(fiqh_events)

    # 5. Seerah content views
    seerah_events = content_events[content_events['event_type'] == 'seerah_read']
    features['seerah_content_views'] = len(seerah_events)

    # 6. Tafsir engagement
    tafsir_events = content_events[
        (content_events['event_type'] == 'tafsir_read') |
        (content_events['content_category'] == 'Tafsir')
    ]
    features['tafsir_engagement'] = len(tafsir_events)

    # 7. Topic diversity score (number of unique event types)
    unique_types = content_events['event_type'].nunique()
    features['topic_diversity_score'] = float(unique_types)

    # 8. Favorite content type (most common)
    if total_events > 0:
        mode_type = content_events['event_type'].mode()
        features['favorite_content_type'] = mode_type[0] if len(mode_type) > 0 else 'none'

    # 9. Content completion rate (proxy: sessions > 5 minutes)
    long_sessions = content_events[content_events['session_duration_seconds'] > 300]
    if total_events > 0:
        features['content_completion_rate'] = len(long_sessions) / total_events

    # 10. Bookmark count (simulated for demo - would be real data in production)
    # Simulate based on engagement level
    if total_events > 100:
        features['bookmark_count'] = min(100, int(np.random.exponential(total_events / 50)))
    elif total_events > 20:
        features['bookmark_count'] = int(np.random.exponential(5))
    else:
        features['bookmark_count'] = 0

    return features


def calculate_all_users_content(
    events_df: pd.DataFrame,
    user_ids: list,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Calculate content features for multiple users

    Args:
        events_df: DataFrame with all events
        user_ids: List of user IDs to process
        verbose: Whether to print progress

    Returns:
        DataFrame with content features for all users
    """
    features_list = []

    for i, user_id in enumerate(user_ids):
        if verbose and (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1}/{len(user_ids)} users...")

        features = calculate_content_features(events_df, user_id)
        features['user_id'] = user_id
        features_list.append(features)

    return pd.DataFrame(features_list)


if __name__ == "__main__":
    # Test the module
    import sys
    sys.path.append('.')

    # Load data
    events = pd.read_csv('data/raw/sample_events.csv', parse_dates=['event_timestamp'])
    profiles = pd.read_csv('data/raw/sample_profiles.csv')

    # Test on first 10 users
    test_users = profiles['user_id'].head(10).tolist()

    print("Testing content features on 10 users...")
    features_df = calculate_all_users_content(events, test_users, verbose=False)

    print("\nSample features:")
    print(features_df.head())
    print("\nFeature statistics:")
    print(features_df.describe())
