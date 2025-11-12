"""
SHAP Explainability Module
Generates SHAP explanations for model predictions
"""

import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import json
import os
from typing import Dict, List


def load_model_and_data(
    model_path='data/models/xgboost_model.json',
    features_path='data/processed/features.csv',
    config_path='data/models/feature_config.json'
):
    """Load trained model, features, and configuration"""

    print("Loading model and data...")

    # Load model
    model = xgb.Booster()
    model.load_model(model_path)

    # Load features
    features_df = pd.read_csv(features_path)

    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)

    feature_cols = config['feature_columns']
    X = features_df[feature_cols].values

    print(f"  Model loaded: {model_path}")
    print(f"  Features: {len(feature_cols)}")
    print(f"  Samples: {len(features_df)}")

    return model, features_df, feature_cols, X


def generate_shap_values(model, X, feature_cols):
    """Generate SHAP values for all predictions"""

    print("\nGenerating SHAP values...")

    # Create explainer
    explainer = shap.TreeExplainer(model)

    # Calculate SHAP values
    shap_values = explainer.shap_values(X)

    print(f"  SHAP values shape: {shap_values.shape}")

    return explainer, shap_values


def explain_prediction(
    user_id: str,
    features_df: pd.DataFrame,
    model: xgb.Booster,
    explainer: shap.Explainer,
    feature_cols: List[str],
    top_n: int = 10
) -> Dict:
    """
    Generate detailed explanation for a single user prediction

    Args:
        user_id: User identifier
        features_df: DataFrame with all features
        model: Trained XGBoost model
        explainer: SHAP explainer
        feature_cols: List of feature column names
        top_n: Number of top features to return

    Returns:
        Dictionary with prediction and explanation
    """

    # Get user data
    user_data = features_df[features_df['user_id'] == user_id]

    if len(user_data) == 0:
        return {'error': f'User {user_id} not found'}

    user_idx = user_data.index[0]
    X_user = user_data[feature_cols].values

    # Prediction
    duser = xgb.DMatrix(X_user)
    churn_prob = float(model.predict(duser)[0])
    risk_level = 'HIGH' if churn_prob > 0.7 else ('MEDIUM' if churn_prob > 0.3 else 'LOW')

    # SHAP values
    shap_vals = explainer.shap_values(X_user)[0]
    base_value = explainer.expected_value

    # Get feature contributions
    contributions = []
    for i, (feat_name, shap_val, feat_val) in enumerate(zip(feature_cols, shap_vals, X_user[0])):
        contributions.append({
            'feature': feat_name,
            'value': float(feat_val),
            'shap_value': float(shap_val),
            'impact': 'increases' if shap_val > 0 else 'decreases'
        })

    # Sort by absolute SHAP value
    contributions.sort(key=lambda x: abs(x['shap_value']), reverse=True)

    # Top positive and negative contributors
    top_positive = [c for c in contributions if c['shap_value'] > 0][:top_n]
    top_negative = [c for c in contributions if c['shap_value'] < 0][:top_n]

    # Generate human-readable explanations
    explanations = []

    for contrib in top_positive[:5]:
        explanations.append(generate_feature_explanation(contrib, increase_risk=True))

    for contrib in top_negative[:5]:
        explanations.append(generate_feature_explanation(contrib, increase_risk=False))

    return {
        'user_id': user_id,
        'churn_probability': churn_prob,
        'risk_level': risk_level,
        'base_value': float(base_value),
        'prediction': churn_prob,
        'top_positive_contributors': top_positive,
        'top_negative_contributors': top_negative,
        'explanations': explanations,
        'all_contributions': contributions[:20]  # Top 20 overall
    }


