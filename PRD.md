# Product Requirements Document - FINAL

## Islamic App User Retention Prediction System

### "Barakah Retain" - Blessing Your User Retention

**Version:** 1.0 FINAL

**Date:** November 11, 2024

**Implementation:** Bolt/Lovable → Claude Code

**Timeline:** 4 weeks to portfolio-ready

**Owner:** Ameen

---

## 🎯 Executive Summary

### The Problem

Islamic mobile apps see 60-70% of users leave within 30 days after Ramadan. Organizations waste resources on blanket campaigns with <10% success rates because they can't predict which users need help.

### The Solution

**Barakah Retain** uses XGBoost machine learning to predict which users will churn 7-30 days in advance with >85% accuracy, providing Islamic organizations with actionable insights and personalized intervention recommendations.

### Success Metrics

* **Model Performance:** >85% accuracy, >0.90 AUC-ROC
* **Business Impact:** +30% retention rate improvement
* **Early Warning:** Flag 70% of churners 7+ days early
* **Cost Efficiency:** 40% reduction in cost per retained user

---

## 🏗️ Technical Architecture

### System Overview

```
Data → Feature Engineering → XGBoost Model → API/Dashboard → Insights
```

### Tech Stack

* **Backend:** Python 3.9+, FastAPI
* **ML:** XGBoost, scikit-learn, SHAP, pandas, numpy
* **Frontend:** Streamlit (for dashboard)
* **Database:** PostgreSQL (predictions), CSV (for demo)
* **Deployment:** Docker, Streamlit Cloud (free tier)
* **Tools:** MLflow (experiment tracking), Plotly (visualizations)

### Complete File Structure

```
barakah-retain/
├── data/
│   ├── raw/
│   │   ├── sample_users.csv
│   │   └── sample_events.csv
│   ├── processed/
│   │   ├── train.csv
│   │   ├── test.csv
│   │   └── features.csv
│   └── models/
│       ├── xgboost_model.pkl
│       ├── scaler.pkl
│       └── feature_config.json
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_generator.py (simulate data)
│   │   ├── data_loader.py
│   │   ├── data_cleaner.py
│   │   └── data_validator.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── engagement_features.py
│   │   ├── islamic_calendar_features.py
│   │   ├── content_features.py
│   │   └── feature_engineering.py (main pipeline)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train_model.py
│   │   ├── predict.py
│   │   ├── evaluate.py
│   │   └── explain.py (SHAP)
│   └── utils/
│       ├── __init__.py
│       ├── metrics.py
│       └── helpers.py
├── api/
│   ├── __init__.py
│   ├── main.py (FastAPI app)
│   ├── models.py (Pydantic schemas)
│   ├── routes.py
│   └── config.py
├── dashboard/
│   ├── app.py (main Streamlit app)
│   ├── pages/
│   │   ├── 1_🏠_Home.py
│   │   ├── 2_👥_User_Predictions.py
│   │   ├── 3_📊_Model_Performance.py
│   │   └── 4_💡_Insights.py
│   └── components/
│       ├── metrics_cards.py
│       ├── user_table.py
│       ├── charts.py
│       └── explanations.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_evaluation.ipynb
├── tests/
│   ├── test_features.py
│   ├── test_model.py
│   └── test_api.py
├── .gitignore
├── requirements.txt
├── Dockerfile
├── README.md
└── config.yaml
```

---

## 📊 Data Schema & Features

### Input Data Schema

#### Table 1: user_events.csv

```
user_id,event_timestamp,event_type,session_duration_seconds,content_category
user-1234,2024-06-15 08:30:00,app_open,180,NULL
user-1234,2024-06-15 08:32:00,quran_read,600,Quran
user-1234,2024-06-15 20:15:00,prayer_log,30,Prayer
user-5678,2024-06-16 14:20:00,lecture_view,1800,Seerah
```

#### Table 2: user_profiles.csv

```
user_id,signup_date,subscription_type,location,is_churned,last_active
user-1234,2024-03-15,premium,Chicago IL,False,2024-11-10
user-5678,2024-04-01,free,Houston TX,True,2024-10-15
```

### Complete Feature Set (32 Features)

#### 1. Engagement Features (10)

```python
{
    'days_since_last_session': int,      # Range: 0-180
    'session_frequency_7d': int,         # Range: 0-50
    'session_frequency_30d': int,        # Range: 0-200
    'avg_session_duration': float,       # Minutes, Range: 0-60
    'total_sessions': int,               # Range: 1-5000
    'streak_current': int,               # Days, Range: 0-365
    'streak_longest': int,               # Days, Range: 0-365
    'days_since_signup': int,            # Range: 30-365
    'sessions_per_week': float,          # Range: 0-50
    'weekend_activity_ratio': float      # Range: 0-1
}
```

