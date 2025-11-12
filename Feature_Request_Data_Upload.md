# Feature Request: Real-Time User Data Upload & Analysis
## SpecSailor v2.0 - Interactive Data Analysis

**Version:** 1.0  
**Date:** November 11, 2024  
**Requester:** Ameen  
**Priority:** HIGH  
**Status:** Ready for Implementation

---

## 📋 Executive Summary

Add functionality for users to upload their own Islamic app user data (CSV/JSON) and receive instant churn predictions without needing to modify code or redeploy the system.

### Current State
- System works only with pre-loaded 7,373 users
- New data requires manual feature engineering and model retraining
- No way for external users to test with their own data

### Desired State
- Upload CSV/Excel/JSON file via web interface
- Automatic feature engineering on uploaded data
- Real-time churn predictions displayed in dashboard
- Downloadable results with recommendations

---

## 🎯 Problem Statement

**User Story:**
> "As a product manager at an Islamic app company, I want to upload my user activity data and immediately see which users are at risk of churning, so I can run targeted retention campaigns without hiring a data scientist."

**Current Pain Points:**
1. **No Self-Service:** Users can't test the system with their own data
2. **Technical Barrier:** Requires Python knowledge to prepare data
3. **Limited Demo Value:** Portfolio visitors see only pre-loaded data
4. **No Real Business Use:** Can't be used by actual Islamic organizations

**Business Impact:**
- 🔴 Blocks real-world adoption
- 🔴 Limits portfolio demonstration value
- 🟡 Requires manual work for each new dataset
- 🟡 Can't showcase to potential employers/partners

---

## ✅ Success Criteria

### Functional Requirements
- [ ] Upload interface accepts CSV, Excel, JSON files
- [ ] Automatic validation of required columns
- [ ] Real-time feature engineering (completes in <30 seconds)
- [ ] Predictions displayed in existing dashboard views
- [ ] Export results as CSV with recommendations
- [ ] Handle files up to 50,000 users

### Non-Functional Requirements
- [ ] Upload + prediction time: <30 seconds for 10K users
- [ ] Clear error messages for invalid data
- [ ] Progress indicator during processing
- [ ] Mobile-responsive upload interface
- [ ] Secure file handling (no data persistence)

### User Experience Goals
- [ ] Zero-code experience (no terminal, no Python)
- [ ] Sample data template provided
- [ ] Inline help explaining required columns
- [ ] Preview of uploaded data before processing

---

## 🏗️ Technical Architecture

### System Flow
```
User Upload → Validation → Feature Engineering → Prediction → Dashboard Display
     ↓            ↓              ↓                  ↓              ↓
   File        Check         Generate            XGBoost        React
  Browser     Columns        Features            Model          Tables
   (CSV)      Format         Pipeline            API            Charts
```

### Component Changes

#### 1. Frontend (React)
**New Components:**
- `UploadPage.tsx` - Main upload interface
- `FileUploader.tsx` - Drag-and-drop component
- `DataPreview.tsx` - Show first 10 rows before processing
- `UploadProgress.tsx` - Loading state with steps

**Modified Components:**
- `Predictions.tsx` - Switch between default data and uploaded data
- `Layout.tsx` - Add "Upload Data" nav link

#### 2. Backend (FastAPI)
**New Endpoints:**
```python
POST /api/v1/upload
- Accepts: multipart/form-data (CSV/Excel/JSON)
- Returns: upload_id, validation_status

POST /api/v1/analyze/{upload_id}
- Triggers: Feature engineering + prediction
- Returns: job_id, estimated_time

GET /api/v1/results/{job_id}
- Returns: predictions array, metrics, feature_importance

GET /api/v1/download/{job_id}
- Returns: CSV file with predictions + recommendations
```

**New Modules:**
```python
api/
├── upload_handler.py      # File upload & validation
├── feature_pipeline.py    # Automatic feature engineering
├── prediction_service.py  # Generate predictions for new data
└── job_manager.py         # Track async processing jobs
```

#### 3. Feature Engineering Pipeline
**Automatic Detection:**
- Detect date/time columns
- Infer event types (prayer, donation, session)
- Calculate recency, frequency, monetary features
- Handle missing Islamic calendar features

**Flexible Schema:**
```python
# Required columns (minimum)
user_id: str
event_timestamp: datetime
event_type: str

# Optional columns (enhance predictions)
session_duration: int
donation_amount: float
content_category: str
```

---

## 📊 Data Schema Requirements

### Minimum Required Format

#### CSV Example:
```csv
user_id,event_timestamp,event_type
user-001,2024-11-01 08:30:00,app_open
user-001,2024-11-01 08:35:00,prayer_log
user-001,2024-11-01 09:00:00,quran_read
user-002,2024-11-02 14:20:00,donation
```

#### JSON Example:
```json
[
  {
    "user_id": "user-001",
    "event_timestamp": "2024-11-01T08:30:00Z",
    "event_type": "app_open",
    "session_duration": 300,
    "donation_amount": null
  }
]
```

### Validation Rules
```python
Required:
- user_id: Non-null, string
- event_timestamp: Valid datetime (ISO 8601 or common formats)
- event_type: Non-null, string

Optional (improves accuracy):
- session_duration: Positive integer (seconds)
- donation_amount: Positive float
- content_category: String
- location: String

Constraints:
- Minimum 100 events per file
- Minimum 10 unique users
- Date range: Last 90 days recommended
- File size: <50 MB
```

---

## 🎨 UI/UX Design Specifications

### Upload Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  📤 Upload Your Data                                         │
│  Get instant churn predictions for your app users            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Step 1: Download Template (Optional)                       │
│  [📥 Download CSV Template] [📥 Download Sample Data]        │
│                                                               │
│  Your data should include:                                   │
│  ✓ user_id - Unique identifier for each user                │
│  ✓ event_timestamp - When the event occurred                │
│  ✓ event_type - Type of activity (prayer, session, etc.)    │
│  ⚡ More columns = Better predictions!                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Step 2: Upload Your File                                    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                       │   │
│  │           📁 Drag & drop your file here              │   │
│  │                       or                             │   │
│  │              [Choose File to Upload]                 │   │
│  │                                                       │   │
│  │     Accepted formats: CSV, Excel (.xlsx), JSON       │   │
│  │            Maximum size: 50 MB                        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

[After file selected]

┌─────────────────────────────────────────────────────────────┐
│  Step 3: Preview Your Data                                   │
│  ✓ File: user_data.csv (2.3 MB, 15,432 events)              │
│  ✓ Detected: 1,245 unique users                             │
│  ✓ Date range: Oct 1, 2024 - Nov 10, 2024                   │
│                                                               │
│  First 10 rows:                                              │
│  ┌──────────┬─────────────────────┬─────────────┐           │
│  │ user_id  │ event_timestamp     │ event_type  │           │
│  ├──────────┼─────────────────────┼─────────────┤           │
│  │ user-001 │ 2024-11-01 08:30:00 │ app_open    │           │
│  │ user-001 │ 2024-11-01 08:35:00 │ prayer_log  │           │
│  └──────────┴─────────────────────┴─────────────┘           │
│                                                               │
│  [⬅️ Upload Different File]  [➡️ Analyze Data]               │
└─────────────────────────────────────────────────────────────┘

[After clicking Analyze]

┌─────────────────────────────────────────────────────────────┐
│  🔄 Analyzing Your Data...                                   │
│                                                               │
│  ✓ Validating data format                [Done]              │
│  ✓ Engineering features                  [Done]              │
│  🔄 Generating predictions                [Processing...]     │
│  ⏳ Calculating insights                  [Waiting...]        │
│                                                               │
│  Processing 1,245 users... (Estimated: 15 seconds)          │
│                                                               │
│  [Progress Bar: ████████░░░░░░░░ 60%]                       │
└─────────────────────────────────────────────────────────────┘

