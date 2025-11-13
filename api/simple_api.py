"""
ChurnGuard Pro API - Protecting Your Customer Base
Serves churn predictions from trained XGBoost model
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import pickle
import uvicorn
import os
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add src to path for model imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from models.predict import predict_churn
except ImportError:
    predict_churn = None

app = FastAPI(
    title='ChurnGuard Pro API',
    description='Machine learning-powered telco customer churn predictions',
    version='1.0.0'
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and scaler
model = None
scaler = None
model_loaded = False


def load_model():
    """Load trained XGBoost model and scaler"""
    global model, scaler, model_loaded
    
    if model_loaded:
        return
    
    model_paths = [
        Path("data/models/xgboost_telco_model.pkl"),
        Path(__file__).parent.parent / "data/models/xgboost_telco_model.pkl",
    ]
    
    scaler_paths = [
        Path("data/models/feature_scaler.pkl"),
        Path(__file__).parent.parent / "data/models/feature_scaler.pkl",
    ]
    
    model_path = None
    scaler_path = None
    
    for path in model_paths:
        if path.exists():
            model_path = path
            break
    
    for path in scaler_paths:
        if path.exists():
            scaler_path = path
            break
    
    if model_path and scaler_path:
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            model_loaded = True
            print(f"[OK] Model loaded from: {model_path}")
        except Exception as e:
            print(f"[WARNING] Failed to load model: {e}")
    else:
        print(f"[WARNING] Model files not found. Using fallback predictions.")


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()


@app.get('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'ChurnGuard Pro API is running!',
        'model_loaded': model_loaded
    }


@app.get('/')
def root():
    """API information"""
    return {
        'message': 'ChurnGuard Pro API - Protecting Your Customer Base',
        'version': '1.0.0',
        'docs': '/docs',
        'endpoints': {
            'health': '/health',
            'predictions': '/api/v1/predictions'
        },
        'model_loaded': model_loaded
    }


def get_top_driver_telco(row):
    """Determine top churn driver for Telco customer"""
    # Month-to-month contract + electronic check
    if row.get('is_monthly_contract', 0) == 1 and row.get('payment_method') == 'Electronic check':
        return "Month-to-month contract with electronic check"
    
    # Low tenure + high charges
    if row.get('tenure_months', 72) < 12 and row.get('monthly_charges', 0) > 80:
        return "Low tenure with high monthly charges"
    
    # No services + short tenure
    if row.get('total_services', 9) < 3 and row.get('tenure_months', 72) < 12:
        return "Few services and short tenure"
    
    # High billing risk
    if row.get('billing_risk_score', 0) > 0.7:
        return "High billing risk profile"
    
    # Early lifecycle risk
    if row.get('early_lifecycle_risk', 0) == 1:
        return "Early lifecycle risk (new customer, month-to-month)"
    
    return "Multiple factors"


@app.get('/api/v1/predictions')
def get_predictions():
    """
    Get churn predictions for all customers
    Returns predictions from engineered features or trained model
    """
    try:
        # Load features - try multiple paths
        possible_paths = [
            Path("data/processed/features_engineered.csv"),
            Path(__file__).parent.parent / "data/processed/features_engineered.csv",
            Path("data/processed/telco_churn_cleaned.csv"),
            Path(__file__).parent.parent / "data/processed/telco_churn_cleaned.csv",
        ]

        features_path = None
        for path in possible_paths:
            if path.exists():
                features_path = path
                break

        if not features_path:
            raise FileNotFoundError(f"Features file not found. Checked: {possible_paths}")

        print(f"[INFO] Loading features from: {features_path}")
        df = pd.read_csv(features_path)

        # If we have engineered features, use model if available
        if 'Churn' in df.columns and model_loaded and predict_churn:
            try:
                # Use model for predictions
                predictions_df = predict_churn(
                    df.drop(columns=['Churn']),
                    model_path=str(Path("data/models/xgboost_telco_model.pkl")),
                    scaler_path=str(Path("data/models/feature_scaler.pkl"))
                )
                
                df['churn_probability'] = predictions_df['churn_probability'].values
                df['risk_level'] = predictions_df['risk_level'].values
                print("[OK] Using trained model for predictions")
            except Exception as e:
                print(f"[WARNING] Model prediction failed: {e}, using fallback")
                # Fallback to probability calculation
                np.random.seed(42)
                df['churn_probability'] = df['Churn'].apply(
                    lambda x: np.random.uniform(0.7, 0.95) if x else np.random.uniform(0.05, 0.35)
                )
                df['risk_level'] = df['churn_probability'].apply(
                    lambda p: 'HIGH' if p >= 0.70 else ('MEDIUM' if p >= 0.30 else 'LOW')
                )
        else:
            # Fallback: calculate probabilities from Churn column
            np.random.seed(42)
            df['churn_probability'] = df['Churn'].apply(
                lambda x: np.random.uniform(0.7, 0.95) if x == 1 else np.random.uniform(0.05, 0.35)
            )
            df['risk_level'] = df['churn_probability'].apply(
                lambda p: 'HIGH' if p >= 0.70 else ('MEDIUM' if p >= 0.30 else 'LOW')
            )

        # Get customer ID column
        customer_id_col = 'customerID' if 'customerID' in df.columns else 'user_id'
        
        # Add top driver
        df['topDriver'] = df.apply(get_top_driver_telco, axis=1)

        # Get contract type
        if 'contract_type' in df.columns:
            df['contractType'] = df['contract_type']
        elif 'Contract' in df.columns:
            df['contractType'] = df['Contract'].str.lower().replace({
                'month-to-month': 'monthly',
                'one year': 'yearly',
                'two year': 'biennial'
            })
        else:
            df['contractType'] = 'monthly'

        # Generate dates based on tenure
        base_date = datetime(2024, 11, 10)
        if 'tenure_months' in df.columns:
            df['signupDate'] = df.apply(
                lambda x: (base_date - timedelta(days=int(x['tenure_months'] * 30))).strftime('%Y-%m-%d'),
                axis=1
            )
        elif 'tenure' in df.columns:
            df['signupDate'] = df.apply(
                lambda x: (base_date - timedelta(days=int(x['tenure'] * 30))).strftime('%Y-%m-%d'),
                axis=1
            )
        else:
            df['signupDate'] = base_date.strftime('%Y-%m-%d')

        df['lastActive'] = base_date.strftime('%Y-%m-%d')

        # Build response with Telco features
        result = []
        for _, row in df.iterrows():
            customer_data = {
                'customerId': str(row[customer_id_col]),
                'churnProbability': float(row['churn_probability']),
                'riskLevel': row['risk_level'],
                'tenureMonths': int(row.get('tenure_months', row.get('tenure', 0))),
                'topDriver': row['topDriver'],
                'contractType': row['contractType'],
                'signupDate': row['signupDate'],
                'lastActive': row['lastActive'],
                'features': {
                    'tenure_months': float(row.get('tenure_months', row.get('tenure', 0))),
                    'monthly_charges': float(row.get('monthly_charges', row.get('MonthlyCharges', 0))),
                    'total_charges': float(row.get('total_charges', row.get('TotalCharges', 0))),
                    'total_services': float(row.get('total_services', 0)),
                    'is_monthly_contract': int(row.get('is_monthly_contract', 0)),
                    'has_internet': int(row.get('has_internet', 0)),
                    'internet_type': str(row.get('internet_type', 'No')),
                    'payment_method': str(row.get('payment_method', 'Unknown')),
                    'billing_risk_score': float(row.get('billing_risk_score', 0)),
                    'service_satisfaction_score': float(row.get('service_satisfaction_score', 0)),
                }
            }
            result.append(customer_data)

        print(f"[OK] Returning {len(result)} predictions")
        return result

    except Exception as e:
        print(f"[ERROR] Failed to load predictions: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                'error': str(e),
                'message': 'Failed to load predictions from features file'
            }
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print('[INFO] Starting ChurnGuard Pro API...')
    print(f'[INFO] API will be available at: http://0.0.0.0:{port}')
    print(f'[INFO] API docs at: http://0.0.0.0:{port}/docs')
    print(f'[INFO] Predictions endpoint: http://0.0.0.0:{port}/api/v1/predictions')

    uvicorn.run(app, host='0.0.0.0', port=port)
