"""
Model evaluation and visualization
Generates comprehensive metrics and visualizations
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, average_precision_score,
    confusion_matrix, matthews_corrcoef
)
import xgboost as xgb


def evaluate_model(
    model_path: str = "data/models/xgboost_telco_model.pkl",
    features_path: str = "data/processed/features_engineered.csv",
    scaler_path: str = "data/models/feature_scaler.pkl",
    output_dir: str = "outputs/evaluation"
):
    """
    Evaluate trained model and generate visualizations
    
    Args:
        model_path: Path to trained XGBoost model
        features_path: Path to engineered features
        scaler_path: Path to feature scaler
        output_dir: Directory to save visualizations
    """
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    
    # Load model and scaler
    print(f"\n[INFO] Loading model from: {model_path}")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"[INFO] Loading scaler from: {scaler_path}")
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    # Load test data
    print(f"[INFO] Loading features from: {features_path}")
    df = pd.read_csv(features_path)
    
    # Separate features and target
    if 'customerID' in df.columns:
        X = df.drop(columns=['customerID', 'Churn'])
    else:
        X = df.drop(columns=['Churn'])
    
    y = df['Churn'].astype(int)
    
    # Scale features
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    one_hot_cols = [col for col in X.columns if any(
        prefix in col for prefix in ['household_type_', 'tenure_group_', 'internet_type_', 
                                     'contract_type_', 'payment_method_', 'churn_likelihood_segment_']
    )]
    numeric_cols = [col for col in numeric_cols if col not in one_hot_cols]
    
    X_scaled = X.copy()
    X_scaled[numeric_cols] = scaler.transform(X[numeric_cols])
    
    # Get predictions
    dtest = xgb.DMatrix(X_scaled, label=y)
    y_pred_proba = model.predict(dtest)
    y_pred = (y_pred_proba >= 0.5).astype(int)
    
    # Calculate metrics
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    roc_auc = roc_auc_score(y, y_pred_proba)
    pr_auc = average_precision_score(y, y_pred_proba)
    mcc = matthews_corrcoef(y, y_pred)
    
    print(f"\n[INFO] Comprehensive Metrics:")
    print(f"  Accuracy:              {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  Precision:             {precision:.4f} ({precision*100:.2f}%)")
    print(f"  Recall:                {recall:.4f} ({recall*100:.2f}%)")
    print(f"  F1-Score:              {f1:.4f}")
    print(f"  ROC-AUC:               {roc_auc:.4f}")
    print(f"  PR-AUC (AP):           {pr_auc:.4f}")
    print(f"  Matthews Correlation:  {mcc:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(y, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print(f"\n[INFO] Confusion Matrix:")
    print(f"  True Negatives:  {tn:4d}")
    print(f"  False Positives: {fp:4d}")
    print(f"  False Negatives: {fn:4d}")
    print(f"  True Positives:  {tp:4d}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 8)
    
    # 1. Confusion Matrix Heatmap
    print(f"\n[INFO] Generating confusion matrix heatmap...")
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=['No Churn', 'Churn'],
        yticklabels=['No Churn', 'Churn'],
        cbar_kws={'label': 'Count'}
    )
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    
    # Add percentages
    cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    for i in range(2):
        for j in range(2):
            plt.text(j+0.5, i+0.7, f'({cm_percent[i,j]:.1f}%)',
                    ha='center', va='center', fontsize=10, color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved to: {output_path / 'confusion_matrix.png'}")
    
    # 2. ROC Curve
    print(f"[INFO] Generating ROC curve...")
    fpr, tpr, thresholds = roc_curve(y, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curve', fontsize=16, fontweight='bold')
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / 'roc_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved to: {output_path / 'roc_curve.png'}")
    
    # 3. Precision-Recall Curve
    print(f"[INFO] Generating Precision-Recall curve...")
    precision_vals, recall_vals, pr_thresholds = precision_recall_curve(y, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall_vals, precision_vals, linewidth=2, label=f'PR Curve (AP = {pr_auc:.4f})')
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title('Precision-Recall Curve', fontsize=16, fontweight='bold')
    plt.legend(loc='lower left', fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / 'pr_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved to: {output_path / 'pr_curve.png'}")
    
    # 4. Feature Importance
    print(f"[INFO] Generating feature importance plot...")
    feature_importance = model.get_score(importance_type='gain')
    importance_df = pd.DataFrame([
        {'feature': k, 'importance': v}
        for k, v in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    ]).head(20)
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(importance_df)), importance_df['importance'], color='steelblue')
    plt.yticks(range(len(importance_df)), importance_df['feature'])
    plt.xlabel('Importance (Gain)', fontsize=12)
    plt.title('Top 20 Feature Importance', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / 'feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved to: {output_path / 'feature_importance.png'}")
    
    # 5. Probability Distribution
    print(f"[INFO] Generating probability distribution...")
    plt.figure(figsize=(10, 6))
    plt.hist(y_pred_proba[y == 0], bins=50, alpha=0.7, label='No Churn', color='green', density=True)
    plt.hist(y_pred_proba[y == 1], bins=50, alpha=0.7, label='Churn', color='red', density=True)
    plt.xlabel('Predicted Probability', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.title('Predicted Probability Distribution', fontsize=16, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / 'probability_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved to: {output_path / 'probability_distribution.png'}")
    
    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)
    print(f"\n[SUCCESS] All visualizations saved to: {output_path}")


if __name__ == "__main__":
    evaluate_model()