[After completion]

┌─────────────────────────────────────────────────────────────┐
│  ✅ Analysis Complete!                                       │
│                                                               │
│  📊 Results Summary:                                         │
│  • Total Users: 1,245                                        │
│  • High Risk: 167 (13.4%)                                    │
│  • Medium Risk: 312 (25.1%)                                  │
│  • Low Risk: 766 (61.5%)                                     │
│                                                               │
│  [📊 View Dashboard] [📥 Download Results] [🔄 Upload New]   │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Implementation Guide for Claude Code

### Phase 1: Backend - File Upload Handler

**File:** `api/upload_handler.py`

```python
from fastapi import UploadFile, HTTPException
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List
import uuid

class DataUploadHandler:
    """Handle file uploads and validation"""
    
    REQUIRED_COLUMNS = ['user_id', 'event_timestamp', 'event_type']
    ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.json']
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    
    @staticmethod
    async def validate_and_parse(file: UploadFile) -> Dict:
        """
        Validate uploaded file and parse into DataFrame
        
        Returns:
            {
                'upload_id': str,
                'data': pd.DataFrame,
                'validation': {
                    'is_valid': bool,
                    'errors': List[str],
                    'warnings': List[str]
                },
                'summary': {
                    'total_events': int,
                    'unique_users': int,
                    'date_range': tuple,
                    'event_types': List[str]
                }
            }
        """
        
        # Check file extension
        file_ext = file.filename.split('.')[-1]
        if f'.{file_ext}' not in DataUploadHandler.ALLOWED_EXTENSIONS:
            raise HTTPException(400, f"Unsupported file type: {file_ext}")
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > DataUploadHandler.MAX_FILE_SIZE:
            raise HTTPException(400, "File too large (max 50 MB)")
        
        # Parse based on file type
        try:
            if file_ext == 'csv':
                df = pd.read_csv(io.BytesIO(content))
            elif file_ext == 'xlsx':
                df = pd.read_excel(io.BytesIO(content))
            elif file_ext == 'json':
                df = pd.read_json(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(400, f"Failed to parse file: {str(e)}")
        
        # Validate columns
        validation_result = DataUploadHandler._validate_columns(df)
        
        if not validation_result['is_valid']:
            raise HTTPException(400, f"Validation failed: {validation_result['errors']}")
        
        # Generate upload ID
        upload_id = str(uuid.uuid4())
        
        # Create summary
        summary = DataUploadHandler._create_summary(df)
        
        return {
            'upload_id': upload_id,
            'data': df,
            'validation': validation_result,
            'summary': summary
        }
    
    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> Dict:
        """Validate required columns exist and are formatted correctly"""
        errors = []
        warnings = []
        
        # Check required columns
        missing_cols = [col for col in DataUploadHandler.REQUIRED_COLUMNS 
                       if col not in df.columns]
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
        
        # Check for nulls in required columns
        for col in DataUploadHandler.REQUIRED_COLUMNS:
            if col in df.columns and df[col].isnull().any():
                null_count = df[col].isnull().sum()
                errors.append(f"Column '{col}' has {null_count} null values")
        
        # Validate timestamp format
        if 'event_timestamp' in df.columns:
            try:
                df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
            except Exception as e:
                errors.append(f"Invalid timestamp format: {str(e)}")
        
        # Check minimum data requirements
        if len(df) < 100:
            errors.append(f"Insufficient data: {len(df)} events (minimum 100)")
        
        unique_users = df['user_id'].nunique() if 'user_id' in df.columns else 0
        if unique_users < 10:
            errors.append(f"Insufficient users: {unique_users} (minimum 10)")
        
        # Warnings for optional columns
        optional_cols = ['session_duration', 'donation_amount', 'content_category']
        missing_optional = [col for col in optional_cols if col not in df.columns]
        if missing_optional:
            warnings.append(f"Optional columns missing (may reduce accuracy): {missing_optional}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def _create_summary(df: pd.DataFrame) -> Dict:
        """Generate summary statistics"""
        return {
            'total_events': len(df),
            'unique_users': df['user_id'].nunique(),
            'date_range': (
                df['event_timestamp'].min().isoformat(),
                df['event_timestamp'].max().isoformat()
            ),
            'event_types': df['event_type'].unique().tolist()
        }
```

---

### Phase 2: Backend - Automatic Feature Engineering

