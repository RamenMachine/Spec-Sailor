"""
XGBoost model training for Telco Customer Churn prediction
Implements PRD specifications with SMOTE, hyperparameters, and evaluation
"""

import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb


def train_xgboost_model(
    features_path: str = "data/processed/features_engineered.csv",
    model_dir: str = "data/models",
    random_state: int = 42
):
    """
    Train XGBoost model per PRD specifications
    
    Steps:
    1. Load engineered features
    2. Train-test split (80/20, stratified)
    3. Apply StandardScaler to numeric features
    4. Handle class imbalance with SMOTE
    5. Train XGBoost with PRD hyperparameters
    6. Evaluate on test set
    7. Save model and artifacts
    
    Args:
        features_path: Path to engineered features CSV
        model_dir: Directory to save model artifacts
        random_state: Random seed for reproducibility
    
    Returns:
        Trained model, scaler, and metrics dictionary
    """
    print("=" * 60)
    print("XGBOOST MODEL TRAINING")
    print("=" * 60)
    
    # Step 1: Load engineered features
    print(f"\n[STEP 1] Loading engineered features from: {features_path}")
    df = pd.read_csv(features_path)
    
    # Separate features and target
    if 'customerID' in df.columns:
        customer_ids = df['customerID']
        X = df.drop(columns=['customerID', 'Churn'])
    else:
        customer_ids = None
        X = df.drop(columns=['Churn'])
    
    y = df['Churn'].astype(int)
    
    print(f"  Features shape: {X.shape}")
    print(f"  Target distribution:")
    print(f"    Non-churners (0): {(y == 0).sum()} ({(y == 0).mean():.1%})")
    print(f"    Churners (1): {(y == 1).sum()} ({(y == 1).mean():.1%})")
    
    # Step 2: Train-test split
    print(f"\n[STEP 2] Train-test split (80/20, stratified)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=random_state
    )
    
    print(f"  Training set: {X_train.shape[0]} samples")
    print(f"  Test set: {X_test.shape[0]} samples")
    print(f"  Train churn rate: {y_train.mean():.1%}")
    print(f"  Test churn rate: {y_test.mean():.1%}")
    
    # Step 3: Feature scaling
    print(f"\n[STEP 3] Applying StandardScaler to numeric features...")
    
    # Identify numeric vs categorical (one-hot encoded) features
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    # Exclude one-hot encoded columns (they're already 0/1)
    one_hot_cols = [col for col in X_train.columns if any(
        prefix in col for prefix in ['household_type_', 'tenure_group_', 'internet_type_', 
                                     'contract_type_', 'payment_method_', 'churn_likelihood_segment_']
    )]
    numeric_cols = [col for col in numeric_cols if col not in one_hot_cols]
    
    print(f"  Scaling {len(numeric_cols)} numeric features")
    print(f"  Keeping {len(one_hot_cols)} one-hot encoded features as-is")
    
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])
    
    # Step 4: Handle class imbalance with SMOTE
    print(f"\n[STEP 4] Applying SMOTE to handle class imbalance...")
    print(f"  Before SMOTE:")
    print(f"    Non-churners: {(y_train == 0).sum()}")
    print(f"    Churners: {(y_train == 1).sum()}")
    print(f"    Ratio: {(y_train == 0).sum() / (y_train == 1).sum():.2f}:1")
    
    smote = SMOTE(sampling_strategy=0.7, random_state=random_state)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
    
    print(f"  After SMOTE:")
    print(f"    Non-churners: {(y_train_balanced == 0).sum()}")
    print(f"    Churners: {(y_train_balanced == 1).sum()}")
    print(f"    Ratio: {(y_train_balanced == 0).sum() / (y_train_balanced == 1).sum():.2f}:1")
    
    # Step 5: Train XGBoost with PRD parameters
    print(f"\n[STEP 5] Training XGBoost model...")
    
    # Calculate scale_pos_weight
    non_churners = (y_train == 0).sum()
    churners = (y_train == 1).sum()
    scale_pos_weight = non_churners / churners
    
    xgb_params = {
        'objective': 'binary:logistic',
        'eval_metric': ['auc', 'logloss'],
        'max_depth': 6,
        'learning_rate': 0.05,
        'n_estimators': 150,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 1,
        'scale_pos_weight': scale_pos_weight,
        'gamma': 0.1,
        'reg_alpha': 0.1,
        'reg_lambda': 1.0,
        'random_state': random_state,
        'use_label_encoder': False
    }
    
    print(f"  Hyperparameters:")
    for key, value in xgb_params.items():
        print(f"    {key}: {value}")
    
    # Create DMatrix for XGBoost
    dtrain = xgb.DMatrix(X_train_balanced, label=y_train_balanced)
    dtest = xgb.DMatrix(X_test_scaled, label=y_test)
    
    # Train with early stopping
    print(f"\n  Training with early stopping (20 rounds)...")
    evals = [(dtrain, 'train'), (dtest, 'test')]
    
    model = xgb.train(
        xgb_params,
        dtrain,
        num_boost_round=150,
        evals=evals,
        early_stopping_rounds=20,
        verbose_eval=10
    )
    
    # Step 6: Evaluate on test set
    print(f"\n[STEP 6] Evaluating on test set...")
    
    # Get predictions
    y_pred_proba = model.predict(dtest)
    y_pred = (y_pred_proba >= 0.5).astype(int)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'roc_auc': float(roc_auc),
        'confusion_matrix': {
            'true_negative': int(tn),
            'false_positive': int(fp),
            'false_negative': int(fn),
            'true_positive': int(tp)
        },
        'training_date': datetime.now().isoformat(),
        'model_type': 'XGBoost',
        'hyperparameters': xgb_params,
        'scale_pos_weight': float(scale_pos_weight)
    }
    
    print(f"\n  Test Set Metrics:")
    print(f"    Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"    Precision:   {precision:.4f} ({precision*100:.2f}%)")
    print(f"    Recall:      {recall:.4f} ({recall*100:.2f}%)")
    print(f"    F1-Score:    {f1:.4f}")
    print(f"    ROC-AUC:     {roc_auc:.4f}")
    print(f"\n  Confusion Matrix:")
    print(f"    True Negatives:  {tn}")
    print(f"    False Positives: {fp}")
    print(f"    False Negatives: {fn}")
    print(f"    True Positives:  {tp}")
    
    # Check if targets are met
    print(f"\n  Target Check:")
    targets_met = True
    if accuracy >= 0.80:
        print(f"    ✓ Accuracy >= 80%: {accuracy*100:.2f}%")
    else:
        print(f"    ✗ Accuracy < 80%: {accuracy*100:.2f}%")
        targets_met = False
    
    if roc_auc >= 0.85:
        print(f"    ✓ ROC-AUC >= 0.85: {roc_auc:.4f}")
    else:
        print(f"    ✗ ROC-AUC < 0.85: {roc_auc:.4f}")
        targets_met = False
    
    # Step 7: Save artifacts
    print(f"\n[STEP 7] Saving model artifacts...")
    
    model_dir_path = Path(model_dir)
    model_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Save model
    model_path = model_dir_path / "xgboost_telco_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"  Saved model to: {model_path}")
    
    # Save scaler
    scaler_path = model_dir_path / "feature_scaler.pkl"
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"  Saved scaler to: {scaler_path}")
    
    # Save metrics
    metrics_path = model_dir_path / "model_metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"  Saved metrics to: {metrics_path}")
    
    # Save feature importance
    feature_importance = model.get_score(importance_type='gain')
    importance_df = pd.DataFrame([
        {'feature': k, 'importance': v}
        for k, v in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    ])
    
    importance_path = model_dir_path / "feature_importance.csv"
    importance_df.to_csv(importance_path, index=False)
    print(f"  Saved feature importance to: {importance_path}")
    
    print(f"\n  Top 15 Important Features:")
    for idx, row in importance_df.head(15).iterrows():
        print(f"    {idx+1:2d}. {row['feature']:30s} {row['importance']:10.2f}")
    
    print("\n" + "=" * 60)
    print("MODEL TRAINING COMPLETE")
    print("=" * 60)
    
    return model, scaler, metrics


if __name__ == "__main__":
    # Test training
    model, scaler, metrics = train_xgboost_model()
    print(f"\n[SUCCESS] Model training complete!")
    print(f"  Accuracy: {metrics['accuracy']:.2%}")
    print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")

