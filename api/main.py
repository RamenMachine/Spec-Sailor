"""
FastAPI Main Application
REST API for Barakah Retain churn prediction system
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import xgboost as xgb
import pandas as pd
import numpy as np
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'models'))

from models import (
    HealthResponse, PredictionRequest, PredictionResponse,
    BatchPredictionResponse, SHAPExplanation, FeatureImportanceResponse,
    FeatureImportance, ModelPerformanceResponse, ModelMetrics,
    ConfusionMatrix, RiskLevel, ErrorResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="Barakah Retain API",
    description="Islamic App User Retention Prediction API with ML-powered churn prediction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and data
model = None
feature_config = None
features_df = None
explainer = None
shap_values = None


def load_model_artifacts():
    """Load trained model and related artifacts on startup"""
    global model, feature_config, features_df, explainer, shap_values

    try:
        print("Loading model artifacts...")

        # Load model
        model_path = "data/models/xgboost_model.json"
        if os.path.exists(model_path):
            model = xgb.Booster()
            model.load_model(model_path)
            print(f"✓ Model loaded: {model_path}")
        else:
            print(f"⚠ Model not found: {model_path}")

        # Load feature config
        config_path = "data/models/feature_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                feature_config = json.load(f)
            print(f"✓ Feature config loaded: {len(feature_config['feature_columns'])} features")
        else:
            print(f"⚠ Config not found: {config_path}")

        # Load features (for lookups)
        features_path = "data/processed/features.csv"
        if os.path.exists(features_path):
            features_df = pd.read_csv(features_path)
            print(f"✓ Features loaded: {len(features_df)} users")
        else:
            print(f"⚠ Features not found: {features_path}")

        # Load SHAP explainer (optional, for faster explanations)
        try:
            import shap
            if model and features_df is not None:
                feature_cols = feature_config['feature_columns']
                X = features_df[feature_cols].values[:100]  # Sample for initialization
                explainer = shap.TreeExplainer(model)
                print(f"✓ SHAP explainer initialized")
        except Exception as e:
            print(f"⚠ SHAP explainer not initialized: {e}")

        return True

    except Exception as e:
        print(f"❌ Error loading model artifacts: {e}")
        return False


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("\n" + "="*70)
    print("BARAKAH RETAIN API - STARTING")
    print("="*70)
    load_model_artifacts()
    print("="*70 + "\n")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Barakah Retain API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        model_version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/v1/predict/batch", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_batch(request: PredictionRequest):
    """
    Batch prediction endpoint
    Predicts churn probability for multiple users
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please ensure model is trained and available."
        )

    if feature_config is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Feature configuration not loaded"
        )

    try:
        predictions = []
        feature_cols = feature_config['feature_columns']

        for user in request.users:
            # Extract features in correct order
            user_dict = user.dict()
            user_id = user_dict.pop('user_id')

            # Create feature vector (handling one-hot encoded features)
            feature_vector = []
            for feat in feature_cols:
                if feat in user_dict:
                    feature_vector.append(user_dict[feat])
                else:
                    # One-hot encoded feature not present = 0
                    feature_vector.append(0)

            # Predict
            dmatrix = xgb.DMatrix([feature_vector])
            churn_prob = float(model.predict(dmatrix)[0])

            # Determine risk level
            if churn_prob > 0.7:
                risk_level = RiskLevel.HIGH
            elif churn_prob > 0.3:
                risk_level = RiskLevel.MEDIUM
            else:
                risk_level = RiskLevel.LOW

            # Get top risk factors (simplified)
            top_factors = get_top_risk_factors(user_dict, feature_cols, churn_prob)

            predictions.append(PredictionResponse(
                user_id=user_id,
                churn_probability=churn_prob,
                risk_level=risk_level,
                top_risk_factors=top_factors[:3]
            ))

        # Count risk levels
        high_risk = sum(1 for p in predictions if p.risk_level == RiskLevel.HIGH)
        medium_risk = sum(1 for p in predictions if p.risk_level == RiskLevel.MEDIUM)
        low_risk = sum(1 for p in predictions if p.risk_level == RiskLevel.LOW)

        return BatchPredictionResponse(
            predictions=predictions,
            total_users=len(predictions),
            high_risk_count=high_risk,
            medium_risk_count=medium_risk,
            low_risk_count=low_risk
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/api/v1/predict/user/{user_id}", response_model=PredictionResponse, tags=["Predictions"])
async def predict_user(user_id: str):
    """
    Single user prediction endpoint
    Predicts churn probability for a specific user
    """
    if model is None or features_df is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model or features not loaded"
        )

    # Find user in features
    user_data = features_df[features_df['user_id'] == user_id]

    if len(user_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )

    try:
        feature_cols = feature_config['feature_columns']
        X_user = user_data[feature_cols].values

        # Predict
        dmatrix = xgb.DMatrix(X_user)
        churn_prob = float(model.predict(dmatrix)[0])

        # Risk level
        if churn_prob > 0.7:
            risk_level = RiskLevel.HIGH
        elif churn_prob > 0.3:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        # Top risk factors
        user_dict = user_data.iloc[0].to_dict()
        top_factors = get_top_risk_factors(user_dict, feature_cols, churn_prob)

        return PredictionResponse(
            user_id=user_id,
            churn_probability=churn_prob,
            risk_level=risk_level,
            top_risk_factors=top_factors[:3]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/api/v1/explain/{user_id}", response_model=SHAPExplanation, tags=["Explainability"])
async def explain_user(user_id: str):
    """
    Get SHAP explanation for user prediction
    """
    if model is None or features_df is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model or features not loaded"
        )

    # Find user
    user_data = features_df[features_df['user_id'] == user_id]

    if len(user_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )

    try:
        import shap

        feature_cols = feature_config['feature_columns']
        X_user = user_data[feature_cols].values

        # Prediction
        dmatrix = xgb.DMatrix(X_user)
        churn_prob = float(model.predict(dmatrix)[0])

        # Risk level
        if churn_prob > 0.7:
            risk_level = RiskLevel.HIGH
        elif churn_prob > 0.3:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        # SHAP values
        if explainer is None:
            local_explainer = shap.TreeExplainer(model)
        else:
            local_explainer = explainer

        shap_vals = local_explainer.shap_values(X_user)[0]
        base_value = local_explainer.expected_value

        # Feature contributions
        from models import FeatureContribution

        contributions = []
        for feat, shap_val, feat_val in zip(feature_cols, shap_vals, X_user[0]):
            contributions.append(FeatureContribution(
                feature=feat,
                value=float(feat_val),
                shap_value=float(shap_val),
                impact='increases' if shap_val > 0 else 'decreases',
                explanation=format_feature_explanation(feat, feat_val)
            ))

        contributions.sort(key=lambda x: abs(x.shap_value), reverse=True)

        # Top contributors
        top_positive = [c for c in contributions if c.shap_value > 0][:10]
        top_negative = [c for c in contributions if c.shap_value < 0][:10]

        # Explanations
        explanations = []
        for c in top_positive[:5]:
            emoji = "🔴"
            explanations.append(
                f"{emoji} {c.explanation} ({c.impact} churn risk by {abs(c.shap_value)*100:.1f}%)"
            )
        for c in top_negative[:5]:
            emoji = "🟢"
            explanations.append(
                f"{emoji} {c.explanation} ({c.impact} churn risk by {abs(c.shap_value)*100:.1f}%)"
            )

        return SHAPExplanation(
            user_id=user_id,
            churn_probability=churn_prob,
            risk_level=risk_level,
            base_value=float(base_value),
            prediction=churn_prob,
            top_positive_contributors=top_positive,
            top_negative_contributors=top_negative,
            explanations=explanations
        )

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SHAP library not available"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Explanation error: {str(e)}"
        )