#### 2. Islamic Calendar Features (8)

```python
{
    'ramadan_engagement_ratio': float,    # Range: 0-10
    'is_ramadan_convert': bool,           # 0 or 1
    'days_since_ramadan': int,            # Range: 0-330
    'last_10_nights_sessions': int,       # Range: 0-30
    'jummah_participation_rate': float,   # Range: 0-1
    'prayer_time_interaction_rate': float, # Range: 0-1
    'eid_participation': bool,            # 0 or 1
    'muharram_participation': bool        # 0 or 1
}
```

#### 3. Content Features (10)

```python
{
    'quran_reading_pct': float,          # Range: 0-1
    'hadith_engagement_pct': float,      # Range: 0-1
    'lecture_watch_minutes': float,      # Range: 0-5000
    'fiqh_content_views': int,           # Range: 0-500
    'seerah_content_views': int,         # Range: 0-500
    'tafsir_engagement': int,            # Range: 0-200
    'topic_diversity_score': float,      # Range: 0-5
    'favorite_content_type': str,        # Categorical
    'content_completion_rate': float,    # Range: 0-1
    'bookmark_count': int                # Range: 0-100
}
```

#### 4. Social Features (4)

```python
{
    'friends_count': int,                # Range: 0-500
    'shares_sent': int,                  # Range: 0-200
    'comments_made': int,                # Range: 0-300
    'days_since_last_social': int        # Range: 0-180
}
```

### Target Variable

```python
target = 'is_churned'  # Boolean: True if inactive 30+ days
```

---

## 🤖 XGBoost Model Configuration

### Training Parameters

```python
xgb_params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'max_depth': 7,
    'learning_rate': 0.05,
    'n_estimators': 200,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'min_child_weight': 3,
    'scale_pos_weight': 3,  # Handle class imbalance
    'gamma': 0.1,
    'random_state': 42
}
```

### Hyperparameter Tuning Grid

```python
param_grid = {
    'max_depth': [5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'subsample': [0.7, 0.8, 0.9],
    'colsample_bytree': [0.7, 0.8, 0.9],
    'scale_pos_weight': [1, 3, 5]
}
```

### Data Preparation

```python
# Train-test split
train_size = 0.8
stratify = True  # Ensure balanced target in both sets

# Handle imbalance with SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy=0.5, random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
```

### Target Metrics

* **Accuracy:** >85%
* **Precision:** >80%
* **Recall:** >75%
* **ROC-AUC:** >0.90

---

## 📝 Bolt/Lovable Implementation Prompts

### PHASE 1: DATA GENERATION (Day 1-2)

#### Prompt 1.1: Generate User Events Data

```
Create a Python function generate_user_events() that creates synthetic Islamic app usage data:

Requirements:
- 10,000 unique users
- 6 months of activity history (June 1 - Nov 10, 2024)
- Event types: 'app_open', 'quran_read', 'prayer_log', 'lecture_view', 'hadith_read', 'fiqh_content', 'seerah_read'
- 70% active users (activity in last 30 days)
- 30% churned users (no activity for 30+ days)

Realistic patterns to include:
1. Ramadan spike (March 11 - April 9, 2024):
   - 300% increase in activity during Ramadan
   - More quran_read and prayer_log events
   
2. Post-Ramadan drop-off:
   - 60% of Ramadan-only users stop after Eid (April 10)
   - Gradual decline over 30 days

3. Weekly patterns:
   - Friday (Jummah) has 40% more activity
   - Weekend activity higher than weekdays

4. Daily patterns:
   - Prayer times: 5 peaks per day (Fajr, Dhuhr, Asr, Maghrib, Isha)
   - Evening activity (7-10 PM) highest

5. User engagement types:
   - High engagers: 5-10 sessions/day
   - Medium engagers: 2-5 sessions/day
   - Low engagers: 0-2 sessions/day
   - Streakers: Consecutive daily activity

Output:
- Save as 'data/raw/sample_events.csv' with columns:
  user_id, event_timestamp, event_type, session_duration_seconds, content_category
- ~500K total events
```

#### Prompt 1.2: Generate User Profiles

```
Create Python function generate_user_profiles() that creates user metadata:

Requirements:
- 10,000 users (matching events data)
- signup_date: Random between Dec 2023 - Nov 2024
  - 40% signed up during Ramadan (March 11 - April 9)
  - 60% throughout other months
- subscription_type: 70% free, 20% basic, 10% premium
- location: US cities with large Muslim populations
  (Chicago, Houston, Dallas, New York, Los Angeles, Detroit, Atlanta)
- is_churned: True if no activity in last 30 days, else False
- last_active: Date of last event

Output:
- Save as 'data/raw/sample_profiles.csv' with columns:
  user_id, signup_date, subscription_type, location, is_churned, last_active
```

---

