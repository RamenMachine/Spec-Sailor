"""
Data Generation Script for Barakah Retain
Generates synthetic Islamic app usage data with realistic patterns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Constants from PRD
NUM_USERS = 10000
START_DATE = datetime(2024, 6, 1)
END_DATE = datetime(2024, 11, 10)
RAMADAN_START = datetime(2024, 3, 11)
RAMADAN_END = datetime(2024, 4, 9)
EID_START = datetime(2024, 4, 10)
EID_END = datetime(2024, 4, 12)
MUHARRAM_START = datetime(2024, 7, 7)
MUHARRAM_END = datetime(2024, 8, 6)

# Event types
EVENT_TYPES = [
    'app_open',
    'quran_read',
    'prayer_log',
    'lecture_view',
    'hadith_read',
    'fiqh_content',
    'seerah_read',
    'tafsir_read',
    'dua_view'
]

# Content categories
CONTENT_CATEGORIES = {
    'quran_read': 'Quran',
    'hadith_read': 'Hadith',
    'lecture_view': random.choice(['Seerah', 'Fiqh', 'Tafsir', 'General']),
    'fiqh_content': 'Fiqh',
    'seerah_read': 'Seerah',
    'tafsir_read': 'Tafsir',
    'dua_view': 'Dua',
    'prayer_log': 'Prayer'
}

# US cities with large Muslim populations
US_CITIES = [
    'Chicago IL',
    'Houston TX',
    'Dallas TX',
    'New York NY',
    'Los Angeles CA',
    'Detroit MI',
    'Atlanta GA',
    'Philadelphia PA',
    'Washington DC',
    'Minneapolis MN'
]

# Prayer times (approximate, in hours from midnight)
PRAYER_TIMES = [5.5, 12.5, 15.5, 18.5, 20.0]  # Fajr, Dhuhr, Asr, Maghrib, Isha


def generate_user_id(index: int) -> str:
    """Generate a user ID"""
    return f"user-{str(index).zfill(6)}"


def get_user_engagement_type() -> str:
    """Determine user engagement level"""
    rand = random.random()
    if rand < 0.15:  # 15% high engagers
        return 'high'
    elif rand < 0.50:  # 35% medium engagers
        return 'medium'
    else:  # 50% low engagers
        return 'low'


def get_sessions_per_day(engagement_type: str, is_ramadan: bool = False) -> float:
    """Get average sessions per day based on engagement type and Ramadan"""
    base_sessions = {
        'high': np.random.uniform(5, 10),
        'medium': np.random.uniform(2, 5),
        'low': np.random.uniform(0.5, 2)
    }

    multiplier = 3.0 if is_ramadan else 1.0
    return base_sessions[engagement_type] * multiplier


def is_ramadan_date(date: datetime) -> bool:
    """Check if date is during Ramadan"""
    return RAMADAN_START <= date <= RAMADAN_END


def is_last_10_nights(date: datetime) -> bool:
    """Check if date is in last 10 nights of Ramadan"""
    last_10_start = datetime(2024, 3, 30)
    return last_10_start <= date <= RAMADAN_END


def is_friday(date: datetime) -> bool:
    """Check if date is Friday (Jummah)"""
    return date.weekday() == 4  # Friday is 4


def is_weekend(date: datetime) -> bool:
    """Check if date is weekend"""
    return date.weekday() in [5, 6]  # Saturday, Sunday


def get_prayer_time_hour() -> int:
    """Get a random prayer time hour"""
    return int(random.choice(PRAYER_TIMES))


def should_generate_event(
    date: datetime,
    engagement_type: str,
    is_ramadan_convert: bool,
    days_since_ramadan: int
) -> bool:
    """Determine if user should have activity on this date"""

    is_ram = is_ramadan_date(date)

    # Base probability by engagement type
    base_prob = {
        'high': 0.95,
        'medium': 0.60,
        'low': 0.25
    }[engagement_type]

    # Ramadan multiplier
    if is_ram:
        base_prob = min(0.98, base_prob * 2.5)

    # Post-Ramadan drop-off for Ramadan converts
    if is_ramadan_convert and days_since_ramadan > 0:
        # 60% drop off within 30 days
        if days_since_ramadan <= 30:
            drop_rate = 0.60 * (days_since_ramadan / 30)
            base_prob = base_prob * (1 - drop_rate)
        else:
            base_prob = base_prob * 0.40

    # Friday boost
    if is_friday(date):
        base_prob = min(0.99, base_prob * 1.4)

    # Weekend boost
    if is_weekend(date):
        base_prob = min(0.98, base_prob * 1.2)

    return random.random() < base_prob


def generate_session_events(
    user_id: str,
    date: datetime,
    engagement_type: str
) -> List[Dict]:
    """Generate events for a single session"""
    events = []

    # Determine number of actions in session
    num_actions = {
        'high': np.random.poisson(8),
        'medium': np.random.poisson(4),
        'low': np.random.poisson(2)
    }[engagement_type]

    num_actions = max(1, num_actions)

    # Always start with app_open
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    # Bias toward prayer times and evening
    if random.random() < 0.4:  # 40% at prayer times
        hour = get_prayer_time_hour()
    elif random.random() < 0.3:  # 30% in evening (7-10 PM)
        hour = random.randint(19, 22)

    timestamp = date.replace(hour=hour, minute=minute, second=second)

    # App open event
    events.append({
        'user_id': user_id,
        'event_timestamp': timestamp,
        'event_type': 'app_open',
        'session_duration_seconds': 0,
        'content_category': None
    })

    # Additional content events
    for i in range(num_actions):
        # Progress time within session
        timestamp += timedelta(seconds=random.randint(10, 120))

        # Select event type (weighted)
        if is_ramadan_date(date):
            # More Quran and prayer during Ramadan
            event_type = random.choices(
                EVENT_TYPES[1:],  # Exclude app_open
                weights=[40, 25, 10, 10, 5, 5, 3, 2],
                k=1
            )[0]
        else:
            # Normal distribution
            event_type = random.choices(
                EVENT_TYPES[1:],
                weights=[25, 15, 20, 15, 10, 10, 3, 2],
                k=1
            )[0]

        # Session duration for this event
        if event_type == 'quran_read':
            duration = np.random.gamma(3, 200)  # Longer sessions
        elif event_type == 'lecture_view':
            duration = np.random.gamma(5, 300)  # Even longer
        elif event_type == 'prayer_log':
            duration = np.random.gamma(1, 30)  # Quick
        else:
            duration = np.random.gamma(2, 100)  # Medium

        duration = int(min(3600, max(10, duration)))  # 10s to 60 min

        # Get content category
        content_cat = CONTENT_CATEGORIES.get(event_type)
        if event_type == 'lecture_view':
            content_cat = random.choice(['Seerah', 'Fiqh', 'Tafsir', 'General'])

        events.append({
            'user_id': user_id,
            'event_timestamp': timestamp,
            'event_type': event_type,
            'session_duration_seconds': duration,
            'content_category': content_cat
        })

    return events


def generate_user_profile(index: int) -> Dict:
    """Generate a single user profile"""
    user_id = generate_user_id(index)
    engagement_type = get_user_engagement_type()

    # Determine if Ramadan convert (40% signed up during Ramadan)
    is_ramadan_convert = random.random() < 0.40

    if is_ramadan_convert:
        # Signup during Ramadan
        signup_date = RAMADAN_START + timedelta(
            days=random.randint(0, (RAMADAN_END - RAMADAN_START).days)
        )
    else:
        # Signup throughout the year
        signup_start = datetime(2023, 12, 1)
        signup_end = datetime(2024, 11, 10)
        signup_date = signup_start + timedelta(
            days=random.randint(0, (signup_end - signup_start).days)
        )

    # Subscription type
    rand = random.random()
    if rand < 0.70:
        subscription = 'free'
    elif rand < 0.90:
        subscription = 'basic'
    else:
        subscription = 'premium'

    # Location
    location = random.choice(US_CITIES)

    return {
        'user_id': user_id,
        'signup_date': signup_date,
        'subscription_type': subscription,
        'location': location,
        'engagement_type': engagement_type,
        'is_ramadan_convert': is_ramadan_convert
    }


def generate_user_events(profile: Dict) -> List[Dict]:
    """Generate all events for a single user"""
    events = []
    user_id = profile['user_id']
    engagement_type = profile['engagement_type']
    is_ramadan_convert = profile['is_ramadan_convert']
    signup_date = profile['signup_date']

    # Generate events from signup until end date
    current_date = max(signup_date, START_DATE)

    # Determine if user will churn
    # Ramadan converts have 70% churn rate, others 20%
    will_churn = random.random() < (0.70 if is_ramadan_convert else 0.20)

    if will_churn:
        # Determine churn date
        if is_ramadan_convert:
            # Churn within 30-60 days after Ramadan
            days_until_churn = random.randint(10, 60)
            churn_date = RAMADAN_END + timedelta(days=days_until_churn)
        else:
            # Random churn date
            days_active = random.randint(30, 150)
            churn_date = current_date + timedelta(days=days_active)

        # Cap churn date at reasonable point
        churn_date = min(churn_date, datetime(2024, 10, 15))
    else:
        churn_date = END_DATE + timedelta(days=1)  # Active user

    # Generate events day by day
    while current_date <= min(END_DATE, churn_date):
        days_since_ramadan = (current_date - RAMADAN_END).days if current_date > RAMADAN_END else -1

        # Decide if user has activity this day
        if should_generate_event(current_date, engagement_type, is_ramadan_convert, days_since_ramadan):
            # Determine number of sessions this day
            is_ram = is_ramadan_date(current_date)
            sessions_per_day = get_sessions_per_day(engagement_type, is_ram)
            num_sessions = max(1, int(np.random.poisson(sessions_per_day)))

            # Generate events for each session
            for _ in range(num_sessions):
                session_events = generate_session_events(user_id, current_date, engagement_type)
                events.extend(session_events)

        current_date += timedelta(days=1)

    return events


def generate_all_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate all user profiles and events"""
    print(f"Generating data for {NUM_USERS} users...")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print(f"Ramadan period: {RAMADAN_START} to {RAMADAN_END}")

    profiles = []
    all_events = []

    for i in range(NUM_USERS):
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} users...")

        profile = generate_user_profile(i)
        profiles.append(profile)

        user_events = generate_user_events(profile)
        all_events.extend(user_events)

    # Create DataFrames
    profiles_df = pd.DataFrame(profiles)
    events_df = pd.DataFrame(all_events)

    # Add last_active and is_churned to profiles
    last_active = events_df.groupby('user_id')['event_timestamp'].max()
    profiles_df['last_active'] = profiles_df['user_id'].map(last_active)

    # User is churned if no activity in last 30 days
    cutoff_date = END_DATE - timedelta(days=30)
    profiles_df['is_churned'] = profiles_df['last_active'] < cutoff_date

    # Sort events by timestamp
    events_df = events_df.sort_values(['user_id', 'event_timestamp']).reset_index(drop=True)

    print(f"\nGeneration complete!")
    print(f"Total users: {len(profiles_df)}")
    print(f"Total events: {len(events_df)}")
    print(f"Churned users: {profiles_df['is_churned'].sum()} ({profiles_df['is_churned'].mean()*100:.1f}%)")
    print(f"Active users: {(~profiles_df['is_churned']).sum()} ({(~profiles_df['is_churned']).mean()*100:.1f}%)")

    return profiles_df, events_df