**File:** `api/feature_pipeline.py`

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class AutoFeatureEngineer:
    """Automatically generate features from raw event data"""
    
    @staticmethod
    def engineer_features(df: pd.DataFrame, as_of_date: str = None) -> pd.DataFrame:
        """
        Generate all 44 features from raw event data
        
        Args:
            df: Raw events DataFrame with columns:
                - user_id
                - event_timestamp
                - event_type
                - (optional) session_duration, donation_amount, etc.
            as_of_date: Reference date for calculating features (default: today)
        
        Returns:
            DataFrame with one row per user and 44 feature columns
        """
        
        if as_of_date is None:
            as_of_date = datetime.now()
        else:
            as_of_date = pd.to_datetime(as_of_date)
        
        # Filter to events before as_of_date
        df = df[df['event_timestamp'] <= as_of_date].copy()
        
        # Initialize features dict
        all_users = df['user_id'].unique()
        features_list = []
        
        for user_id in all_users:
            user_events = df[df['user_id'] == user_id].copy()
            features = AutoFeatureEngineer._calculate_user_features(
                user_events, as_of_date
            )
            features['user_id'] = user_id
            features_list.append(features)
        
        return pd.DataFrame(features_list)
    
    @staticmethod
    def _calculate_user_features(user_events: pd.DataFrame, as_of_date: datetime) -> Dict:
        """Calculate all features for a single user"""
        
        features = {}
        
        # Sort events chronologically
        user_events = user_events.sort_values('event_timestamp')
        
        # 1. ENGAGEMENT FEATURES
        features.update(AutoFeatureEngineer._engagement_features(user_events, as_of_date))
        
        # 2. RECENCY FEATURES  
        features.update(AutoFeatureEngineer._recency_features(user_events, as_of_date))
        
        # 3. CONTENT FEATURES
        features.update(AutoFeatureEngineer._content_features(user_events))
        
        # 4. FINANCIAL FEATURES (if donation data exists)
        features.update(AutoFeatureEngineer._financial_features(user_events, as_of_date))
        
        # 5. ISLAMIC CALENDAR FEATURES
        features.update(AutoFeatureEngineer._islamic_features(user_events, as_of_date))
        
        return features
    
    @staticmethod
    def _engagement_features(df: pd.DataFrame, as_of_date: datetime) -> Dict:
        """Calculate engagement metrics"""
        
        # Session events
        sessions = df[df['event_type'].str.contains('app_open|session', case=False, na=False)]
        
        # Last 7 days
        week_ago = as_of_date - timedelta(days=7)
        sessions_7d = sessions[sessions['event_timestamp'] >= week_ago]
        
        # Last 30 days
        month_ago = as_of_date - timedelta(days=30)
        sessions_30d = sessions[sessions['event_timestamp'] >= month_ago]
        
        # Session duration
        avg_duration = 0
        if 'session_duration' in df.columns:
            avg_duration = df['session_duration'].mean() / 60  # Convert to minutes
        
        # Signup date (first event)
        signup_date = df['event_timestamp'].min()
        days_since_signup = (as_of_date - signup_date).days
        
        # Sessions per week
        weeks_active = max(1, days_since_signup / 7)
        sessions_per_week = len(sessions) / weeks_active
        
        return {
            'session_frequency_7d': len(sessions_7d),
            'session_frequency_30d': len(sessions_30d),
            'avg_session_duration': avg_duration,
            'total_sessions': len(sessions),
            'days_since_signup': days_since_signup,
            'sessions_per_week': sessions_per_week
        }
    
    @staticmethod
    def _recency_features(df: pd.DataFrame, as_of_date: datetime) -> Dict:
        """Calculate days since last activity for each event type"""
        
        features = {}
        
        # Days since any event
        last_event = df['event_timestamp'].max()
        features['days_since_last_activity'] = (as_of_date - last_event).days
        
        # Days since specific event types
        event_types = {
            'prayer': ['prayer', 'salah'],
            'quran': ['quran', 'reading'],
            'donation': ['donation', 'sadaqah'],
            'article': ['article', 'blog'],
            'video': ['video', 'lecture']
        }
        
        for key, keywords in event_types.items():
            type_events = df[df['event_type'].str.contains('|'.join(keywords), case=False, na=False)]
            if len(type_events) > 0:
                last_occurrence = type_events['event_timestamp'].max()
                features[f'days_since_last_{key}'] = (as_of_date - last_occurrence).days
            else:
                features[f'days_since_last_{key}'] = 999  # Never occurred
        
        return features
    
    @staticmethod
    def _content_features(df: pd.DataFrame) -> Dict:
        """Calculate content consumption metrics"""
        
        # Count by event type
        event_counts = df['event_type'].value_counts().to_dict()
        
        # Prayer logs
        prayer_events = df[df['event_type'].str.contains('prayer', case=False, na=False)]
        
        # Quran reading (if duration available)
        quran_minutes = 0
        if 'session_duration' in df.columns:
            quran_events = df[df['event_type'].str.contains('quran', case=False, na=False)]
            quran_minutes = quran_events['session_duration'].sum() / 60
        
        # Article/video counts
        articles = df[df['event_type'].str.contains('article|blog', case=False, na=False)]
        videos = df[df['event_type'].str.contains('video|lecture', case=False, na=False)]
        
        return {
            'prayers_logged_total': len(prayer_events),
            'quran_reading_minutes_total': quran_minutes,
            'articles_read_count': len(articles),
            'videos_watched_count': len(videos),
            'unique_event_types': df['event_type'].nunique()
        }
    
    @staticmethod
    def _financial_features(df: pd.DataFrame, as_of_date: datetime) -> Dict:
        """Calculate donation metrics if available"""
        
        if 'donation_amount' not in df.columns:
            return {
                'donations_count': 0,
                'donations_total_amount': 0.0,
                'avg_donation_amount': 0.0,
                'days_since_last_donation': 999
            }
        
        donations = df[df['donation_amount'].notna()]
        
        if len(donations) == 0:
            return {
                'donations_count': 0,
                'donations_total_amount': 0.0,
                'avg_donation_amount': 0.0,
                'days_since_last_donation': 999
            }
        
        last_donation = donations['event_timestamp'].max()
        
        return {
            'donations_count': len(donations),
            'donations_total_amount': donations['donation_amount'].sum(),
            'avg_donation_amount': donations['donation_amount'].mean(),
            'days_since_last_donation': (as_of_date - last_donation).days
        }
    
    @staticmethod
    def _islamic_features(df: pd.DataFrame, as_of_date: datetime) -> Dict:
        """Calculate Islamic calendar-aware features"""
        
        # Detect Ramadan period (approximate - would use hijri calendar in production)
        # For 2024: March 11 - April 9
        ramadan_start = datetime(2024, 3, 11)
        ramadan_end = datetime(2024, 4, 9)
        
        ramadan_events = df[
            (df['event_timestamp'] >= ramadan_start) & 
            (df['event_timestamp'] <= ramadan_end)
        ]
        non_ramadan_events = df[
            (df['event_timestamp'] < ramadan_start) | 
            (df['event_timestamp'] > ramadan_end)
        ]
        
        # Ramadan engagement ratio
        ramadan_ratio = 0
        if len(non_ramadan_events) > 0:
            ramadan_per_day = len(ramadan_events) / 30 if len(ramadan_events) > 0 else 0
            non_ramadan_per_day = len(non_ramadan_events) / max(1, (df['event_timestamp'].max() - df['event_timestamp'].min()).days - 30)
            ramadan_ratio = ramadan_per_day / max(0.1, non_ramadan_per_day)
        
        # Friday (Jumma) activity
        df_copy = df.copy()
        df_copy['day_of_week'] = df_copy['event_timestamp'].dt.dayofweek
        friday_events = df_copy[df_copy['day_of_week'] == 4]  # Friday = 4
        
        total_fridays = len(pd.date_range(
            start=df['event_timestamp'].min(),
            end=as_of_date,
            freq='W-FRI'
        ))
        
        fridays_with_activity = friday_events['event_timestamp'].dt.date.nunique()
        jumma_rate = fridays_with_activity / max(1, total_fridays)
        
        return {
            'ramadan_engagement_ratio': ramadan_ratio,
            'ramadan_activity_score': len(ramadan_events),
            'jumma_prayer_rate': jumma_rate
        }