### PHASE 2: FEATURE ENGINEERING (Day 3-5)

#### Prompt 2.1: Engagement Features

```
Create Python function calculate_engagement_features(events_df, profiles_df, user_id, as_of_date):

Calculate for a single user as of a specific date:
1. days_since_last_session: Days between as_of_date and last app_open event
2. session_frequency_7d: Count of app_open in last 7 days
3. session_frequency_30d: Count of app_open in last 30 days
4. avg_session_duration: Mean session_duration_seconds in minutes
5. total_sessions: Total count of app_open events
6. streak_current: Consecutive days with activity ending on as_of_date
7. streak_longest: Maximum consecutive days with activity in history
8. days_since_signup: as_of_date - signup_date
9. sessions_per_week: total_sessions / weeks_since_signup
10. weekend_activity_ratio: weekend_sessions / total_sessions

Handle edge cases:
- New users (<7 days history): Use available data
- No events: Return 0 or NaN appropriately
- Division by zero: Return 0

Return: Dictionary of 10 features
```

#### Prompt 2.2: Islamic Calendar Features

```
Create Python function calculate_islamic_features(events_df, profiles_df, user_id, as_of_date):

Use hijri-converter library for Islamic dates.

Calculate:
1. ramadan_engagement_ratio:
   - sessions_during_ramadan / sessions_during_non_ramadan
   - Ramadan 2024: March 11 - April 9
   - If denominator is 0, return 0
   
2. is_ramadan_convert: True if signup_date in Ramadan period

3. days_since_ramadan: Days between as_of_date and April 9, 2024 (end of Ramadan)

4. last_10_nights_sessions: Count of sessions in March 30 - April 9 (last 10 nights)

5. jummah_participation_rate:
   - Count Fridays with activity / Total Fridays since signup
   
6. prayer_time_interaction_rate:
   - Count events within ±1 hour of prayer times / (5 prayers * days since signup)
   - Prayer times (approximate): 5:30 AM, 12:30 PM, 3:30 PM, 6:30 PM, 8:00 PM

7. eid_participation: True if activity on Eid days (April 10-12, 2024)

8. muharram_participation: True if activity during Muharram (July 7 - Aug 6, 2024)

Return: Dictionary of 8 features
```

#### Prompt 2.3: Content Features

```
Create Python function calculate_content_features(events_df, user_id):

Calculate:
1. quran_reading_pct: % of events where event_type == 'quran_read'
2. hadith_engagement_pct: % of events where event_type == 'hadith_read'
3. lecture_watch_minutes: Sum of session_duration for event_type == 'lecture_view'
4. fiqh_content_views: Count of event_type == 'fiqh_content'
5. seerah_content_views: Count of event_type == 'seerah_read'
6. tafsir_engagement: Count of content_category == 'Tafsir'
7. topic_diversity_score: Number of unique event_types used
8. favorite_content_type: Mode of event_type (most common)
9. content_completion_rate: % of sessions > 5 minutes (proxy for completion)
10. bookmark_count: Random 0-50 for demo (would be real data in production)

Return: Dictionary of 10 features
```

#### Prompt 2.4: Social Features

```
Create Python function calculate_social_features(events_df, user_id):

For demo purposes, simulate social features with realistic distributions:
1. friends_count: Random 0-100, weighted toward lower values (exponential distribution)
2. shares_sent: Random 0-50, correlated with engagement level
3. comments_made: Random 0-30, correlated with engagement level
4. days_since_last_social: Days since last social action (simulated)

In production, these would come from real social interaction data.

Return: Dictionary of 4 features
```

#### Prompt 2.5: Master Feature Engineering Pipeline

```
Create Python function engineer_all_features(events_df, profiles_df, as_of_date='2024-11-10'):

For each user in profiles_df:
1. Call calculate_engagement_features()
2. Call calculate_islamic_features()
3. Call calculate_content_features()
4. Call calculate_social_features()
5. Combine all features into one row
6. Add user_id and is_churned (target variable)
7. Handle categorical variables:
   - One-hot encode: favorite_content_type, subscription_type, location
   - Convert boolean to int: is_ramadan_convert, eid_participation, muharram_participation

Output:
- DataFrame with shape (10000, 40+) after one-hot encoding
- Save as 'data/processed/features.csv'
- Save feature names as 'data/models/feature_config.json'

Return: features_df
```

---

### PHASE 3: MODEL TRAINING (Day 6-7)

#### Prompt 3.1: Train XGBoost Model

