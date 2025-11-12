"""
Pydantic Models for API Request/Response Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., example="healthy")
    model_loaded: bool = Field(..., example=True)
    model_version: str = Field(..., example="1.0.0")
    timestamp: str = Field(..., example="2024-11-11T12:00:00")


class UserFeatures(BaseModel):
    """User features for prediction"""
    user_id: str = Field(..., example="user-000123")
    days_since_last_session: int = Field(..., ge=0, example=15)
    session_frequency_7d: int = Field(..., ge=0, example=5)
    session_frequency_30d: int = Field(..., ge=0, example=20)
    avg_session_duration: float = Field(..., ge=0, example=12.5)
    total_sessions: int = Field(..., ge=0, example=100)
    streak_current: int = Field(..., ge=0, example=0)
    streak_longest: int = Field(..., ge=0, example=15)
    days_since_signup: int = Field(..., ge=0, example=180)
    sessions_per_week: float = Field(..., ge=0, example=3.5)
    weekend_activity_ratio: float = Field(..., ge=0, le=1, example=0.3)
    ramadan_engagement_ratio: float = Field(..., ge=0, example=2.5)
    is_ramadan_convert: int = Field(..., ge=0, le=1, example=1)
    days_since_ramadan: int = Field(..., example=200)
    last_10_nights_sessions: int = Field(..., ge=0, example=8)
    jummah_participation_rate: float = Field(..., ge=0, le=1, example=0.7)
    prayer_time_interaction_rate: float = Field(..., ge=0, le=1, example=0.4)
    eid_participation: int = Field(..., ge=0, le=1, example=1)
    muharram_participation: int = Field(..., ge=0, le=1, example=0)
    quran_reading_pct: float = Field(..., ge=0, le=1, example=0.35)
    hadith_engagement_pct: float = Field(..., ge=0, le=1, example=0.20)
    lecture_watch_minutes: float = Field(..., ge=0, example=120.5)
    fiqh_content_views: int = Field(..., ge=0, example=15)
    seerah_content_views: int = Field(..., ge=0, example=10)
    tafsir_engagement: int = Field(..., ge=0, example=5)
    topic_diversity_score: float = Field(..., ge=0, example=5.0)
    content_completion_rate: float = Field(..., ge=0, le=1, example=0.6)
    bookmark_count: int = Field(..., ge=0, example=25)
    friends_count: int = Field(..., ge=0, example=50)
    shares_sent: int = Field(..., ge=0, example=10)
    comments_made: int = Field(..., ge=0, example=15)
    days_since_last_social: int = Field(..., ge=0, example=5)


class PredictionRequest(BaseModel):
    """Batch prediction request"""
    users: List[UserFeatures] = Field(..., min_items=1, max_items=1000)


class PredictionResponse(BaseModel):
    """Single user prediction response"""
    user_id: str = Field(..., example="user-000123")
    churn_probability: float = Field(..., ge=0, le=1, example=0.75)
    risk_level: RiskLevel = Field(..., example=RiskLevel.HIGH)
    top_risk_factors: List[str] = Field(..., example=[
        "User hasn't opened app in 15 days (+18% risk)",
        "User was 5x more active during Ramadan (+15% risk)",
        "No activity in last 10 days (+12% risk)"
    ])


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: List[PredictionResponse]
    total_users: int = Field(..., example=100)
    high_risk_count: int = Field(..., example=30)
    medium_risk_count: int = Field(..., example=40)
    low_risk_count: int = Field(..., example=30)


class FeatureContribution(BaseModel):
    """Single feature contribution to prediction"""
    feature: str = Field(..., example="days_since_last_session")
    value: float = Field(..., example=15.0)
    shap_value: float = Field(..., example=0.18)
    impact: str = Field(..., example="increases")
    explanation: str = Field(..., example="User hasn't opened app in 15 days")


class SHAPExplanation(BaseModel):
    """SHAP explanation for a prediction"""
    user_id: str = Field(..., example="user-000123")
    churn_probability: float = Field(..., ge=0, le=1, example=0.75)
    risk_level: RiskLevel = Field(..., example=RiskLevel.HIGH)
    base_value: float = Field(..., example=0.30)
    prediction: float = Field(..., example=0.75)
    top_positive_contributors: List[FeatureContribution] = Field(..., max_items=10)
    top_negative_contributors: List[FeatureContribution] = Field(..., max_items=10)
    explanations: List[str] = Field(..., example=[
        "🔴 User hasn't opened app in 15 days (increases churn risk by 18.0%)",
        "🟢 User has 50 friends (decreases churn risk by 5.0%)"
    ])


class FeatureImportance(BaseModel):
    """Feature importance from model"""
    feature: str = Field(..., example="days_since_last_session")
    importance: float = Field(..., ge=0, example=150.5)
    rank: int = Field(..., ge=1, example=1)


class FeatureImportanceResponse(BaseModel):
    """Feature importance response"""
    features: List[FeatureImportance]
    total_features: int = Field(..., example=32)


class ModelMetrics(BaseModel):
    """Model performance metrics"""
    accuracy: float = Field(..., ge=0, le=1, example=0.87)
    precision: float = Field(..., ge=0, le=1, example=0.84)
    recall: float = Field(..., ge=0, le=1, example=0.79)
    f1_score: float = Field(..., ge=0, le=1, example=0.81)
    roc_auc: float = Field(..., ge=0, le=1, example=0.92)


class ConfusionMatrix(BaseModel):
    """Confusion matrix"""
    true_negatives: int = Field(..., example=850)
    false_positives: int = Field(..., example=50)
    false_negatives: int = Field(..., example=30)
    true_positives: int = Field(..., example=70)


class ModelPerformanceResponse(BaseModel):
    """Model performance response"""
    metrics: ModelMetrics
    confusion_matrix: ConfusionMatrix
    training_date: str = Field(..., example="2024-11-11")
    model_type: str = Field(..., example="XGBoost")
    target_achieved: bool = Field(..., example=True)


class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., example="User not found")
    detail: Optional[str] = Field(None, example="User ID user-999999 does not exist")
    code: Optional[str] = Field(None, example="USER_NOT_FOUND")