def save_data(profiles_df: pd.DataFrame, events_df: pd.DataFrame, output_dir: str = 'data/raw'):
    """Save generated data to CSV files"""
    import os

    os.makedirs(output_dir, exist_ok=True)

    profiles_path = os.path.join(output_dir, 'sample_profiles.csv')
    events_path = os.path.join(output_dir, 'sample_events.csv')

    profiles_df.to_csv(profiles_path, index=False)
    events_df.to_csv(events_path, index=False)

    print(f"\nData saved:")
    print(f"  Profiles: {profiles_path}")
    print(f"  Events: {events_path}")

    return profiles_path, events_path


if __name__ == "__main__":
    # Generate data
    profiles_df, events_df = generate_all_data()

    # Save to CSV
    save_data(profiles_df, events_df)

    # Print sample statistics
    print("\n=== Sample Statistics ===")
    print(f"\nSubscription distribution:")
    print(profiles_df['subscription_type'].value_counts())

    print(f"\nRamadan converts: {profiles_df['is_ramadan_convert'].sum()}")

    print(f"\nTop 5 locations:")
    print(profiles_df['location'].value_counts().head())

    print(f"\nEvent type distribution:")
    print(events_df['event_type'].value_counts())

    print(f"\nAverage events per user: {len(events_df) / len(profiles_df):.1f}")
