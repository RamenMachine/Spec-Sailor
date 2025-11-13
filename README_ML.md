# 🌙 Spec Sailor - Islamic App User Retention Prediction

> ML-powered churn prediction system for Islamic mobile applications

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-blue.svg)](https://reactjs.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-orange.svg)](https://xgboost.readthedocs.io/)

## 📋 Overview

Barakah Retain uses machine learning to predict which users are likely to churn from Islamic mobile apps, enabling targeted retention campaigns. The system achieves **87% accuracy** in predicting churn 7-30 days in advance.

### Key Features

✨ **ML-Powered Predictions**
- XGBoost model with >85% accuracy
- SHAP explainability for every prediction
- Real-time risk scoring (HIGH/MEDIUM/LOW)

🕌 **Islamic Calendar-Aware**
- Ramadan engagement patterns
- Prayer time interaction tracking
- Jummah (Friday) participation metrics
- Post-Ramadan churn detection

📊 **Interactive Dashboard**
- Real-time churn predictions
- User risk segmentation
- SHAP explanations visualization
- Feature importance charts

🚀 **Production-Ready API**
- FastAPI REST endpoints
- Batch prediction support
- CORS-enabled for web apps
- Full API documentation

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Raw Data  │────▶│  Features    │────▶│  XGBoost    │
│ (11M events)│     │ (32 features)│     │   Model     │
└─────────────┘     └──────────────┘     └─────────────┘
                                                 │
                                                 ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    React    │◀────│   FastAPI    │◀────│    SHAP     │
│  Dashboard  │     │   REST API   │     │ Explainer   │
└─────────────┘     └──────────────┘     └─────────────┘
```

## 📊 Model Performance

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Accuracy | >85% | **87%** | ✅ |
| Precision | >80% | **84%** | ✅ |
| Recall | >75% | **79%** | ✅ |
| ROC-AUC | >0.90 | **0.92** | ✅ |

## 🔧 Tech Stack

### Backend
- **Python 3.12** - Core language
- **XGBoost 2.0.3** - ML model
- **scikit-learn 1.3.2** - ML utilities
- **SHAP 0.50** - Model explainability
- **FastAPI 0.104** - REST API framework
- **pandas/numpy** - Data processing

### Frontend
- **React 18.3** - UI framework
- **TypeScript** - Type safety
- **shadcn/ui** - Component library
- **Recharts** - Data visualization
- **TanStack Query** - API state management

### ML Features (32 Total)

#### Engagement (10)
- Days since last session
- Session frequency (7d, 30d)
- Average session duration
- Current/longest streak
- Sessions per week

#### Islamic Calendar (8)
- Ramadan engagement ratio
- Ramadan convert status
- Prayer time interaction rate
- Jummah participation rate
- Last 10 nights sessions

#### Content (10)
- Quran reading percentage
- Lecture watch minutes
- Topic diversity score
- Content completion rate
- Bookmark count

#### Social (4)
- Friends count
- Shares sent
- Comments made
- Days since last social

## 🚀 Quick Start

### Prerequisites

```bash
- Python 3.9+
- Node.js 16+
- npm or yarn
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/barakah-retain.git
cd barakah-retain
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node dependencies**
```bash
npm install
```

4. **Run the complete pipeline**
```bash
python run_pipeline.py
```

This will:
- Generate synthetic data (10K users, 11M events)
- Engineer 32 features
- Train XGBoost model
- Generate SHAP explanations

### Running the Application

**Terminal 1: Start API Server**
```bash
uvicorn api.main:app --reload --port 8000
```

**Terminal 2: Start Frontend**
```bash
npm run dev
```

Visit: `http://localhost:5173`

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /health
```

#### Single User Prediction
```http
GET /api/v1/predict/user/{user_id}
```

Response:
```json
{
  "user_id": "user-000123",
  "churn_probability": 0.75,
  "risk_level": "HIGH",
  "top_risk_factors": [
    "User hasn't opened app in 15 days (+18% risk)",
    "User was 5x more active during Ramadan (+15% risk)"
  ]
}
```

#### SHAP Explanation
```http
GET /api/v1/explain/{user_id}
```

#### Feature Importance
```http
GET /api/v1/model/feature-importance
```

#### Model Performance
```http
GET /api/v1/model/performance
```

Full API docs: `http://localhost:8000/docs`

## 📁 Project Structure

```
barakah-retain/
├── data/
│   ├── raw/                    # Raw event and profile data
│   ├── processed/              # Engineered features
│   └── models/                 # Trained models and configs
├── src/
│   ├── data/                   # Data generation
│   ├── features/               # Feature engineering
│   ├── models/                 # Model training & SHAP
│   ├── services/               # React API service layer
│   └── pages/                  # React pages
├── api/                        # FastAPI backend
│   ├── main.py                 # API entry point
│   └── models.py               # Pydantic schemas
├── tests/                      # Unit tests
├── config.yaml                 # Configuration
├── requirements.txt            # Python dependencies
└── run_pipeline.py             # Pipeline runner
```

## 🔬 Development

### Generate New Data
```bash
python src/data/data_generator.py
```

### Engineer Features
```bash
python src/features/quick_features.py
```

### Train Model
```bash
python src/models/train_model.py
```

### Run Tests
```bash
pytest tests/
```

## 🎯 Use Cases

### For Islamic App Developers
- Identify users at risk of churning
- Personalize retention campaigns
- Optimize post-Ramadan engagement
- Improve user lifetime value

### For Product Managers
- Understand churn drivers
- Prioritize feature development
- Measure intervention effectiveness
- Track retention KPIs

### For Data Scientists
- ML explainability example
- Islamic calendar feature engineering
- Imbalanced classification
- Production ML pipeline

## 📈 Model Training Details

### Data
- **Users:** 10,000 synthetic users
- **Events:** 11.2 million events over 6 months
- **Churn Rate:** 10% (realistic for Islamic apps)

### Features
- **32 engineered features** across 4 categories
- **One-hot encoding** for categorical variables
- **SMOTE** for class imbalance

### Model
- **Algorithm:** XGBoost (Gradient Boosting)
- **Hyperparameters:** Tuned for churn prediction
- **Training Time:** ~2 minutes on standard laptop
- **Inference:** <10ms per prediction

### Explainability
- **SHAP TreeExplainer** for feature attributions
- **Local explanations** for individual predictions
- **Global importance** for model insights

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use for commercial projects

## 🙏 Acknowledgments

- Built to support Islamic organizations in retaining users
- Inspired by the need to maintain spiritual engagement post-Ramadan
- XGBoost and SHAP teams for excellent ML tools

## 📞 Contact

**Created by:** Ameen
**Portfolio Project:** Islamic App User Retention Prediction
**GitHub:** [github.com/yourusername/barakah-retain]

---

**Made with ❤️ for the Muslim tech community**

🌙 *"Barakah" (بركة) means "blessing" in Arabic*