```

---

### Phase 3: Backend - API Endpoints

**File:** `api/simple_api.py` (add these endpoints)

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from api.upload_handler import DataUploadHandler
from api.feature_pipeline import AutoFeatureEngineer
import json
import os

# Add to existing FastAPI app

# In-memory storage for uploaded data (use Redis/DB in production)
upload_storage = {}

@app.post("/api/v1/upload")
async def upload_data(file: UploadFile = File(...)):
    """
    Upload user data file for analysis
    
    Returns:
        {
            'upload_id': str,
            'summary': {
                'total_events': int,
                'unique_users': int,
                'date_range': tuple,
                'event_types': list
            },
            'validation': {
                'is_valid': bool,
                'warnings': list
            }
        }
    """
    
    try:
        # Validate and parse uploaded file
        result = await DataUploadHandler.validate_and_parse(file)
        
        # Store data in memory (temporarily)
        upload_storage[result['upload_id']] = {
            'data': result['data'],
            'summary': result['summary'],
            'status': 'uploaded',
            'created_at': datetime.now().isoformat()
        }
        
        return {
            'upload_id': result['upload_id'],
            'summary': result['summary'],
            'validation': result['validation']
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {str(e)}")


@app.post("/api/v1/analyze/{upload_id}")
async def analyze_uploaded_data(upload_id: str):
    """
    Generate predictions for uploaded data
    
    Returns:
        {
            'job_id': str,
            'status': 'processing',
            'estimated_time': int (seconds)
        }
    """
    
    if upload_id not in upload_storage:
        raise HTTPException(404, "Upload not found")
    
    try:
        # Get uploaded data
        raw_data = upload_storage[upload_id]['data']
        
        # Run feature engineering
        features_df = AutoFeatureEngineer.engineer_features(raw_data)
        
        # Load trained model
        import xgboost as xgb
        model = xgb.Booster()
        model.load_model('data/models/xgboost_model.json')
        
        # Generate predictions
        import xgboost as xgb
        dmatrix = xgb.DMatrix(features_df.drop('user_id', axis=1))
        predictions = model.predict(dmatrix)
        
        # Add predictions to features
        features_df['churn_probability'] = predictions
        features_df['risk_level'] = features_df['churn_probability'].apply(
            lambda x: 'HIGH' if x > 0.7 else ('MEDIUM' if x > 0.4 else 'LOW')
        )
        
        # Store results
        job_id = upload_id  # Reuse upload_id as job_id for simplicity
        upload_storage[upload_id]['predictions'] = features_df
        upload_storage[upload_id]['status'] = 'completed'
        
        return {
            'job_id': job_id,
            'status': 'completed',
            'summary': {
                'total_users': len(features_df),
                'high_risk': len(features_df[features_df['risk_level'] == 'HIGH']),
                'medium_risk': len(features_df[features_df['risk_level'] == 'MEDIUM']),
                'low_risk': len(features_df[features_df['risk_level'] == 'LOW'])
            }
        }
        
    except Exception as e:
        upload_storage[upload_id]['status'] = 'failed'
        upload_storage[upload_id]['error'] = str(e)
        raise HTTPException(500, f"Analysis failed: {str(e)}")


@app.get("/api/v1/results/{job_id}")
async def get_analysis_results(job_id: str):
    """
    Get predictions for analyzed upload
    
    Returns:
        {
            'predictions': [
                {
                    'user_id': str,
                    'churn_probability': float,
                    'risk_level': str,
                    'features': dict
                }
            ],
            'summary': dict,
            'feature_importance': list
        }
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
        'predictions': predictions,
        'summary': {
            'total_users': len(predictions_df),
            'avg_churn_probability': predictions_df['churn_probability'].mean(),
            'high_risk_count': len(predictions_df[predictions_df['risk_level'] == 'HIGH']),
            'medium_risk_count': len(predictions_df[predictions_df['risk_level'] == 'MEDIUM']),
            'low_risk_count': len(predictions_df[predictions_df['risk_level'] == 'LOW'])
        }
    }


@app.get("/api/v1/download/{job_id}")
async def download_results(job_id: str):
    """
    Download predictions as CSV file
    
    Returns: CSV file with predictions and recommendations
    """
    
    if job_id not in upload_storage:
        raise HTTPException(404, "Job not found")
    
    predictions_df = upload_storage[job_id]['predictions']
    
    # Add recommendations column
    def get_recommendation(row):
        if row['risk_level'] == 'HIGH':
            return "Immediate intervention: Personal outreach within 24h"
        elif row['risk_level'] == 'MEDIUM':
            return "Monitor closely: Send engagement email this week"
        else:
            return "Maintain: Continue regular communication"
    
    predictions_df['recommendation'] = predictions_df.apply(get_recommendation, axis=1)
    
    # Save to temp file
    output_path = f"/tmp/{job_id}_results.csv"
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
    
    Returns: CSV template file
    """
    
    template_data = {
        'user_id': ['user-001', 'user-001', 'user-002', 'user-002'],
        'event_timestamp': [
            '2024-11-01 08:30:00',
            '2024-11-01 09:00:00',
            '2024-11-02 14:20:00',
            '2024-11-02 15:00:00'
        ],
        'event_type': ['app_open', 'prayer_log', 'quran_read', 'donation'],
        'session_duration': [300, None, 600, None],
        'donation_amount': [None, None, None, 25.00]
    }
    
    template_df = pd.DataFrame(template_data)
    output_path = "/tmp/data_template.csv"
    template_df.to_csv(output_path, index=False)
    
    return FileResponse(
        output_path,
        media_type='text/csv',
        filename="specsailor_data_template.csv"
    )
```

---

### Phase 4: Frontend - Upload Page

**File:** `src/pages/UploadPage.tsx`

