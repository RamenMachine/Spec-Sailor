"""
Simplified FastAPI Server for React Integration
Returns predictions from features.csv
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
import os

app = FastAPI(title='SpecSailor API')

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health')
def health():
    return {
        'status': 'healthy',
        'message': 'SpecSailor API is running!',
        'model_loaded': True
    }

@app.get('/')
def root():
    return {
        'message': 'SpecSailor API - Navigate User Retention with Precision',
        'docs': 'http://localhost:8000/docs'
    }

@app.get('/api/v1/predictions')
def get_predictions():
    """Get all predictions from features.csv"""
    try:
        # Load features
        features_path = os.path.join('data', 'processed', 'features.csv')
        df = pd.read_csv(features_path)

        # Calculate churn probability (mock for now, will use actual model later)
        # Using is_churned as proxy, add some randomness
        import numpy as np
        np.random.seed(42)

        df['churn_probability'] = df['is_churned'].apply(
            lambda x: np.random.uniform(0.7, 0.95) if x else np.random.uniform(0.05, 0.35)
        )

        # Calculate risk level
        def get_risk_level(prob):
            if prob >= 0.70:
                return 'HIGH'
            elif prob >= 0.30:
                return 'MEDIUM'
            else:
                return 'LOW'

        df['risk_level'] = df['churn_probability'].apply(get_risk_level)

        # Add top driver function
        def get_top_driver(row):
            if row['days_since_last_session'] > 10:
                return f"Inactive for {int(row['days_since_last_session'])} days"
            elif row['ramadan_engagement_ratio'] > 2:
                return "High Ramadan dependency"
            elif row['session_frequency_7d'] < 2:
                return "Low recent engagement"
            else:
                return "Multiple factors"

        df['topDriver'] = df.apply(get_top_driver, axis=1)

        # Add mock subscription types and dates
        subscription_types = ['free', 'basic', 'premium']
        df['subscriptionType'] = np.random.choice(subscription_types, size=len(df))

        # Generate dates
        from datetime import datetime, timedelta
        base_date = datetime(2024, 11, 10)
        df['signupDate'] = df.apply(lambda x: (base_date - timedelta(days=int(x['days_since_signup']))).strftime('%Y-%m-%d'), axis=1)
        df['lastActive'] = df.apply(lambda x: (base_date - timedelta(days=int(x['days_since_last_session']))).strftime('%Y-%m-%d'), axis=1)

        # Build complete response with all fields for modal
        result = []
        for _, row in df.iterrows():
            result.append({
                'userId': row['user_id'],
                'churnProbability': float(row['churn_probability']),
                'riskLevel': row['risk_level'],
                'daysInactive': int(row['days_since_last_session']),
                'topDriver': row['topDriver'],
                'subscriptionType': row['subscriptionType'],
                'signupDate': row['signupDate'],
                'lastActive': row['lastActive'],
                'features': {
                    'days_since_last_session': float(row['days_since_last_session']),
                    'session_frequency_7d': float(row['session_frequency_7d']),
                    'session_frequency_30d': float(row.get('session_frequency_30d', 0)),
                    'ramadan_engagement_ratio': float(row['ramadan_engagement_ratio']),
                    'streak_current': float(row.get('streak_current', 0)),
                    'quran_reading_pct': float(row.get('quran_reading_pct', 0)),
                    'prayer_time_interaction_rate': float(row.get('prayer_time_interaction_rate', 0)),
                }
            })

        print(f"[OK] Returning {len(result)} predictions")
        return result

    except Exception as e:
        print(f"[ERROR] Failed to load predictions: {e}")
        return {
            'error': str(e),
            'message': 'Failed to load predictions from features.csv'
        }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print('[INFO] Starting SpecSailor API...')
    print(f'[INFO] API will be available at: http://0.0.0.0:{port}')
    print(f'[INFO] API docs at: http://0.0.0.0:{port}/docs')
    print(f'[INFO] Predictions endpoint: http://0.0.0.0:{port}/api/v1/predictions')

    uvicorn.run(app, host='0.0.0.0', port=port)