def generate_feature_explanation(contribution: Dict, increase_risk: bool) -> str:
    """Generate human-readable explanation for a feature contribution"""

    feature = contribution['feature']
    value = contribution['value']
    shap_val = contribution['shap_value']
    impact_pct = abs(shap_val) * 100

    # Map feature names to readable explanations
    explanations_map = {
        'days_since_last_session': f"User hasn't opened app in {int(value)} days",
        'session_frequency_7d': f"User had {int(value)} sessions in last 7 days",
        'session_frequency_30d': f"User had {int(value)} sessions in last 30 days",
        'avg_session_duration': f"Average session duration: {value:.1f} minutes",
        'total_sessions': f"Total sessions: {int(value)}",
        'streak_current': f"Current streak: {int(value)} days",
        'streak_longest': f"Longest streak: {int(value)} days",
        'days_since_signup': f"User signed up {int(value)} days ago",
        'sessions_per_week': f"Sessions per week: {value:.1f}",
        'weekend_activity_ratio': f"Weekend activity: {value*100:.0f}%",
        'ramadan_engagement_ratio': f"User was {value:.1f}x more active during Ramadan",
        'is_ramadan_convert': "User signed up during Ramadan" if value == 1 else "User signed up outside Ramadan",
        'days_since_ramadan': f"{int(value)} days since Ramadan ended",
        'last_10_nights_sessions': f"{int(value)} sessions during last 10 nights of Ramadan",
        'jummah_participation_rate': f"Jummah participation: {value*100:.0f}%",
        'prayer_time_interaction_rate': f"Prayer time activity: {value*100:.0f}%",
        'eid_participation': "Participated during Eid" if value == 1 else "No Eid participation",
        'muharram_participation': "Participated during Muharram" if value == 1 else "No Muharram participation",
        'quran_reading_pct': f"Quran reading: {value*100:.0f}% of activity",
        'hadith_engagement_pct': f"Hadith engagement: {value*100:.0f}% of activity",
        'lecture_watch_minutes': f"Watched {value:.0f} minutes of lectures",
        'fiqh_content_views': f"Viewed {int(value)} Fiqh content items",
        'seerah_content_views': f"Viewed {int(value)} Seerah content items",
        'tafsir_engagement': f"Engaged with {int(value)} Tafsir content",
        'topic_diversity_score': f"Explored {int(value)} different content types",
        'content_completion_rate': f"Content completion rate: {value*100:.0f}%",
        'bookmark_count': f"Saved {int(value)} bookmarks",
        'friends_count': f"Has {int(value)} friends",
        'shares_sent': f"Shared content {int(value)} times",
        'comments_made': f"Made {int(value)} comments",
        'days_since_last_social': f"Last social interaction: {int(value)} days ago"
    }

    # Get readable explanation
    readable = explanations_map.get(feature, f"{feature}: {value:.2f}")

    # Add impact direction
    direction = "increases" if increase_risk else "decreases"
    impact_emoji = "🔴" if increase_risk else "🟢"

    return f"{impact_emoji} {readable} ({direction} churn risk by {impact_pct:.1f}%)"


def save_shap_explanations(
    features_df: pd.DataFrame,
    shap_values: np.ndarray,
    feature_cols: List[str],
    output_dir: str = 'data/models'
):
    """Save SHAP values for all users"""

    print("\nSaving SHAP explanations...")

    os.makedirs(output_dir, exist_ok=True)

    # Create DataFrame with SHAP values
    shap_df = pd.DataFrame(
        shap_values,
        columns=[f'shap_{col}' for col in feature_cols]
    )

    shap_df['user_id'] = features_df['user_id'].values

    # Save
    output_path = os.path.join(output_dir, 'shap_values.csv')
    shap_df.to_csv(output_path, index=False)

    print(f"  SHAP values saved: {output_path}")

    return output_path


def main():
    """Generate SHAP explanations for all users"""

    print("="*70)
    print("BARAKAH RETAIN - SHAP EXPLAINABILITY")
    print("="*70)

    # Load model and data
    model, features_df, feature_cols, X = load_model_and_data()

    # Generate SHAP values
    explainer, shap_values = generate_shap_values(model, X, feature_cols)

    # Save SHAP values
    save_shap_explanations(features_df, shap_values, feature_cols)

    # Example: Explain predictions for first 5 high-risk users
    print("\n" + "="*70)
    print("EXAMPLE EXPLANATIONS - Top 5 High-Risk Users")
    print("="*70)

    # Get predictions
    dmatrix = xgb.DMatrix(X)
    predictions = model.predict(dmatrix)
    features_df['churn_prob'] = predictions

    # Get top 5 high-risk users
    high_risk = features_df.nlargest(5, 'churn_prob')

    for idx, row in high_risk.iterrows():
        user_id = row['user_id']
        explanation = explain_prediction(user_id, features_df, model, explainer, feature_cols)

        print(f"\n{'─'*70}")
        print(f"User: {user_id}")
        print(f"Churn Probability: {explanation['churn_probability']:.1%}")
        print(f"Risk Level: {explanation['risk_level']}")
        print(f"\nTop Factors Increasing Churn Risk:")
        for exp in explanation['explanations'][:3]:
            if '🔴' in exp:
                print(f"  {exp}")
        print(f"\nTop Factors Decreasing Churn Risk:")
        for exp in explanation['explanations'][:3]:
            if '🟢' in exp:
                print(f"  {exp}")

    print(f"\n{'='*70}")
    print("SHAP explanations generated successfully!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