```
Create Python script train_model.py that:

1. Load features from 'data/processed/features.csv'
2. Separate features (X) and target (y = is_churned)
3. Train-test split: 80-20, stratified by target
4. Handle class imbalance with SMOTE on training set only
5. Train XGBoost with these params:
   {
       'objective': 'binary:logistic',
       'eval_metric': 'auc',
       'max_depth': 7,
       'learning_rate': 0.05,
       'n_estimators': 200,
       'subsample': 0.8,
       'colsample_bytree': 0.8,
       'min_child_weight': 3,
       'scale_pos_weight': 3,
       'random_state': 42
   }
6. Evaluate on test set: accuracy, precision, recall, f1, ROC-AUC
7. Save model as 'data/models/xgboost_model.pkl'
8. Save metrics as JSON

Print:
- Training complete message
- Test set metrics
- Feature importance (top 10)

Must achieve: Accuracy >85%, ROC-AUC >0.90
```

#### Prompt 3.2: Model Evaluation Script

```
Create Python script evaluate_model.py that:

1. Load trained model
2. Load test set
3. Generate predictions and probabilities
4. Calculate metrics:
   - Accuracy, Precision, Recall, F1
   - ROC-AUC, PR-AUC
   - Confusion matrix
5. Create visualizations:
   - Confusion matrix heatmap
   - ROC curve
   - Precision-Recall curve
   - Feature importance bar chart (top 15)
6. Save plots to 'outputs/model_evaluation/'
7. Generate classification report

Output: Print metrics and save visualizations
```

#### Prompt 3.3: SHAP Explainability

```
Create Python function generate_shap_explanations(model, X_test, user_idx):

1. Initialize SHAP TreeExplainer with model
2. Calculate SHAP values for user at user_idx
3. Get base value (average prediction)
4. Get SHAP contributions for each feature
5. Identify top 5 positive contributors (increase churn risk)
6. Identify top 5 negative contributors (decrease churn risk)
7. Create waterfall plot showing prediction logic
8. Translate feature names to readable text:
   - 'days_since_last_session' → "User hasn't opened app in X days"
   - 'ramadan_engagement_ratio' → "User was Xx more active during Ramadan"
   
Return: Dictionary with SHAP values and explanations
Save waterfall plot to 'outputs/explanations/user_{user_id}_shap.png'
```

---

### PHASE 4: API DEVELOPMENT (Day 8-10)

#### Prompt 4.1: FastAPI Main Application

```
Create FastAPI application in api/main.py:

Endpoints:
1. GET /health - Health check
2. POST /api/v1/predict/batch - Batch predictions
3. GET /api/v1/predict/user/{user_id} - Single user prediction
4. GET /api/v1/explain/{user_id} - SHAP explanation
5. GET /api/v1/model/feature-importance - Feature importance
6. GET /api/v1/model/performance - Model metrics

Include:
- API key authentication
- Request validation with Pydantic models
- Error handling
- CORS middleware
- Response models for each endpoint
- Swagger documentation

Load model on startup (not per request)
Cache SHAP explanations for performance
```

#### Prompt 4.2: Pydantic Schemas

```
Create Pydantic models in api/models.py:

1. UserFeatures: All 32 feature fields with types and validation
2. PredictionRequest: List of users with features
3. PredictionResponse: user_id, probability, risk_level, top_factors
4. SHAPExplanation: base_value, contributions, waterfall_data
5. FeatureImportance: feature name, importance score, rank
6. ModelPerformance: metrics dictionary, confusion matrix

Include field descriptions and examples for Swagger docs
```

---

(Continue in Part 2 due to length...)

# PRD Part 2: Dashboard & Deployment

## PHASE 5: STREAMLIT DASHBOARD (Day 11-14)

### Prompt 5.1: Main Dashboard App

```
Create Streamlit multi-page app in dashboard/app.py:

Setup:
- Page config: wide layout, page title "Barakah Retain", crescent moon icon
- Sidebar navigation to pages
- Load model and predictions on app start
- Cache data loading for performance
- Custom CSS for Islamic app branding (green accents, clean design)

Sidebar content:
- App logo and title
- Last updated timestamp
- Navigation menu
- Data refresh button
- About section

Main page (Home):
- Welcome message
- Key metrics cards (4 columns)
- Churn risk trend chart
- Top 10 at-risk users table
- Quick action buttons
```

### Prompt 5.2: Page 1 - Home Dashboard

```
Create dashboard/pages/1_🏠_Home.py:

Layout:
1. Header with app title and last update time

2. Metrics Row (4 columns):
   - Total Users (count)
   - High Risk 🔴 (count + percentage)
   - Medium Risk 🟡 (count + percentage)
   - Low Risk 🟢 (count + percentage)
   
   Use st.metric() with delta showing trend vs yesterday

3. Churn Risk Trend Chart:
   - Line chart showing daily high-risk user count over last 30 days
   - Use plotly for interactivity
   - X-axis: Date, Y-axis: Number of high-risk users
   - Add Ramadan period annotation

4. Top 10 At-Risk Users Table:
   - Columns: User ID, Risk Score, Risk Level, Days Inactive, Top Driver
   - Sortable and clickable
   - Color-code by risk level
   - "View Details" button for each user

5. Quick Actions Row (3 buttons):
   - Export CSV (download all predictions)
   - Refresh Data (reload predictions)
   - View Insights (navigate to insights page)

Use components from dashboard/components/
```