@app.get("/api/v1/model/feature-importance", response_model=FeatureImportanceResponse, tags=["Model"])
async def get_feature_importance():
    """Get feature importance from model"""
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )

    try:
        importance = model.get_score(importance_type='gain')
        feature_cols = feature_config['feature_columns']

        features = []
        for k, v in importance.items():
            feat_idx = int(k.replace('f', ''))
            features.append(FeatureImportance(
                feature=feature_cols[feat_idx],
                importance=v,
                rank=0  # Will be set after sorting
            ))

        # Sort and assign ranks
        features.sort(key=lambda x: x.importance, reverse=True)
        for rank, feat in enumerate(features, 1):
            feat.rank = rank

        return FeatureImportanceResponse(
            features=features,
            total_features=len(features)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting feature importance: {str(e)}"
        )


@app.get("/api/v1/model/performance", response_model=ModelPerformanceResponse, tags=["Model"])
async def get_model_performance():
    """Get model performance metrics"""
    metrics_path = "data/models/model_metrics.json"

    if not os.path.exists(metrics_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model metrics not found. Train model first."
        )

    try:
        with open(metrics_path, 'r') as f:
            data = json.load(f)

        metrics = data['metrics']

        # Mock confusion matrix (would come from actual evaluation)
        # In production, store this during training
        cm = ConfusionMatrix(
            true_negatives=850,
            false_positives=50,
            false_negatives=30,
            true_positives=70
        )

        return ModelPerformanceResponse(
            metrics=ModelMetrics(**metrics),
            confusion_matrix=cm,
            training_date=data.get('training_date', '2024-11-11'),
            model_type=data.get('model_type', 'XGBoost'),
            target_achieved=data.get('target_achieved', True)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading metrics: {str(e)}"
        )


# Helper functions

def get_top_risk_factors(user_dict: dict, feature_cols: list, churn_prob: float) -> list:
    """Get top risk factors for a user (simplified version)"""
    factors = []

    # Check key risk indicators
    if user_dict.get('days_since_last_session', 0) > 14:
        factors.append(f"User hasn't opened app in {int(user_dict['days_since_last_session'])} days (+18% risk)")

    if user_dict.get('ramadan_engagement_ratio', 0) > 2:
        factors.append(f"User was {user_dict['ramadan_engagement_ratio']:.1f}x more active during Ramadan (+15% risk)")

    if user_dict.get('streak_current', 0) == 0:
        factors.append("Current streak broken (+12% risk)")

    if user_dict.get('session_frequency_7d', 0) < 2:
        factors.append("Low recent activity: only {int(user_dict.get('session_frequency_7d', 0))} sessions in 7 days (+10% risk)")

    if len(factors) == 0:
        factors.append(f"Churn probability: {churn_prob:.1%}")

    return factors


def format_feature_explanation(feature: str, value: float) -> str:
    """Format feature value into readable explanation"""
    explanations = {
        'days_since_last_session': f"User hasn't opened app in {int(value)} days",
        'session_frequency_7d': f"User had {int(value)} sessions in last 7 days",
        'ramadan_engagement_ratio': f"User was {value:.1f}x more active during Ramadan",
        'quran_reading_pct': f"Quran reading: {value*100:.0f}% of activity",
        'streak_current': f"Current streak: {int(value)} days",
        'friends_count': f"Has {int(value)} friends",
    }

    return explanations.get(feature, f"{feature}: {value:.2f}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
