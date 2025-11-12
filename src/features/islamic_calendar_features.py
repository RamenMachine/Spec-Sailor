"""
Islamic Calendar Features Module
Calculates 8 Islamic calendar-related features for churn prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict


# Islamic calendar constants
RAMADAN_START = datetime(2024, 3, 11)
RAMADAN_END = datetime(2024, 4, 9)
LAST_10_NIGHTS_START = datetime(2024, 3, 30)
EID_START = datetime(2024, 4, 10)
EID_END = datetime(2024, 4, 12)
MUHARRAM_START = datetime(2024, 7, 7)
MUHARRAM_END = datetime(2024, 8, 6)

# Prayer times (approximate, in hours from midnight)
PRAYER_TIMES = [5.5, 12.5, 15.5, 18.5, 20.0]  # Fajr, Dhuhr, Asr, Maghrib, Isha


def is_during_ramadan(date: datetime) -> bool:
    """Check if date is during Ramadan"""
    return RAMADAN_START <= date <= RAMADAN_END


def is_during_last_10_nights(date: datetime) -> bool:
    """Check if date is in last 10 nights of Ramadan"""
    return LAST_10_NIGHTS_START <= date <= RAMADAN_END


def is_friday(date: datetime) -> bool:
    """Check if date is Friday (Jummah)"""
    return date.weekday() == 4


def is_prayer_time(hour: float, window: float = 1.0) -> bool:
    """Check if hour is within prayer time window"""
    for prayer_time in PRAYER_TIMES:
        if abs(hour - prayer_time) <= window:
            return True
    return False


def calculate_islamic_features(
    events_df: pd.DataFrame,
    profiles_df: pd.DataFrame,
    user_id: str,
    as_of_date: datetime
) -> Dict[str, float]:
    """
    Calculate all 8 Islamic calendar features for a single user

    Args:
        events_df: DataFrame with all user events
        profiles_df: DataFrame with user profiles
        user_id: User identifier
        as_of_date: Date to calculate features as of

    Returns:
        Dictionary with 8 Islamic calendar features
    """
    # Filter events for this user
    user_events = events_df[
        (events_df['user_id'] == user_id) &
        (events_df['event_timestamp'] <= as_of_date)
    ].copy()

    # Get user profile
    user_profile = profiles_df[profiles_df['user_id'] == user_id].iloc[0] if len(
        profiles_df[profiles_df['user_id'] == user_id]
    ) > 0 else None

    # Initialize features
    features = {
        'ramadan_engagement_ratio': 0.0,
        'is_ramadan_convert': 0,
        'days_since_ramadan': 0,
        'last_10_nights_sessions': 0,
        'jummah_participation_rate': 0.0,
        'prayer_time_interaction_rate': 0.0,
        'eid_participation': 0,
        'muharram_participation': 0
    }

    if len(user_events) == 0:
        # Calculate features that don't require events
        if user_profile is not None:
            signup_date = pd.to_datetime(user_profile['signup_date'])
            features['is_ramadan_convert'] = 1 if is_during_ramadan(signup_date) else 0

        features['days_since_ramadan'] = (as_of_date - RAMADAN_END).days
        return features

    # Get session events
    sessions = user_events[user_events['event_type'] == 'app_open'].copy()

    if len(sessions) == 0:
        return features

    # 1. Ramadan engagement ratio
    ramadan_sessions = sessions[
        (sessions['event_timestamp'] >= RAMADAN_START) &
        (sessions['event_timestamp'] <= RAMADAN_END)
    ]
    non_ramadan_sessions = sessions[
        (sessions['event_timestamp'] < RAMADAN_START) |
        (sessions['event_timestamp'] > RAMADAN_END)
    ]

    ramadan_count = len(ramadan_sessions)
    non_ramadan_count = len(non_ramadan_sessions)

    if non_ramadan_count > 0:
        # Calculate engagement ratio (sessions per day)
        ramadan_days = (RAMADAN_END - RAMADAN_START).days + 1
        ramadan_rate = ramadan_count / ramadan_days if ramadan_count > 0 else 0

        # Non-Ramadan days available
        first_event = sessions['event_timestamp'].min()
        last_event = min(sessions['event_timestamp'].max(), as_of_date)

        # Calculate non-Ramadan days
        total_days = (last_event - first_event).days + 1
        non_ramadan_days = total_days - min(ramadan_days, total_days)

        if non_ramadan_days > 0:
            non_ramadan_rate = non_ramadan_count / non_ramadan_days
            if non_ramadan_rate > 0:
                features['ramadan_engagement_ratio'] = ramadan_rate / non_ramadan_rate
            else:
                features['ramadan_engagement_ratio'] = ramadan_rate
        else:
            features['ramadan_engagement_ratio'] = ramadan_rate
    elif ramadan_count > 0:
        features['ramadan_engagement_ratio'] = 10.0  # Only active during Ramadan
    else:
        features['ramadan_engagement_ratio'] = 0.0

    # 2. Is Ramadan convert
    if user_profile is not None:
        signup_date = pd.to_datetime(user_profile['signup_date'])
        features['is_ramadan_convert'] = 1 if is_during_ramadan(signup_date) else 0

    # 3. Days since Ramadan
    features['days_since_ramadan'] = (as_of_date - RAMADAN_END).days

    # 4. Last 10 nights sessions
    last_10_sessions = sessions[
        (sessions['event_timestamp'] >= LAST_10_NIGHTS_START) &
        (sessions['event_timestamp'] <= RAMADAN_END)
    ]
    features['last_10_nights_sessions'] = len(last_10_sessions)

    # 5. Jummah (Friday) participation rate
    # Count Fridays since first activity
    first_activity = sessions['event_timestamp'].min()
    days_active = (as_of_date - first_activity).days + 1
    total_fridays = days_active // 7  # Approximate number of Fridays

    if total_fridays > 0:
        sessions['is_friday'] = sessions['event_timestamp'].apply(lambda x: is_friday(x))
        fridays_with_activity = sessions[sessions['is_friday']]['event_timestamp'].dt.date.nunique()
        features['jummah_participation_rate'] = fridays_with_activity / total_fridays
    else:
        features['jummah_participation_rate'] = 0.0

    # 6. Prayer time interaction rate
    total_prayer_opportunities = days_active * 5  # 5 prayers per day

    if total_prayer_opportunities > 0:
        # Check events within ±1 hour of prayer times
        user_events['hour'] = user_events['event_timestamp'].dt.hour + \
                             user_events['event_timestamp'].dt.minute / 60.0
        user_events['is_prayer_time'] = user_events['hour'].apply(is_prayer_time)

        prayer_time_events = user_events[user_events['is_prayer_time']].groupby(
            user_events['event_timestamp'].dt.date
        ).size()

        # Count days with at least one prayer time interaction
        days_with_prayer_interaction = len(prayer_time_events)
        features['prayer_time_interaction_rate'] = days_with_prayer_interaction / days_active
    else:
        features['prayer_time_interaction_rate'] = 0.0

    # 7. Eid participation
    eid_sessions = sessions[
        (sessions['event_timestamp'] >= EID_START) &
        (sessions['event_timestamp'] <= EID_END)
    ]
    features['eid_participation'] = 1 if len(eid_sessions) > 0 else 0

    # 8. Muharram participation
    muharram_sessions = sessions[
        (sessions['event_timestamp'] >= MUHARRAM_START) &
        (sessions['event_timestamp'] <= MUHARRAM_END)
    ]
    features['muharram_participation'] = 1 if len(muharram_sessions) > 0 else 0

    return features


def calculate_all_users_islamic(
    events_df: pd.DataFrame,
    profiles_df: pd.DataFrame,
    user_ids: list,
    as_of_date: datetime,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Calculate Islamic calendar features for multiple users

    Args:
        events_df: DataFrame with all events
        profiles_df: DataFrame with user profiles
        user_ids: List of user IDs to process
        as_of_date: Date to calculate features as of
        verbose: Whether to print progress

    Returns:
        DataFrame with Islamic calendar features for all users
    """
    features_list = []

    for i, user_id in enumerate(user_ids):
        if verbose and (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1}/{len(user_ids)} users...")

        features = calculate_islamic_features(events_df, profiles_df, user_id, as_of_date)
        features['user_id'] = user_id
        features_list.append(features)

    return pd.DataFrame(features_list)


if __name__ == "__main__":
    # Test the module
    import sys
    sys.path.append('.')

    # Load data
    events = pd.read_csv('data/raw/sample_events.csv', parse_dates=['event_timestamp'])
    profiles = pd.read_csv('data/raw/sample_profiles.csv', parse_dates=['signup_date'])

    # Test on first 10 users
    test_users = profiles['user_id'].head(10).tolist()
    as_of_date = datetime(2024, 11, 10)

    print("Testing Islamic calendar features on 10 users...")
    features_df = calculate_all_users_islamic(events, profiles, test_users, as_of_date, verbose=False)

    print("\nSample features:")
    print(features_df.head())
    print("\nFeature statistics:")
    print(features_df.describe())