### Prompt 5.3: Page 2 - User Predictions List

```
Create dashboard/pages/2_👥_User_Predictions.py:

Filters section:
- Risk Level: multiselect [HIGH, MEDIUM, LOW]
- Subscription Type: select [All, Free, Basic, Premium]
- Signup Cohort: select [All, Ramadan 2024, Q1 2024, Q2 2024, etc.]
- Days Inactive: slider (0-180)
- Search User ID: text input

User Table:
- Display filtered results
- Columns: checkbox, user_id, risk_level, churn_probability, days_inactive, 
  last_active, subscription_type, recommended_intervention
- Pagination: 50 rows per page
- Sortable by any column
- Click row to expand and show SHAP explanation inline
- Bulk selection checkboxes

Bulk Actions (for selected users):
- Export selected to CSV
- Generate intervention report
- Create user segment

User Detail Modal (when row clicked):
- Risk score gauge chart
- SHAP waterfall plot
- Engagement history line chart
- Recommended intervention card
- Close button
```

### Prompt 5.4: Page 3 - Model Performance

```
Create dashboard/pages/3_📊_Model_Performance.py:

Section 1: Performance Metrics Cards
- 4 columns: Accuracy, Precision, Recall, F1 Score
- Show value + green checkmark if target met
- Compare to baseline model (simple rule-based)

Section 2: Confusion Matrix
- Heatmap visualization
- Annotations with counts
- Explanation text below:
  "True Positives: 1,400 users correctly predicted as churners"
  "False Positives: 200 users incorrectly flagged"
  etc.

Section 3: ROC Curve
- Plot with AUC score
- Diagonal reference line
- Interactive plotly chart

Section 4: Precision-Recall Curve
- Plot with AP score
- Explain trade-off in text

Section 5: Feature Importance
- Horizontal bar chart of top 15 features
- SHAP values (mean absolute)
- Sort by importance descending
- Explain what each feature means

Section 6: Model Information
- Model version
- Training date
- Test set size
- Retraining schedule
- Download model card PDF button
```

### Prompt 5.5: Page 4 - Insights & Analytics

```
Create dashboard/pages/4_💡_Insights.py:

Section 1: Key Findings (Expandable Cards)
Card 1: Post-Ramadan Drop-off Pattern
- Stat: "68% of Ramadan converts churn within 30 days"
- Chart: Retention curve for Ramadan cohort
- Recommendation: Launch retention campaign at Day 7

Card 2: Engagement Streak Impact
- Stat: "Streak breaks increase churn probability by 45%"
- Chart: Churn rate by streak length
- Recommendation: Streak recovery notifications

Card 3: Content Preferences
- Stat: "Quran readers have 20% lower churn"
- Chart: Churn rate by favorite content type
- Recommendation: Personalized content mix

Section 2: Cohort Analysis
- Dropdown to select cohort:
  * Ramadan 2024 Converts
  * Long-term Users (1+ year)
  * Premium Subscribers
  * Free Users
  * New Users (<30 days)
  
- For selected cohort, show:
  * Size and churn rate
  * Retention curve chart
  * Top churn drivers
  * Recommended interventions

Section 3: Segment Breakdown
- Pie chart: Risk level distribution
- Breakdown table:
  * High Risk: count, % of total, top characteristics
  * Medium Risk: count, % of total, top characteristics
  * Low Risk: count, % of total, top characteristics
- Download segment CSV button
- Create campaign button (future feature)

Section 4: Intervention Effectiveness (future)
- Track outcomes of interventions
- A/B test results
- ROI calculations
```

### Prompt 5.6: Reusable Components

#### Component: Metrics Cards

```
Create dashboard/components/metrics_cards.py:

Function render_metric_card(label, value, delta=None, delta_color='normal'):
- Create styled metric card
- Show delta with up/down arrow
- Color code: red for negative, green for positive
- Support for custom icons

Function render_metrics_row(metrics_list):
- Create row of metric cards using st.columns()
- Evenly distribute across width
- Handle different numbers of metrics (2-5)
```

#### Component: User Table

```
Create dashboard/components/user_table.py:

Function render_user_table(df, page_size=50):
- Display paginated dataframe
- Apply conditional formatting:
  * High risk: red background
  * Medium risk: yellow background
  * Low risk: green background
- Make columns sortable
- Add row selection checkboxes
- Return selected user IDs

Function render_user_detail_modal(user_id, predictions_df, shap_values):
- Show in st.expander()
- Display all user details
- SHAP waterfall chart
- Engagement history chart
- Intervention recommendations
```

