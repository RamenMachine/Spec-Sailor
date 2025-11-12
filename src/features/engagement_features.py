"""
Engagement Features Module
Calculates 10 engagement-related features for churn prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict


def calculate_engagement_features(
    events_df: pd.DataFrame,
    user_id: str,
    as_of_date: datetime
) -> Dict[str, float]:
    """
    Calculate all 10 engagement features for a single user

    Args:
        events_df: DataFrame with all user events
        user_id: User identifier
        as_of_date: Date to calculate features as of

    Returns:
        Dictionary with 10 engagement features
    """
    # Filter events for this user before as_of_date
    user_events = events_df[
        (events_df['user_id'] == user_id) &
        (events_df['event_timestamp'] <= as_of_date)
    ].copy()

    # Initialize features with default values
    features = {
        'days_since_last_session': 180,  # Max value if no events
        'session_frequency_7d': 0,
        'session_frequency_30d': 0,
        'avg_session_duration': 0.0,
        'total_sessions': 0,
        'streak_current': 0,
        'streak_longest': 0,
        'days_since_signup': 0,
        'sessions_per_week': 0.0,
        'weekend_activity_ratio': 0.0
    }

    if len(user_events) == 0:
        return features

    # Get app_open events (sessions)
    sessions = user_events[user_events['event_type'] == 'app_open'].copy()

    if len(sessions) == 0:
        return features

    # 1. Days since last session
    last_session = sessions['event_timestamp'].max()
    features['days_since_last_session'] = (as_of_date - last_session).days

    # 2. Session frequency last 7 days
    seven_days_ago = as_of_date - timedelta(days=7)
    features['session_frequency_7d'] = len(
        sessions[sessions['event_timestamp'] >= seven_days_ago]
    )

    # 3. Session frequency last 30 days
    thirty_days_ago = as_of_date - timedelta(days=30)
    features['session_frequency_30d'] = len(
        sessions[sessions['event_timestamp'] >= thirty_days_ago]
    )

    # 4. Average session duration (in minutes)
    # Sum all non-zero durations per session day
    user_events['date'] = user_events['event_timestamp'].dt.date
    daily_durations = user_events.groupby('date')['session_duration_seconds'].sum()
    if len(daily_durations) > 0:
        features['avg_session_duration'] = daily_durations.mean() / 60.0  # Convert to minutes

    # 5. Total sessions
    features['total_sessions'] = len(sessions)

    # 6 & 7. Calculate streaks (current and longest)
    sessions['date'] = sessions['event_timestamp'].dt.date
    unique_dates = sorted(sessions['date'].unique())

    if len(unique_dates) > 0:
        current_streak = 0
        longest_streak = 0
        temp_streak = 1

        # Calculate longest streak
        for i in range(1, len(unique_dates)):
            if (unique_dates[i] - unique_dates[i-1]).days == 1:
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
        longest_streak = max(longest_streak, temp_streak)

        # Calculate current streak (working backwards from as_of_date)
        current_date = as_of_date.date()
        while current_date in unique_dates:
            current_streak += 1
            current_date -= timedelta(days=1)

        features['streak_current'] = current_streak
        features['streak_longest'] = longest_streak

    # 8. Days since signup (calculated in main pipeline from profile)
    # This will be added from profile data

    # 9. Sessions per week
    if 'signup_date' in user_events.columns and len(user_events) > 0:
        first_event = user_events['event_timestamp'].min()
        days_active = (as_of_date - first_event).days + 1
        weeks_active = max(1, days_active / 7.0)
        features['sessions_per_week'] = features['total_sessions'] / weeks_active

    # 10. Weekend activity ratio
    sessions['is_weekend'] = sessions['event_timestamp'].dt.dayofweek.isin([5, 6])
    if len(sessions) > 0:
        features['weekend_activity_ratio'] = sessions['is_weekend'].mean()

    return features


def calculate_all_users_engagement(
    events_df: pd.DataFrame,
    user_ids: list,
    as_of_date: datetime,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Calculate engagement features for multiple users

    Args:
        events_df: DataFrame with all events
        user_ids: List of user IDs to process
        as_of_date: Date to calculate features as of
        verbose: Whether to print progress

    Returns:
        DataFrame with engagement features for all users
    """
    features_list = []

    for i, user_id in enumerate(user_ids):
        if verbose and (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1}/{len(user_ids)} users...")

        features = calculate_engagement_features(events_df, user_id, as_of_date)
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
    as_of_date = datetime(2024, 11, 10)

    print("Testing engagement features on 10 users...")
    features_df = calculate_all_users_engagement(events, test_users, as_of_date, verbose=False)

    print("\nSample features:")
    print(features_df.head())
    print("\nFeature statistics:")
    print(features_df.describe())
