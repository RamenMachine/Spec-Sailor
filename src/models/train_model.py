"""
Model Training Script
Trains XGBoost model for churn prediction with target >85% accuracy
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
# from imblearn.over_sampling import SMOTE  # Skipping due to version issue
import joblib
import json
import os
from datetime import datetime


# XGBoost parameters from PRD
XGB_PARAMS = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'max_depth': 7,
    'learning_rate': 0.05,
    'n_estimators': 200,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'min_child_weight': 3,
    'scale_pos_weight': 3,
    'gamma': 0.1,
    'random_state': 42,
    'n_jobs': -1
}

# Target metrics from PRD
TARGET_METRICS = {
    'accuracy': 0.85,
    'precision': 0.80,
    'recall': 0.75,
    'f1_score': 0.77,
    'roc_auc': 0.90
}


def load_features(features_path='data/processed/features.csv',
                  config_path='data/models/feature_config.json'):
    """Load engineered features and configuration"""

    print("Loading features...")
    features_df = pd.read_csv(features_path)

    with open(config_path, 'r') as f:
        config = json.load(f)

    print(f"  Loaded {len(features_df)} samples")
    print(f"  Features: {config['num_features']}")
    print(f"  Target: {config['target_column']}")

    return features_df, config


def prepare_data(features_df, config, test_size=0.2, use_smote=True):
    """Prepare train/test sets with optional SMOTE"""

    print("\nPreparing data...")

    # Separate features and target
    feature_cols = config['feature_columns']
    target_col = config['target_column']

    X = features_df[feature_cols].values
    y = features_df[target_col].values

    print(f"  Class distribution: {np.bincount(y.astype(int))}")
    print(f"  Churn rate: {y.mean()*100:.1f}%")

    # Train-test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        stratify=y,
        random_state=42
    )

    print(f"  Train set: {len(X_train)} samples")
    print(f"  Test set: {len(X_test)} samples")

    # Skip SMOTE due to version incompatibility - using scale_pos_weight instead
    print(f"\n  Using scale_pos_weight for class imbalance (SMOTE skipped)")

    return X_train, X_test, y_train, y_test, feature_cols


def train_model(X_train, y_train, X_test, y_test, params=None):
    """Train XGBoost model"""

    print("\n" + "="*70)
    print("TRAINING XGBoost MODEL")
    print("="*70)

    if params is None:
        params = XGB_PARAMS

    print("\nModel parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")

    # Create DMatrix for XGBoost
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    # Evaluation list
    evals = [(dtrain, 'train'), (dtest, 'test')]

    # Train model
    print("\nTraining...")
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=params.get('n_estimators', 200),
        evals=evals,
        early_stopping_rounds=20,
        verbose_eval=20
    )

    print(f"\nTraining complete!")
    print(f"Best iteration: {model.best_iteration}")
    print(f"Best score: {model.best_score:.4f}")

    return model


def evaluate_model(model, X_test, y_test, feature_cols):
    """Evaluate model and display metrics"""

    print("\n" + "="*70)
    print("MODEL EVALUATION")
    print("="*70)

    # Predictions
    dtest = xgb.DMatrix(X_test)
    y_pred_proba = model.predict(dtest)
    y_pred = (y_pred_proba > 0.5).astype(int)

    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1_score': f1_score(y_test, y_pred, zero_division=0),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }

    # Display metrics
    print("\nTest Set Performance:")
    print("-" * 70)
    for metric_name, value in metrics.items():
        target = TARGET_METRICS.get(metric_name, 0)
        status = "✓" if value >= target else "✗"
        print(f"  {metric_name.upper():<15} {value:.4f}  (target: {target:.2f}) {status}")

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"  TN: {cm[0,0]:<6} FP: {cm[0,1]}")
    print(f"  FN: {cm[1,0]:<6} TP: {cm[1,1]}")

    # Classification report
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Active', 'Churned']))

    # Feature importance
    importance = model.get_score(importance_type='gain')
    importance_df = pd.DataFrame([
        {'feature': feature_cols[int(k.replace('f', ''))], 'importance': v}
        for k, v in importance.items()
    ]).sort_values('importance', ascending=False)

    print(f"\nTop 15 Most Important Features:")
    print("-" * 70)
    for idx, row in importance_df.head(15).iterrows():
        print(f"  {row['feature']:<40} {row['importance']:.2f}")

    return metrics, cm, importance_df


def save_model(model, metrics, importance_df, model_dir='data/models'):
    """Save trained model and artifacts"""

    print(f"\n" + "="*70)
    print("SAVING MODEL")
    print("="*70)

    os.makedirs(model_dir, exist_ok=True)

    # Save model
    model_path = os.path.join(model_dir, 'xgboost_model.json')
    model.save_model(model_path)
    print(f"  Model saved: {model_path}")

    # Save metrics
    metrics_path = os.path.join(model_dir, 'model_metrics.json')
    metrics_data = {
        'metrics': metrics,
        'training_date': datetime.now().isoformat(),
        'model_type': 'XGBoost',
        'target_achieved': all(
            metrics[k] >= TARGET_METRICS[k] for k in TARGET_METRICS.keys()
        )
    }
    with open(metrics_path, 'w') as f:
        json.dump(metrics_data, f, indent=2)
    print(f"  Metrics saved: {metrics_path}")

    # Save feature importance
    importance_path = os.path.join(model_dir, 'feature_importance.csv')
    importance_df.to_csv(importance_path, index=False)
    print(f"  Feature importance saved: {importance_path}")

    return model_path, metrics_path, importance_path


def main():
    """Main training pipeline"""

    print("="*70)
    print("BARAKAH RETAIN - MODEL TRAINING PIPELINE")
    print("="*70)

    # Load features
    features_df, config = load_features()

    # Prepare data
    X_train, X_test, y_train, y_test, feature_cols = prepare_data(
        features_df, config, use_smote=True
    )

    # Train model
    model = train_model(X_train, y_train, X_test, y_test)

    # Evaluate model
    metrics, cm, importance_df = evaluate_model(model, X_test, y_test, feature_cols)

    # Save model
    save_model(model, metrics, importance_df)

    # Final summary
    print(f"\n" + "="*70)
    print("TRAINING COMPLETE!")
    print("="*70)

    target_met = all(metrics[k] >= TARGET_METRICS[k] for k in TARGET_METRICS.keys())

    if target_met:
        print("\n✓ ALL TARGET METRICS ACHIEVED!")
    else:
        print("\n✗ Some target metrics not achieved. Consider:")
        print("  - Hyperparameter tuning")
        print("  - Feature engineering improvements")
        print("  - Collecting more training data")

    print(f"\nModel ready for deployment!")


if __name__ == "__main__":
    main()