#### Component: Charts

```
Create dashboard/components/charts.py:

Function plot_risk_trend(predictions_over_time_df):
- Line chart of daily high-risk user count
- Plotly for interactivity
- Add reference lines for Ramadan period
- Return fig object

Function plot_confusion_matrix(cm, labels):
- Seaborn heatmap
- Annotations with counts
- Color scale: Blues
- Return fig object

Function plot_roc_curve(fpr, tpr, auc_score):
- Plotly ROC curve
- Add diagonal reference line
- Show AUC in legend
- Return fig object

Function plot_feature_importance(feature_names, importances, top_n=15):
- Horizontal bar chart
- Top N features only
- Sort descending
- Return fig object

Function plot_shap_waterfall(base_value, shap_values, feature_names):
- SHAP waterfall plot
- Show how features push prediction from base to final
- Use shap.plots.waterfall()
- Return fig object
```

#### Component: Explanations

```
Create dashboard/components/explanations.py:

Function render_shap_explanation(user_id, shap_values, feature_values):
- Display top contributing factors as text
- Format as readable sentences:
  * "User hasn't opened app in 15 days (+18% churn risk)"
  * "User was 5x more active during Ramadan (+15% churn risk)"
- Color code positive (red) and negative (green) contributors
- Show SHAP waterfall chart

Function render_intervention_recommendation(user_id, churn_drivers):
- Based on top churn drivers, suggest intervention
- Show as styled card with:
  * Intervention strategy name
  * Specific actions to take
  * Expected success rate
  * Timing recommendation
  * Copy-paste templates for emails/push notifications
```

---

## PHASE 6: TESTING & REFINEMENT (Day 15-18)

### Prompt 6.1: Unit Tests for Features

```
Create tests/test_features.py:

Test calculate_engagement_features():
- Test with normal user data
- Test with new user (<7 days)
- Test with churned user (no recent activity)
- Test edge cases: no events, single event
- Assert output types and ranges

Test calculate_islamic_features():
- Test with Ramadan convert
- Test with long-term user
- Test prayer time calculations
- Test with user who joined after Ramadan

Test calculate_content_features():
- Test with varied content consumption
- Test with single content type
- Test with no content engagement

Run with pytest, aim for >80% coverage
```

### Prompt 6.2: Unit Tests for Model

```
Create tests/test_model.py:

Test model loading:
- Load saved model successfully
- Verify model parameters
- Check feature names match training

Test predictions:
- Predict on sample data
- Verify output shape and types
- Check probability range [0, 1]
- Test batch prediction

Test SHAP generation:
- Generate SHAP for sample users
- Verify explanation structure
- Check top features identified

Test risk categorization:
- Verify HIGH: >70%, MEDIUM: 30-70%, LOW: <30%
```

### Prompt 6.3: API Tests

```
Create tests/test_api.py:

Use FastAPI TestClient

Test /health endpoint:
- Returns 200
- Contains model version

Test /api/v1/predict/batch:
- Valid request returns predictions
- Invalid features return 422
- Empty request handled

Test /api/v1/predict/user/{user_id}:
- Valid user returns prediction
- Non-existent user handled
- Response schema correct

Test authentication:
- Valid API key works
- Invalid API key returns 401
- Missing API key returns 401
```

---

## PHASE 7: DOCUMENTATION & DEPLOYMENT (Day 19-21)

### Prompt 7.1: README.md

```
Create comprehensive README.md:

Structure:
# 🌙 Barakah Retain - Islamic App User Retention Prediction

## Overview
[Project description, problem statement, solution]

## Features
- ✅ 87% accurate churn prediction
- ✅ SHAP-based explainability
- ✅ Interactive dashboard
- ✅ REST API
- ✅ Islamic calendar-aware features

## Demo
- [Live Dashboard Link]
- [Video Walkthrough] (3 min demo)
- [API Documentation]

## Tech Stack
[List all technologies]

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
git clone https://github.com/yourusername/barakah-retain.git
cd barakah-retain
pip install -r requirements.txt
```

### Quick Start

```bash
# Generate sample data
python src/data/data_generator.py

# Train model
python src/models/train_model.py

# Run dashboard
streamlit run dashboard/app.py

# Run API
uvicorn api.main:app --reload
```

## Project Structure

[File tree diagram]

## Features Explained

[Table of all 32 features with descriptions]

## Model Performance

[Metrics and charts]

## API Usage

[Examples with curl/Python]

## Dashboard Guide

[Screenshots and explanations]

## Roadmap

* [ ] Multi-language support (Arabic)
* [ ] Real-time predictions
* [ ] A/B testing framework
* [ ] Integration with CRM tools

## Contributing

[Guidelines]

## License

MIT

## Contact

[Your info]

## Acknowledgments