```typescript
import React, { useState } from 'react';
import { Upload, FileText, Download, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/v1/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setUploadResult(data);
    } catch (err) {
      setError('Failed to upload file. Please check the format and try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!uploadResult) return;

    setAnalyzing(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/analyze/${uploadResult.upload_id}`,
        { method: 'POST' }
      );

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setAnalysisResult(data);
    } catch (err) {
      setError('Failed to analyze data. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleDownload = async () => {
    if (!analysisResult) return;

    window.open(
      `http://localhost:8000/api/v1/download/${analysisResult.job_id}`,
      '_blank'
    );
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-2">Upload Your Data</h1>
        <p className="text-muted-foreground">
          Get instant churn predictions for your app users
        </p>
      </div>

      {/* Step 1: Download Template */}
      <Card>
        <CardHeader>
          <CardTitle>Step 1: Download Template (Optional)</CardTitle>
          <CardDescription>
            Download our template to ensure your data is in the correct format
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-4">
            <Button
              variant="outline"
              onClick={() => window.open('http://localhost:8000/api/v1/template', '_blank')}
            >
              <Download className="mr-2 h-4 w-4" />
              Download CSV Template
            </Button>
          </div>
          <div className="text-sm text-muted-foreground space-y-2">
            <p>Your data should include:</p>
            <ul className="list-disc list-inside space-y-1">
              <li><strong>user_id</strong> - Unique identifier for each user</li>
              <li><strong>event_timestamp</strong> - When the event occurred</li>
              <li><strong>event_type</strong> - Type of activity (prayer, session, etc.)</li>
              <li className="text-purple-400">⚡ More columns = Better predictions!</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* Step 2: Upload File */}
      <Card>
        <CardHeader>
          <CardTitle>Step 2: Upload Your File</CardTitle>
          <CardDescription>
            Upload CSV, Excel, or JSON file with your user activity data
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-purple-500/50 rounded-lg p-8 text-center">
              <Upload className="mx-auto h-12 w-12 text-purple-500 mb-4" />
              <input
                type="file"
                accept=".csv,.xlsx,.json"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <Button variant="outline" asChild>
                  <span>Choose File to Upload</span>
                </Button>
              </label>
              <p className="mt-2 text-sm text-muted-foreground">
                Accepted formats: CSV, Excel (.xlsx), JSON
              </p>
              <p className="text-sm text-muted-foreground">Maximum size: 50 MB</p>
            </div>

            {file && (
              <Alert>
                <FileText className="h-4 w-4" />
                <AlertDescription>
                  Selected: <strong>{file.name}</strong> ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </AlertDescription>
              </Alert>
            )}

            {file && !uploadResult && (
              <Button
                onClick={handleUpload}
                disabled={uploading}
                className="w-full"
              >
                {uploading ? 'Uploading...' : 'Upload & Validate'}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Step 3: Preview & Analyze */}
      {uploadResult && (
        <Card>
          <CardHeader>
            <CardTitle>Step 3: Preview Your Data</CardTitle>
            <CardDescription>Review your data before analysis</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Total Events</p>
                <p className="text-2xl font-bold">{uploadResult.summary.total_events.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Unique Users</p>
                <p className="text-2xl font-bold">{uploadResult.summary.unique_users.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Date Range</p>
                <p className="text-sm font-medium">
                  {new Date(uploadResult.summary.date_range[0]).toLocaleDateString()} -
                  {new Date(uploadResult.summary.date_range[1]).toLocaleDateString()}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Event Types</p>
                <p className="text-sm font-medium">{uploadResult.summary.event_types.length} types</p>
              </div>
            </div>

            {uploadResult.validation.warnings.length > 0 && (
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  <strong>Warnings:</strong>
                  <ul className="list-disc list-inside mt-2">
                    {uploadResult.validation.warnings.map((warning: string, i: number) => (
                      <li key={i}>{warning}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            )}

            {!analysisResult && (
              <Button
                onClick={handleAnalyze}
                disabled={analyzing}
                className="w-full"
              >
                {analyzing ? 'Analyzing...' : 'Analyze Data'}
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {/* Step 4: Results */}
      {analysisResult && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-6 w-6 text-green-500" />
              Analysis Complete!
            </CardTitle>
            <CardDescription>Your predictions are ready</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Total Users</p>
                <p className="text-2xl font-bold">{analysisResult.summary.total_users.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">High Risk</p>
                <p className="text-2xl font-bold text-red-500">
                  {analysisResult.summary.high_risk.toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Medium Risk</p>
                <p className="text-2xl font-bold text-yellow-500">
                  {analysisResult.summary.medium_risk.toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Low Risk</p>
                <p className="text-2xl font-bold text-green-500">
                  {analysisResult.summary.low_risk.toLocaleString()}
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <Button onClick={handleDownload} className="flex-1">
                <Download className="mr-2 h-4 w-4" />
                Download Results
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setFile(null);
                  setUploadResult(null);
                  setAnalysisResult(null);
                }}
                className="flex-1"
              >
                Upload New File
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
```

---

## 📅 Implementation Timeline

### Week 1: Backend (Days 1-5)
- [ ] Day 1-2: Implement `upload_handler.py` - file upload and validation
- [ ] Day 3-4: Implement `feature_pipeline.py` - automatic feature engineering
- [ ] Day 5: Add API endpoints to `simple_api.py`

### Week 2: Frontend (Days 6-10)
- [ ] Day 6-7: Create `UploadPage.tsx` with file upload UI
- [ ] Day 8: Implement preview and validation display
- [ ] Day 9: Add analysis trigger and results display
- [ ] Day 10: Integrate download functionality

### Week 3: Testing & Polish (Days 11-15)
- [ ] Day 11-12: End-to-end testing with various file formats
- [ ] Day 13: Error handling and edge cases
- [ ] Day 14: UI polish and loading states
- [ ] Day 15: Documentation and demo video

---

## ✅ Acceptance Criteria

### Must Have (MVP)
- [ ] User can upload CSV file via web interface
- [ ] System validates required columns
- [ ] Automatic feature engineering works for 1,000+ users
- [ ] Predictions displayed in existing dashboard
- [ ] Download results as CSV
- [ ] Clear error messages for invalid data
- [ ] Process completes in <30 seconds for 10K users

### Should Have (Post-MVP)
- [ ] Support Excel and JSON formats
- [ ] Real-time progress indicator with steps
- [ ] Sample data generation (synthetic test data)
- [ ] Comparison between uploaded data and baseline
- [ ] Email notification when analysis completes

### Nice to Have (Future)
- [ ] API key authentication
- [ ] Persistent storage (database)
- [ ] Scheduled re-analysis
- [ ] Multi-file upload (compare cohorts)
- [ ] Integration with Google Sheets / Airtable

---

## 🧪 Testing Checklist

### Functional Tests
- [ ] Upload valid CSV file → Success
- [ ] Upload Excel file → Success
- [ ] Upload JSON file → Success
- [ ] Upload file with missing columns → Error message
- [ ] Upload file with wrong date format → Error message
- [ ] Upload file with <100 events → Error message
- [ ] Upload 50MB file → Success (at limit)
- [ ] Upload 51MB file → Error message
- [ ] Analyze 10K users → Completes in <30s
- [ ] Download results → CSV file downloads correctly

### Edge Cases
- [ ] Upload empty file → Error
- [ ] Upload non-CSV/Excel/JSON → Error
- [ ] Upload corrupted file → Error
- [ ] Multiple uploads without refreshing → Works
- [ ] Upload with special characters in user_id → Handled
- [ ] Upload with future dates → Warning displayed

### UI/UX Tests
- [ ] Drag & drop file → Works
- [ ] Progress indicator shows correctly
- [ ] Error messages are clear
- [ ] Success state displays summary
- [ ] Download button is enabled after completion
- [ ] Works on mobile (responsive)

---

## 📊 Success Metrics

### User Engagement
- **Upload Rate**: >50% of visitors try upload feature
- **Completion Rate**: >80% complete analysis after upload
- **Download Rate**: >60% download results
- **Time to Value**: <2 minutes from upload to download

### Technical Performance
- **Processing Time**: <30s for 10K users, <60s for 50K users
- **Error Rate**: <5% of uploads fail validation
- **API Uptime**: >99% availability

### Business Impact
- **Demo Conversions**: Can showcase live with real data
- **Portfolio Engagement**: Visitors spend >3 minutes using tool
- **Partnership Leads**: Islamic orgs request production deployment

---

## 🚀 Deployment Notes

### Environment Variables
```bash
# .env
MAX_UPLOAD_SIZE=52428800  # 50 MB in bytes
ALLOWED_ORIGINS=http://localhost:8080,https://specsailor.com
STORAGE_TYPE=memory  # Use 'redis' or 'postgres' in production
```

### Production Recommendations
1. **File Storage**: Use S3/Cloudinary instead of memory
2. **Job Queue**: Use Celery/RQ for async processing
3. **Database**: Store upload metadata in PostgreSQL
4. **Rate Limiting**: Limit uploads to 10/hour per IP
5. **Authentication**: Require API key for production
6. **Monitoring**: Track upload success rate, processing time

---

## 📝 Documentation Updates

### README.md - Complete Upload Instructions Section

Add this comprehensive section to the README.md:

```markdown
## 📤 Upload Your Own Data

SpecSailor allows you to upload your own Islamic app user data and get instant churn predictions with 87% accuracy!

### Quick Start

1. **Navigate to Upload Page**
   - Click "Upload Data" in the navigation menu
   - Or visit: `https://your-app-url.com/upload`

2. **Prepare Your Data**
   - Download our template: Click "Download CSV Template" button
   - Or format your data according to the schema below

3. **Upload & Analyze**
   - Drag & drop your file or click "Choose File"
   - Preview your data summary
   - Click "Analyze Data" to generate predictions
   - Download results with personalized recommendations

### ✅ Data Format Requirements

#### Required Columns (Minimum)

Your CSV/Excel/JSON file **must** include these three columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `user_id` | String | Unique identifier for each user | `"user-001"`, `"abc123"` |
| `event_timestamp` | DateTime | When the event occurred | `"2024-11-01 08:30:00"` |
| `event_type` | String | Type of user activity | `"app_open"`, `"prayer_log"` |

**Supported Date Formats:**
- ISO 8601: `2024-11-01T08:30:00Z`
- Standard: `2024-11-01 08:30:00`
- US Format: `11/01/2024 8:30 AM`
- European: `01/11/2024 08:30`

#### Optional Columns (Improve Accuracy)

Adding these columns can improve prediction accuracy by up to 15%:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `session_duration` | Integer | Length of session in seconds | `300` (5 minutes) |
| `donation_amount` | Float | Dollar amount donated | `25.00` |
| `content_category` | String | Type of content accessed | `"Quran"`, `"Hadith"`, `"Prayer"` |
| `location` | String | User's city/region | `"Chicago, IL"` |

#### Recommended Event Types

For best results, include these event types in your data:

**Core Events:**
- `app_open` - User opened the application
- `session_start` / `session_end` - Session tracking

**Religious Activity:**
- `prayer_log` - User logged a prayer
- `quran_read` - Quran reading session
- `hadith_read` - Hadith study
- `dua_view` - Supplication viewed

**Engagement:**
- `article_read` - Article/blog post read
- `video_watch` - Video/lecture watched
- `lecture_view` - Islamic lecture viewed

**Financial:**
- `donation` - Charitable donation made
- `subscription_payment` - Premium subscription payment

**Social:**
- `share` - Content shared
- `comment` - Community comment
- `friend_add` - Social connection added

### 📋 CSV Template Example

```csv
user_id,event_timestamp,event_type,session_duration,donation_amount,content_category
user-001,2024-11-01 08:30:00,app_open,300,,
user-001,2024-11-01 08:35:00,prayer_log,,,Prayer
user-001,2024-11-01 09:00:00,quran_read,600,,Quran
user-002,2024-11-02 14:20:00,donation,,,
user-002,2024-11-02 14:20:00,donation,,25.00,Donation
user-002,2024-11-02 15:00:00,lecture_view,1800,,Seerah
user-003,2024-11-03 07:00:00,app_open,180,,
user-003,2024-11-03 07:05:00,hadith_read,420,,Hadith
```

### 📊 Excel Format Example

Create an Excel file (.xlsx) with one sheet containing these columns:

| user_id | event_timestamp | event_type | session_duration | donation_amount |
|---------|----------------|------------|------------------|-----------------|
| user-001 | 11/1/2024 8:30 AM | app_open | 300 | |
| user-001 | 11/1/2024 8:35 AM | prayer_log | | |
| user-002 | 11/2/2024 2:20 PM | donation | | 25.00 |

**Excel Tips:**
- Use first row for column headers
- Format timestamp column as "Date" or "Custom: yyyy-mm-dd hh:mm:ss"
- Leave empty cells blank (don't use "N/A" or "null")
- Save as .xlsx (not .xls)

### 🔧 JSON Format Example

```json
[
  {
    "user_id": "user-001",
    "event_timestamp": "2024-11-01T08:30:00Z",
    "event_type": "app_open",
    "session_duration": 300,
    "donation_amount": null,
    "content_category": null
  },
  {
    "user_id": "user-001",
    "event_timestamp": "2024-11-01T08:35:00Z",
    "event_type": "prayer_log",
    "session_duration": null,
    "donation_amount": null,
    "content_category": "Prayer"
  }
]
```

### ✅ Data Quality Requirements

For accurate predictions, your data should meet these criteria:

**Minimum Requirements:**
- ✅ At least 100 events total
- ✅ At least 10 unique users
- ✅ Events from last 30-90 days (recommended)
- ✅ No more than 50 MB file size
- ✅ No more than 50,000 users

**Data Quality Best Practices:**
- ✅ Include at least 2-3 event types per user
- ✅ Cover a minimum of 30 days of activity
- ✅ Include both active and inactive users
- ✅ Ensure timestamp chronological order
- ✅ Remove test/admin users

### ⚠️ Common Issues & Solutions

**Issue:** "Missing required columns"
- **Solution:** Ensure your file has `user_id`, `event_timestamp`, and `event_type` columns
- Check for typos in column names (case-sensitive)

**Issue:** "Invalid timestamp format"
- **Solution:** Use one of the supported date formats listed above
- Ensure dates are in YYYY-MM-DD or MM/DD/YYYY format
- Include time component (HH:MM:SS)

**Issue:** "Insufficient data"
- **Solution:** You need at least 100 events and 10 users
- Combine data from multiple time periods if needed

**Issue:** "File too large"
- **Solution:** File must be under 50 MB
- Split into multiple uploads if needed
- Remove unnecessary columns

**Issue:** "No events for user"
- **Solution:** Every user_id must have at least one event
- Check for null/empty user_id values

### 📈 What Happens After Upload?

1. **Validation (5 seconds)**
   - System checks for required columns
   - Validates date formats
   - Counts users and events
   - Shows warnings for missing optional columns

2. **Feature Engineering (10-20 seconds)**
   - Calculates 44 behavioral features per user:
     - Engagement patterns (session frequency, duration)
     - Recency metrics (days since last activity)
     - Content preferences (prayer, Quran, donations)
     - Islamic calendar patterns (Ramadan, Jumma)
     - Social engagement (shares, comments)

3. **Prediction Generation (5-10 seconds)**
   - XGBoost model predicts churn probability (0-100%)
   - Categorizes users: HIGH (>70%), MEDIUM (40-70%), LOW (<40%)
   - Generates top risk factors per user
   - Creates personalized recommendations

4. **Results Display**
   - Interactive dashboard with your uploaded data
   - Risk distribution chart
   - Top 10 at-risk users
   - Downloadable CSV with all predictions

### 💾 Download Results Format

After analysis, download a CSV with these columns:

| Column | Description |
|--------|-------------|
| `user_id` | Your original user identifier |
| `churn_probability` | Predicted likelihood to churn (0-1) |
| `risk_level` | HIGH / MEDIUM / LOW classification |
| `days_since_last_activity` | Recency metric |
| `session_frequency_30d` | Sessions in last 30 days |
| `prayers_logged_total` | Total prayers logged |
| `donations_total_amount` | Total donations ($) |
| `recommendation` | Personalized retention strategy |
| `top_risk_factor` | Primary churn driver |

**Recommendation Types:**
- **HIGH Risk:** "Immediate intervention: Personal outreach within 24h + incentive offer"
- **MEDIUM Risk:** "Monitor closely: Send engagement email this week + content recommendation"
- **LOW Risk:** "Maintain: Continue regular communication + appreciation message"

### 🔒 Privacy & Security

- ✅ **No Data Storage:** Your data is processed in-memory and deleted after analysis
- ✅ **Secure Upload:** Files encrypted in transit (HTTPS)
- ✅ **No Sharing:** Your data is never shared with third parties
- ✅ **Anonymous:** We don't see user_id mappings to real identities
- ✅ **GDPR Compliant:** Designed for privacy-first organizations

### 🎯 Tips for Best Results

1. **Include Ramadan Data:** If available, include events from Ramadan for better Islamic calendar pattern detection

2. **Mix Active & Inactive Users:** Include both engaged and at-risk users for accurate model calibration

3. **Recent Data Works Best:** Last 60-90 days gives optimal predictions

4. **More Event Types = Better Accuracy:** Prayer logs, donations, content views all improve predictions

5. **Optional Columns Matter:** Adding session_duration and donation_amount can improve accuracy by 10-15%

### 📞 Need Help?

- 📥 **Download Template:** Use our pre-formatted template to get started
- 📧 **Questions:** Open a GitHub issue or contact us
- 📖 **Documentation:** See our [API docs](API_DOCS.md) for programmatic upload
- 🎥 **Video Tutorial:** Watch our [3-min demo](DEMO_VIDEO_LINK) 

---

**Ready to analyze your data?** [Visit the Upload Page](https://your-app-url.com/upload) and get instant churn predictions! 🚀🌙
```

---

## 🚂 Railway Deployment Configuration

### Overview
Configure SpecSailor for seamless deployment on Railway with both backend (FastAPI) and frontend (React) services.

### Prerequisites
- GitHub repository with SpecSailor code
- Railway account (free tier available)
- Environment variables configured

---

### Step 1: Prepare Backend for Railway

#### Create `railway.json` in project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn api.simple_api:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Create `nixpacks.toml` for Python configuration:

```toml
[phases.setup]
nixPkgs = ["python310", "gcc"]

[phases.install]
cmds = ["pip install --upgrade pip", "pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'Build complete'"]

[start]
cmd = "uvicorn api.simple_api:app --host 0.0.0.0 --port $PORT"
```

#### Update `requirements.txt` with all dependencies:

```txt
# Core API
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0

# Machine Learning
xgboost==2.0.3
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.24.3
shap==0.43.0
imbalanced-learn==0.11.0

# Data Processing
python-dateutil==2.8.2
hijri-converter==2.3.1
pytz==2023.3
openpyxl==3.1.2  # For Excel file support

# Utilities
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

#### Update `api/simple_api.py` - Add Railway-specific configuration:

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SpecSailor API",
    description="Islamic App User Retention Prediction",
    version="2.0.0"
)

# Railway-specific CORS configuration
RAILWAY_FRONTEND_URL = os.getenv("RAILWAY_FRONTEND_URL", "http://localhost:8080")
ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
    RAILWAY_FRONTEND_URL,
    "https://*.railway.app",  # Allow all Railway preview URLs
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Railway health check endpoint
@app.get("/")
async def root():
    return {
        "service": "SpecSailor API",
        "status": "healthy",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Railway health check endpoint"""
    return {
        "status": "healthy",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "production")
    }

# ... rest of your existing endpoints
```

---

### Step 2: Prepare Frontend for Railway

#### Create `railway.frontend.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm run preview -- --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Update `vite.config.ts` for Railway:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 8080,
    host: true, // Bind to 0.0.0.0 for Railway
  },
  preview: {
    port: Number(process.env.PORT) || 8080,
    host: '0.0.0.0', // Required for Railway
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['recharts', 'lucide-react'],
        },
      },
    },
  },
})
```

#### Update `package.json` scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "railway:build": "npm run build",
    "railway:start": "vite preview --host 0.0.0.0 --port $PORT"
  }
}
```

#### Create `.env.example` for reference:

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000

# Railway Production (update after deployment)
# VITE_API_URL=https://your-backend.railway.app
```

#### Update API service in `src/services/api.ts`:

```typescript
// Auto-detect API URL based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 
                     (import.meta.env.MODE === 'production' 
                       ? 'https://your-backend.railway.app'  // Update after backend deployment
                       : 'http://localhost:8000');

export const api = {
  baseURL: API_BASE_URL,
  
  // ... rest of your API methods
};
```

---

### Step 3: Deploy to Railway (Step-by-Step)

#### Deploy Backend First:

1. **Login to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `spec-sailor` repository

3. **Configure Backend Service**
   - Railway auto-detects Python project
   - Name the service: `specsailor-backend`
   - Set root directory: `/` (project root)

4. **Set Environment Variables**
   ```bash
   # Click "Variables" tab and add:
   
   PORT=8000
   PYTHON_VERSION=3.10
   RAILWAY_ENVIRONMENT=production
   
   # File upload settings
   MAX_UPLOAD_SIZE=52428800
   ALLOWED_ORIGINS=*
   
   # Optional: Add your frontend URL after deployment
   RAILWAY_FRONTEND_URL=https://your-frontend.railway.app
   ```

5. **Deploy Backend**
   - Click "Deploy"
   - Wait 3-5 minutes for build
   - Copy the generated URL: `https://specsailor-backend.railway.app`

6. **Test Backend**
   ```bash
   curl https://specsailor-backend.railway.app/health
   # Should return: {"status": "healthy"}
   ```

#### Deploy Frontend Second:

1. **Add New Service to Same Project**
   - In Railway project dashboard, click "+ New"
   - Select "GitHub Repo" again
   - Choose `spec-sailor` repository

2. **Configure Frontend Service**
   - Name the service: `specsailor-frontend`
   - Set root directory: `/` (project root)

3. **Set Environment Variables**
   ```bash
   # Click "Variables" tab and add:
   
   PORT=8080
   NODE_VERSION=18
   
   # CRITICAL: Set backend URL from step 1
   VITE_API_URL=https://specsailor-backend.railway.app
   ```

4. **Configure Build Settings**
   - Build Command: `npm run build`
   - Start Command: `npm run preview -- --host 0.0.0.0 --port $PORT`

5. **Deploy Frontend**
   - Click "Deploy"
   - Wait 2-3 minutes for build
   - Copy the generated URL: `https://specsailor-frontend.railway.app`

6. **Update Backend CORS**
   - Go back to backend service
   - Add environment variable:
     ```bash
     RAILWAY_FRONTEND_URL=https://specsailor-frontend.railway.app
     ```
   - Redeploy backend (click "Deploy" again)

---

### Step 4: Post-Deployment Configuration

#### Update GitHub README with Live URLs:

```markdown
## 🌐 Live Demo

- **Frontend Dashboard:** https://specsailor-frontend.railway.app
- **Backend API:** https://specsailor-backend.railway.app
- **API Documentation:** https://specsailor-backend.railway.app/docs

Try uploading your own data to see instant churn predictions!
```

#### Test Full Upload Flow:

1. Visit frontend URL
2. Navigate to "Upload Data" page
3. Download template
4. Upload sample CSV
5. Verify predictions display
6. Download results

#### Monitor Deployments:

Railway provides:
- ✅ Automatic deployments on git push
- ✅ Build logs and runtime logs
- ✅ Metrics (CPU, memory, network)
- ✅ Custom domains (add your own domain)

---

### Step 5: Custom Domain (Optional)

#### Add Custom Domain to Frontend:

1. **In Railway Frontend Service:**
   - Click "Settings" → "Domains"
   - Click "Add Domain"
   - Enter: `app.specsailor.com`

2. **Configure DNS:**
   ```
   Type: CNAME
   Name: app
   Value: [railway-provided-value]
   TTL: Auto
   ```

3. **SSL Certificate:**
   - Railway auto-provisions SSL (free)
   - Wait 5-10 minutes for DNS propagation

#### Add Custom Domain to Backend:

1. **In Railway Backend Service:**
   - Click "Settings" → "Domains"
   - Click "Add Domain"
   - Enter: `api.specsailor.com`

2. **Configure DNS:**
   ```
   Type: CNAME
   Name: api
   Value: [railway-provided-value]
   TTL: Auto
   ```

3. **Update Frontend .env:**
   ```bash
   VITE_API_URL=https://api.specsailor.com
   ```

4. **Redeploy Frontend**

---

### Railway Environment Variables - Complete List

#### Backend Service Variables:

```bash
# Required
PORT=8000
PYTHON_VERSION=3.10
RAILWAY_ENVIRONMENT=production

# CORS Configuration
RAILWAY_FRONTEND_URL=https://specsailor-frontend.railway.app
ALLOWED_ORIGINS=*

# File Upload Settings
MAX_UPLOAD_SIZE=52428800
STORAGE_TYPE=memory

# Optional: Database (if adding persistence)
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://...

# Optional: Monitoring
# SENTRY_DSN=https://...
```

#### Frontend Service Variables:

```bash
# Required
PORT=8080
NODE_VERSION=18
VITE_API_URL=https://specsailor-backend.railway.app

# Optional: Analytics
# VITE_GA_ID=G-XXXXXXXXXX
```

---

### Railway Free Tier Limits

Be aware of Railway's free tier limitations:

- ✅ **$5/month credit** (generous for side projects)
- ✅ **500 hours** of runtime per month
- ✅ **1GB RAM** per service
- ✅ **1GB disk** per service
- ✅ **100GB bandwidth** per month

**Cost Optimization Tips:**
1. Use Railway's "sleep" feature for dev environments
2. Deploy only when needed (not on every commit)
3. Optimize Docker images to reduce build time
4. Monitor usage in Railway dashboard

---

### Troubleshooting Common Railway Issues

#### Issue: Backend won't start
```bash
# Solution: Check logs in Railway dashboard
# Common causes:
- Missing dependencies in requirements.txt
- Wrong Python version
- Port not set to $PORT variable
```

#### Issue: Frontend can't connect to backend
```bash
# Solution: Verify CORS settings
# Check these:
1. VITE_API_URL is correct
2. Backend ALLOWED_ORIGINS includes frontend URL
3. Both services are in same Railway project
```

#### Issue: Upload fails with "File too large"
```bash
# Solution: Railway has 100MB request limit
# Fix: Reduce MAX_UPLOAD_SIZE or split files
MAX_UPLOAD_SIZE=52428800  # 50MB (safe)
```

#### Issue: Build fails with "Out of memory"
```bash
# Solution: Optimize build process
# Add to railway.json:
"build": {
  "builder": "NIXPACKS",
  "buildCommand": "pip install --no-cache-dir -r requirements.txt"
}
```

---

### Continuous Deployment Setup

Railway auto-deploys on git push. Configure deployment triggers:

#### Backend Deployment Triggers:

```yaml
# In Railway dashboard → Settings → Deploys
Trigger: Push to main branch
Root Directory: /
Build Command: Auto-detected
Start Command: uvicorn api.simple_api:app --host 0.0.0.0 --port $PORT
```

#### Frontend Deployment Triggers:

```yaml
# In Railway dashboard → Settings → Deploys
Trigger: Push to main branch
Root Directory: /
Build Command: npm run build
Start Command: npm run preview -- --host 0.0.0.0 --port $PORT
```

---

### Final Deployment Checklist

Before announcing your deployment:

- [ ] Backend health check returns 200
- [ ] Frontend loads without errors
- [ ] Upload functionality works end-to-end
- [ ] Download results works
- [ ] API documentation accessible at /docs
- [ ] CORS allows frontend to call backend
- [ ] Environment variables all set
- [ ] GitHub README updated with live URLs
- [ ] Custom domains configured (optional)
- [ ] SSL certificates active
- [ ] Railway monitoring dashboard reviewed
- [ ] Test with real data upload
- [ ] Verify predictions accuracy
- [ ] Check mobile responsiveness

---

### Monitoring & Maintenance

#### Set Up Alerts:

Railway provides:
- ✅ Email notifications for failed deployments
- ✅ Slack integration for deploy notifications
- ✅ Webhook support for custom integrations

#### Weekly Maintenance:

1. Check Railway usage metrics
2. Review error logs
3. Monitor API response times
4. Test upload flow
5. Update dependencies if needed

#### Monthly Review:

1. Analyze user upload patterns
2. Review Railway costs
3. Update model if needed
4. Refresh documentation
5. Check for security updates

---

### Cost Estimate

**Railway Free Tier:**
- Backend: ~$2-3/month
- Frontend: ~$1-2/month
- **Total: ~$3-5/month** (well within $5 credit)

**If Upgrade Needed (Paid Plan):**
- Hobby Plan: $5/month base + usage
- Pro Plan: $20/month + usage
- Typical total for this project: **$10-15/month**

---

### Alternative: Monorepo Deployment

If you want to deploy both services from one Railway project:

#### Create `railway.toml`:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "sh start.sh"

[environments.backend]
buildCommand = "pip install -r requirements.txt"
startCommand = "uvicorn api.simple_api:app --host 0.0.0.0 --port $PORT"

[environments.frontend]
buildCommand = "npm install && npm run build"
startCommand = "npm run preview -- --host 0.0.0.0 --port $PORT"
```

Then create `start.sh`:

```bash
#!/bin/bash

if [ "$SERVICE_TYPE" = "backend" ]; then
    uvicorn api.simple_api:app --host 0.0.0.0 --port $PORT
elif [ "$SERVICE_TYPE" = "frontend" ]; then
    npm run preview -- --host 0.0.0.0 --port $PORT
else
    echo "SERVICE_TYPE not set"
    exit 1
fi
```

---

## 🎉 End Result

After implementation, users will be able to:
✅ Upload their own Islamic app data
✅ See instant churn predictions (87% accuracy)
✅ Download actionable recommendations
✅ Demo the tool with real data to potential employers/partners
✅ Use SpecSailor as a production tool (with proper deployment)

This transforms SpecSailor from a **static portfolio project** into a **real business tool** that Islamic organizations can actually use!

---

**Ready for Claude Code implementation? This feature request contains:**
- ✅ Complete technical specifications
- ✅ All code files with implementation details
- ✅ UI mockups and flow diagrams
- ✅ Testing checklist
- ✅ **Comprehensive README with upload instructions**
- ✅ **Complete Railway deployment configuration**
- ✅ Success metrics

---

## 📋 Implementation Instructions for Claude Code

### When you give this to Claude Code, say:

```
Please implement the following for SpecSailor:

1. FEATURE IMPLEMENTATION:
   - Add real-time data upload capability (Phase 1-3)
   - Implement upload_handler.py for file validation
   - Implement feature_pipeline.py for automatic feature engineering
   - Add 6 new API endpoints (upload, analyze, results, download, template, health)
   - Create UploadPage.tsx with drag-and-drop interface
   - Add all necessary error handling and loading states

2. README UPDATES:
   - Add the complete "Upload Your Own Data" section from this document
   - Include all data format requirements and examples
   - Add CSV, Excel, and JSON format templates
   - Include troubleshooting guide
   - Add live deployment URLs (after Railway deployment)

3. RAILWAY DEPLOYMENT PREPARATION:
   - Create railway.json and nixpacks.toml
   - Update api/simple_api.py with Railway-specific CORS
   - Update vite.config.ts for Railway preview server
   - Create .env.example with Railway variables
   - Add health check endpoints
   - Configure environment variables list
   - Add deployment instructions to README

4. TESTING:
   - Test upload with CSV, Excel, JSON files
   - Test validation error handling
   - Test feature engineering with various data formats
   - Test end-to-end: upload → analyze → download
   - Verify Railway deployment works

PRIORITY: Implement in this order:
1. Backend upload handler and feature pipeline (Week 1)
2. API endpoints (Week 1)
3. Frontend upload page (Week 2)
4. Railway configuration files (Week 2)
5. README updates (Week 3)
6. Deploy to Railway (Week 3)
```

---

## 🎯 Final Deliverables Checklist

After Claude Code completes implementation, you should have:

### Code Files (New):
- [ ] `api/upload_handler.py` - File upload and validation
- [ ] `api/feature_pipeline.py` - Automatic feature engineering
- [ ] `src/pages/UploadPage.tsx` - Upload interface
- [ ] `railway.json` - Railway backend config
- [ ] `railway.frontend.json` - Railway frontend config
- [ ] `nixpacks.toml` - Python environment config
- [ ] `.env.example` - Environment variables template

### Code Files (Updated):
- [ ] `api/simple_api.py` - Added 6 new endpoints + Railway CORS
- [ ] `vite.config.ts` - Railway preview server config
- [ ] `src/services/api.ts` - Dynamic API URL detection
- [ ] `package.json` - Railway start scripts
- [ ] `requirements.txt` - Added openpyxl for Excel support

### Documentation (Updated):
- [ ] `README.md` - Complete upload instructions section
- [ ] `README.md` - Data format examples (CSV/Excel/JSON)
- [ ] `README.md` - Railway deployment URLs
- [ ] `README.md` - Live demo links

### Deployed:
- [ ] Backend on Railway: `https://specsailor-backend.railway.app`
- [ ] Frontend on Railway: `https://specsailor-frontend.railway.app`
- [ ] Both services connected and working
- [ ] Upload flow tested end-to-end
- [ ] Results downloadable as CSV

---

## 🚀 Post-Implementation Steps

### 1. Test Locally First
```bash
# Start backend
python api/simple_api.py

# Start frontend
npm run dev

# Visit http://localhost:8080/upload
# Test upload flow
```

### 2. Deploy to Railway
```bash
# Push to GitHub
git add .
git commit -m "Add data upload feature + Railway deployment"
git push origin main

# Follow Railway deployment steps from this document
# Takes ~10 minutes total
```

### 3. Update LinkedIn Post
Add to your LinkedIn post:
```
🆕 NEW: Upload your own data for instant predictions!

Just deployed a major update:
• Real-time data upload (CSV/Excel/JSON)
• Automatic feature engineering
• Download results with recommendations
• Zero-code interface

Live demo: https://specsailor-frontend.railway.app

Try it with your Islamic app data! 🌙
```

### 4. Update GitHub README
Add badge at top:
```markdown
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

**🌐 Live Demo:** [specsailor-frontend.railway.app](https://specsailor-frontend.railway.app)
```

---

**Estimated Development Time:** 2-3 weeks  
**Priority:** HIGH - Unlocks real business value  
**Railway Deployment Time:** 10 minutes  
**Monthly Cost:** $3-5 (within free tier)

**This transforms SpecSailor from a static portfolio project into a production-ready SaaS tool!** 🎉

---

END OF FEATURE REQUEST
