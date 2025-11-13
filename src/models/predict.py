"""
Prediction module for Telco Customer Churn
Loads trained model and makes predictions on new customer data
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import xgboost as xgb


def predict_churn(
    customer_data: pd.DataFrame,
    model_path: str = "data/models/xgboost_telco_model.pkl",
    scaler_path: str = "data/models/feature_scaler.pkl"
) -> pd.DataFrame:
    """
    Predict churn probability for customer data
    
    Args:
        customer_data: DataFrame with customer features (must match training features)
        model_path: Path to trained XGBoost model
        scaler_path: Path to feature scaler
    
    Returns:
        DataFrame with predictions including:
        - customerID (if present)
        - churn_probability
        - churn_prediction (0/1)
        - risk_level ('HIGH', 'MEDIUM', 'LOW')
    """
    # Load model and scaler
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    # Prepare features
    if 'customerID' in customer_data.columns:
        customer_ids = customer_data['customerID']
        X = customer_data.drop(columns=['customerID'])
    else:
        customer_ids = None
        X = customer_data.copy()
    
    # Scale numeric features
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    one_hot_cols = [col for col in X.columns if any(
        prefix in col for prefix in ['household_type_', 'tenure_group_', 'internet_type_', 
                                     'contract_type_', 'payment_method_', 'churn_likelihood_segment_']
    )]
    numeric_cols = [col for col in numeric_cols if col not in one_hot_cols]
    
    X_scaled = X.copy()
    if len(numeric_cols) > 0:
        X_scaled[numeric_cols] = scaler.transform(X[numeric_cols])
    
    # Make predictions
    dtest = xgb.DMatrix(X_scaled)
    churn_probabilities = model.predict(dtest)
    churn_predictions = (churn_probabilities >= 0.5).astype(int)
    
    # Determine risk levels
    def get_risk_level(prob):
        if prob >= 0.70:
            return 'HIGH'
        elif prob >= 0.30:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    risk_levels = [get_risk_level(prob) for prob in churn_probabilities]
    
    # Create results DataFrame
    results = pd.DataFrame({
        'churn_probability': churn_probabilities,
        'churn_prediction': churn_predictions,
        'risk_level': risk_levels
    })
    
    if customer_ids is not None:
        results.insert(0, 'customerID', customer_ids)
    
    return results