* Inspired by the need to support Islamic organizations
* Built with ❤️ by Ameen

```

### Prompt 7.2: requirements.txt
```

Create requirements.txt with exact versions:

# Core ML

xgboost==2.0.3
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.24.3
shap==0.43.0
imbalanced-learn==0.11.0

# API

fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0

# Dashboard

streamlit==1.28.2
plotly==5.18.0
matplotlib==3.8.2
seaborn==0.13.0

# Utils

python-dateutil==2.8.2
hijri-converter==2.3.1
pytz==2023.3

# Development

pytest==7.4.3
pytest-cov==4.1.0
black==23.12.0
flake8==6.1.0

# Deployment

docker==7.0.0

```

### Prompt 7.3: Dockerfile
```

Create Dockerfile for deployment:

FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code

COPY . .

# Create data and model directories

RUN mkdir -p data/models data/raw data/processed outputs

# Expose ports

EXPOSE 8000 8501

# Default command (can override for API or dashboard)

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

```

### Prompt 7.4: Deployment to Streamlit Cloud
```

Create deployment guide:

1. Push code to GitHub:
   * Create public repo: barakah-retain
   * Push all code
   * Include .gitignore for data/ and models/
2. Deploy to Streamlit Cloud:
   * Go to share.streamlit.io
   * Connect GitHub repo
   * Select main file: dashboard/app.py
   * Add secrets (if needed for API keys)
   * Deploy
3. Custom domain (optional):
   * Configure in Streamlit settings
   * Point DNS to Streamlit
4. Continuous Deployment:
   * Enable auto-deploy on push to main branch

Note: Streamlit Cloud is free for public apps!

```

---

## REQUIREMENTS.TXT - Complete
```

# Core ML & Data Science

xgboost==2.0.3
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.24.3
scipy==1.11.4
shap==0.43.0
imbalanced-learn==0.11.0

# API Framework

fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6

# Dashboard

streamlit==1.28.2
plotly==5.18.0
matplotlib==3.8.2
seaborn==0.13.0

# Utilities

python-dateutil==2.8.2
hijri-converter==2.3.1
pytz==2023.3
joblib==1.3.2
pyyaml==6.0.1

# ML Experiment Tracking

mlflow==2.9.1

# Development & Testing

pytest==7.4.3
pytest-cov==4.1.0
black==23.12.0
flake8==6.1.0
ipykernel==6.27.1
jupyter==1.0.0

# Deployment

gunicorn==21.2.0

```

---

## CONFIG.YAML - Configuration File
```yaml
# config.yaml
app:
  name: "Barakah Retain"
  version: "1.0.0"
  description: "Islamic App User Retention Prediction"

data:
  raw_path: "data/raw/"
  processed_path: "data/processed/"
  model_path: "data/models/"
  
  simulation:
    n_users: 10000
    date_range_start: "2024-06-01"
    date_range_end: "2024-11-10"
    churn_rate: 0.30
    ramadan_start: "2024-03-11"
    ramadan_end: "2024-04-09"

features:
  engagement_features:
    - days_since_last_session
    - session_frequency_7d
    - session_frequency_30d
    - avg_session_duration
    - total_sessions
    - streak_current
    - streak_longest
    - days_since_signup
    - sessions_per_week
    - weekend_activity_ratio
  
  islamic_features:
    - ramadan_engagement_ratio
    - is_ramadan_convert
    - days_since_ramadan
    - last_10_nights_sessions
    - jummah_participation_rate
    - prayer_time_interaction_rate
    - eid_participation
    - muharram_participation
  
  content_features:
    - quran_reading_pct
    - hadith_engagement_pct
    - lecture_watch_minutes
    - fiqh_content_views
    - seerah_content_views
    - tafsir_engagement
    - topic_diversity_score
    - favorite_content_type
    - content_completion_rate
    - bookmark_count
  
  social_features:
    - friends_count
    - shares_sent
    - comments_made
    - days_since_last_social

model:
  algorithm: "xgboost"
  target: "is_churned"
  
  xgb_params:
    objective: "binary:logistic"
    eval_metric: "auc"
    max_depth: 7
    learning_rate: 0.05
    n_estimators: 200
    subsample: 0.8
    colsample_bytree: 0.8
    min_child_weight: 3
    scale_pos_weight: 3
    random_state: 42
  
  train_test_split:
    test_size: 0.2
    random_state: 42
    stratify: true
  
  imbalance_handling:
    method: "smote"
    sampling_strategy: 0.5

  target_metrics:
    accuracy: 0.85
    precision: 0.80
    recall: 0.75
    f1_score: 0.77
    roc_auc: 0.90

risk_thresholds:
  high: 0.70
  medium: 0.30
  low: 0.0

api:
  host: "0.0.0.0"
  port: 8000
  api_key_header: "X-API-Key"
  rate_limit: 1000  # requests per hour

