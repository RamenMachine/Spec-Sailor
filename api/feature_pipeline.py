"""
Automatic feature engineering pipeline for uploaded user data
Converts raw event logs into features for churn prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict


class AutoFeatureEngineer:
    """Automatically generate features from raw event data"""

    @staticmethod
    def engineer_features(df: pd.DataFrame, as_of_date: str = None) -> pd.DataFrame:
        """
        Generate features from raw event data

        Args:
            df: Raw events DataFrame with columns:
                - user_id
                - event_timestamp
                - event_type
                - (optional) session_duration, donation_amount, etc.
            as_of_date: Reference date for calculating features (default: today)

        Returns:
            DataFrame with one row per user and feature columns
        """

        if as_of_date is None:
            as_of_date = datetime.now()
        else:
            as_of_date = pd.to_datetime(as_of_date)

        # Ensure timestamp is datetime
        df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

        # Filter to events before as_of_date
        df = df[df['event_timestamp'] <= as_of_date].copy()

        # Initialize features list
        all_users = df['user_id'].unique()
        features_list = []

        print(f"[INFO] Engineering features for {len(all_users)} users...")

        for user_id in all_users:
            user_events = df[df['user_id'] == user_id].copy()
            features = AutoFeatureEngineer._calculate_user_features(
                user_events, as_of_date
            )
            features['user_id'] = user_id
            features_list.append(features)

        result_df = pd.DataFrame(features_list)
        print(f"[INFO] Generated {len(result_df.columns)-1} features for {len(result_df)} users")

        return result_df

    @staticmethod
    def _calculate_user_features(user_events: pd.DataFrame, as_of_date: datetime) -> Dict:
        """Calculate all features for a single user"""

        features = {}

        # Sort events chronologically
        user_events = user_events.sort_values('event_timestamp')

        # Basic engagement features
        features['total_events'] = len(user_events)

        # Recency: days since last activity
        last_event = user_events['event_timestamp'].max()
        features['days_since_last_activity'] = (as_of_date - last_event).days

        # Frequency: events in last 7 and 30 days
        week_ago = as_of_date - timedelta(days=7)
        month_ago = as_of_date - timedelta(days=30)

        features['events_last_7d'] = len(user_events[user_events['event_timestamp'] >= week_ago])
        features['events_last_30d'] = len(user_events[user_events['event_timestamp'] >= month_ago])

        # Tenure
        signup_date = user_events['event_timestamp'].min()
        features['days_since_signup'] = (as_of_date - signup_date).days

        # Session duration (if available)
        if 'session_duration' in user_events.columns:
            features['avg_session_duration'] = user_events['session_duration'].mean() / 60  # minutes
        else:
            features['avg_session_duration'] = 0

        # Event type diversity
        features['unique_event_types'] = user_events['event_type'].nunique()

        # Prayer-specific features
        prayer_events = user_events[user_events['event_type'].str.contains('prayer|salah', case=False, na=False)]
        features['prayer_count'] = len(prayer_events)
        if len(prayer_events) > 0:
            last_prayer = prayer_events['event_timestamp'].max()
            features['days_since_last_prayer'] = (as_of_date - last_prayer).days
        else:
            features['days_since_last_prayer'] = 999

        # Quran features
        quran_events = user_events[user_events['event_type'].str.contains('quran', case=False, na=False)]
        features['quran_count'] = len(quran_events)
        if len(quran_events) > 0:
            last_quran = quran_events['event_timestamp'].max()
            features['days_since_last_quran'] = (as_of_date - last_quran).days
        else:
            features['days_since_last_quran'] = 999

        # Donation features
        if 'donation_amount' in user_events.columns:
            donations = user_events[user_events['donation_amount'].notna()]
            features['donation_count'] = len(donations)
            features['total_donation_amount'] = donations['donation_amount'].sum() if len(donations) > 0 else 0
            if len(donations) > 0:
                last_donation = donations['event_timestamp'].max()
                features['days_since_last_donation'] = (as_of_date - last_donation).days
            else:
                features['days_since_last_donation'] = 999
        else:
            features['donation_count'] = 0
            features['total_donation_amount'] = 0
            features['days_since_last_donation'] = 999

        # Activity consistency (variance)
        if len(user_events) > 1:
            # Calculate days between consecutive events
            time_diffs = user_events['event_timestamp'].diff().dt.total_seconds() / 86400  # days
            features['activity_variance'] = time_diffs.std()
        else:
            features['activity_variance'] = 0

        # Ramadan engagement (approximate dates for 2024)
        ramadan_start = datetime(2024, 3, 11)
        ramadan_end = datetime(2024, 4, 9)
        ramadan_events = user_events[
            (user_events['event_timestamp'] >= ramadan_start) &
            (user_events['event_timestamp'] <= ramadan_end)
        ]
        features['ramadan_activity'] = len(ramadan_events)

        return features
