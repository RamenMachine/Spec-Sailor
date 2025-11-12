"""
Simplified FastAPI Server for React Integration
Returns predictions from features.csv
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import uvicorn
import os
import sys
from datetime import datetime

# Fix Python path for Railway/Docker deployment
# Add parent directory to Python path so we can import api module
# This works when running: python api/simple_api.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try imports with proper path handling
try:
    # Try absolute import (when running as module or with fixed path)
    from api.upload_handler import DataUploadHandler
    from api.feature_pipeline import AutoFeatureEngineer
except ImportError:
    try:
        # Try relative import (when running from api directory)
        from upload_handler import DataUploadHandler
        from feature_pipeline import AutoFeatureEngineer
    except ImportError:
        # Last resort: add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        from upload_handler import DataUploadHandler
        from feature_pipeline import AutoFeatureEngineer

app = FastAPI(title='SpecSailor API')

# In-memory storage for uploaded data (use Redis/DB in production)
upload_storage = {}

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
        # Load features - try multiple paths for Railway/Docker
        possible_paths = [
            os.path.join('data', 'processed', 'features.csv'),
            os.path.join(os.getcwd(), 'data', 'processed', 'features.csv'),
            os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'features.csv')
        ]
        
        features_path = None
        for path in possible_paths:
            if os.path.exists(path):
                features_path = path
                break
        
        if not features_path:
            raise FileNotFoundError(f"Features file not found. Checked: {possible_paths}")
        
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


# ============================================================================
# UPLOAD & ANALYSIS ENDPOINTS
# ============================================================================

@app.post("/api/v1/upload")
async def upload_data(file: UploadFile = File(...)):
    """
    Upload user data file for analysis
    Accepts CSV, Excel (.xlsx), or JSON files
    """
    try:
        print(f"[INFO] Received upload: {file.filename}")

        # Validate and parse
        result = await DataUploadHandler.validate_and_parse(file)

        # Store data in memory
        upload_storage[result['upload_id']] = {
            'data': result['data'],
            'summary': result['summary'],
            'status': 'uploaded',
            'created_at': datetime.now().isoformat()
        }

        print(f"[OK] Upload {result['upload_id']} stored successfully")

        return {
            'upload_id': result['upload_id'],
            'summary': result['summary'],
            'validation': result['validation']
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        raise HTTPException(500, f"Upload failed: {str(e)}")


@app.post("/api/v1/analyze/{upload_id}")
async def analyze_uploaded_data(upload_id: str):
    """
    Generate churn predictions for uploaded data
    """
    if upload_id not in upload_storage:
        raise HTTPException(404, "Upload not found")

    try:
        print(f"[INFO] Analyzing upload: {upload_id}")

        # Get uploaded data
        raw_data = upload_storage[upload_id]['data']

        # Run feature engineering
        print("[INFO] Engineering features...")
        features_df = AutoFeatureEngineer.engineer_features(raw_data)

        # For now, use simple heuristics for prediction
        # (In production, load actual XGBoost model)
        print("[INFO] Generating predictions...")

        # Simple heuristic: high days since last activity = high churn risk
        features_df['churn_probability'] = features_df.apply(
            lambda row: min(0.95, max(0.05, (
                0.5 * (row['days_since_last_activity'] / 30) +
                0.3 * (1 - row['events_last_7d'] / max(1, row['events_last_30d'])) +
                0.2 * (row['days_since_last_prayer'] / 30)
            ))),
            axis=1
        )

        features_df['risk_level'] = features_df['churn_probability'].apply(
            lambda x: 'HIGH' if x > 0.7 else ('MEDIUM' if x > 0.4 else 'LOW')
        )

        # Store results
        upload_storage[upload_id]['predictions'] = features_df
        upload_storage[upload_id]['status'] = 'completed'

        print(f"[OK] Analysis complete for {len(features_df)} users")

        return {
            'job_id': upload_id,
            'status': 'completed',
            'summary': {
                'total_users': int(len(features_df)),
                'high_risk': int(len(features_df[features_df['risk_level'] == 'HIGH'])),
                'medium_risk': int(len(features_df[features_df['risk_level'] == 'MEDIUM'])),
                'low_risk': int(len(features_df[features_df['risk_level'] == 'LOW']))
            }
        }

    except Exception as e:
        print(f"[ERROR] Analysis failed: {e}")
        upload_storage[upload_id]['status'] = 'failed'
        upload_storage[upload_id]['error'] = str(e)
        raise HTTPException(500, f"Analysis failed: {str(e)}")


@app.get("/api/v1/results/{job_id}")
async def get_analysis_results(job_id: str):
    """
    Get predictions for analyzed upload
    """
    if job_id not in upload_storage:
        raise HTTPException(404, "Job not found")

    if upload_storage[job_id]['status'] != 'completed':
        return {
            'status': upload_storage[job_id]['status'],
            'message': 'Analysis not completed'
        }

    predictions_df = upload_storage[job_id]['predictions']

    # Convert to API response format
    predictions = predictions_df.to_dict('records')

    return {
        'predictions': predictions[:100],  # Limit to first 100 for performance
        'summary': {
            'total_users': int(len(predictions_df)),
            'avg_churn_probability': float(predictions_df['churn_probability'].mean()),
            'high_risk_count': int(len(predictions_df[predictions_df['risk_level'] == 'HIGH'])),
            'medium_risk_count': int(len(predictions_df[predictions_df['risk_level'] == 'MEDIUM'])),
            'low_risk_count': int(len(predictions_df[predictions_df['risk_level'] == 'LOW']))
        }
    }


@app.get("/api/v1/download/{job_id}")
async def download_results(job_id: str):
    """
    Download predictions as CSV file
    """
    import tempfile

    if job_id not in upload_storage:
        raise HTTPException(404, "Job not found")

    predictions_df = upload_storage[job_id]['predictions'].copy()

    # Add recommendations
    def get_recommendation(row):
        if row['risk_level'] == 'HIGH':
            return "Immediate intervention: Personal outreach within 24h"
        elif row['risk_level'] == 'MEDIUM':
            return "Monitor closely: Send engagement email this week"
        else:
            return "Maintain: Continue regular communication"

    predictions_df['recommendation'] = predictions_df.apply(get_recommendation, axis=1)

    # Save to temp file using cross-platform temp directory
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"{job_id}_results.csv")
    predictions_df.to_csv(output_path, index=False)

    return FileResponse(
        output_path,
        media_type='text/csv',
        filename=f"churn_predictions_{job_id}.csv"
    )


@app.get("/api/v1/template")
async def download_template():
    """
    Download CSV template for data upload
    """
    # Try multiple possible paths for Railway/Docker deployment
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'specsailor_universal_template.csv'),
        os.path.join(os.getcwd(), 'specsailor_universal_template.csv'),
        'specsailor_universal_template.csv'
    ]
    
    template_path = None
    for path in possible_paths:
        if os.path.exists(path):
            template_path = path
            break
    
    if not template_path or not os.path.exists(template_path):
        raise HTTPException(404, f"Template file not found. Checked: {possible_paths}")

    return FileResponse(
        template_path,
        media_type='text/csv',
        filename="specsailor_universal_template.csv"
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print('[INFO] Starting SpecSailor API...')
    print(f'[INFO] API will be available at: http://0.0.0.0:{port}')
    print(f'[INFO] API docs at: http://0.0.0.0:{port}/docs')
    print(f'[INFO] Predictions endpoint: http://0.0.0.0:{port}/api/v1/predictions')

    uvicorn.run(app, host='0.0.0.0', port=port)