dashboard:
  page_size: 50
  refresh_interval: 86400  # 24 hours in seconds
  cache_ttl: 3600  # 1 hour

interventions:
  high_risk:
    strategy: "post_ramadan_reengagement"
    actions:
      - "Send personalized email within 24h"
      - "Offer 7-day premium trial"
      - "Push notification with motivational content"
    expected_success_rate: 0.35
  
  medium_risk:
    strategy: "gentle_reminder"
    actions:
      - "Weekly progress summary email"
      - "Streak recovery notification"
    expected_success_rate: 0.25
  
  low_risk:
    strategy: "maintain_engagement"
    actions:
      - "Continue regular notifications"
      - "Personalized content recommendations"
    expected_success_rate: 0.90
```

---

## GITIGNORE

```
# .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb

# Data files (don't commit large datasets)
data/raw/*.csv
data/processed/*.csv
*.pkl
*.joblib

# Model files
data/models/*.pkl
data/models/*.joblib

# Outputs
outputs/
*.png
*.pdf

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local

# Logs
*.log

# MLflow
mlruns/

# Streamlit
.streamlit/secrets.toml
```

---

## 4-WEEK TIMELINE

### Week 1: Data & Features

* **Day 1-2:** Generate synthetic data (Prompts 1.1, 1.2)
* **Day 3-5:** Engineer all features (Prompts 2.1-2.5)
* **Day 6-7:** EDA notebooks, validate data quality

### Week 2: Model Development

* **Day 8-9:** Train XGBoost model (Prompt 3.1)
* **Day 10:** Model evaluation (Prompt 3.2)
* **Day 11:** SHAP explainability (Prompt 3.3)
* **Day 12-14:** Hyperparameter tuning, achieve >85% accuracy

### Week 3: Dashboard & API

* **Day 15-16:** Build FastAPI (Prompts 4.1, 4.2)
* **Day 17-18:** Build Streamlit dashboard pages (Prompts 5.1-5.5)
* **Day 19-20:** Build reusable components (Prompt 5.6)
* **Day 21:** Connect dashboard to API, end-to-end testing

### Week 4: Polish & Deploy

* **Day 22-23:** Write tests (Prompts 6.1-6.3)
* **Day 24-25:** Documentation (Prompts 7.1-7.2)
* **Day 26:** Deploy to Streamlit Cloud
* **Day 27:** Record demo video
* **Day 28:** Final portfolio presentation prep

---

## SUCCESS CHECKLIST

### Technical Deliverables

* [ ] Synthetic dataset (10K users, 6 months data)
* [ ] 32 engineered features
* [ ] XGBoost model with >85% accuracy
* [ ] SHAP explainability for all predictions
* [ ] FastAPI with 6 endpoints
* [ ] Streamlit dashboard with 4 pages
* [ ] Unit tests with >70% coverage
* [ ] Docker containerization

### Portfolio Presentation

* [ ] GitHub repo with clean code
* [ ] Comprehensive README
* [ ] Live demo URL (Streamlit Cloud)
* [ ] 3-5 minute demo video
* [ ] Model performance visualizations
* [ ] Case study writeup

### Interview Talking Points

* [ ] "Post-Ramadan churn prediction"
* [ ] "32 features including Islamic calendar patterns"
* [ ] "87% accuracy with SHAP explainability"
* [ ] "Full-stack: ML pipeline + API + dashboard"
* [ ] "Deployed and accessible online"

---

## BOLT/LOVABLE WORKFLOW

### How to Use These Prompts:

1. **Copy each prompt exactly** as written in the sections above
2. **Paste into Bolt/Lovable** one at a time
3. **Review generated code** before moving to next prompt
4. **Test each component** before integrating
5. **Iterate on prompts** if output needs refinement

### Order of Development:

```
Data Generation → Feature Engineering → Model Training → 
API Development → Dashboard Development → Testing → Documentation
```

### Tips for Bolt/Lovable:

* Be specific about file paths and names
* Request complete functions, not partial code
* Ask for error handling explicitly
* Request docstrings and type hints
* Specify exactly which libraries to import

### After Bolt/Lovable:

Transfer all code to Claude Code for:

* Refactoring and optimization
* Advanced error handling
* Performance improvements
* Additional features
* Production hardening

---

## CONTACT & SUPPORT

**Created by:** Ameen

**Portfolio Project:** Islamic App User Retention Prediction

**Tech Stack:** Python, XGBoost, FastAPI, Streamlit

**License:** MIT

**For Questions:**

* GitHub Issues: [repo-url]/issues
* Email: your-email@example.com

---

**END OF PRD - READY FOR IMPLEMENTATION**

Start with Prompt 1.1 in Bolt/Lovable and work through sequentially. Good luck! 🚀🌙
