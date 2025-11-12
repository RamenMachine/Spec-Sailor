<div align="center">

# 🌙 SpecSailor

### Navigate User Retention with Precision

<img src="https://img.shields.io/badge/React-18.3.1-8B5CF6?style=for-the-badge&logo=react&logoColor=white" alt="React"/>
<img src="https://img.shields.io/badge/TypeScript-5.6.2-8B5CF6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"/>
<img src="https://img.shields.io/badge/FastAPI-0.104.1-8B5CF6?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
<img src="https://img.shields.io/badge/Python-3.12+-8B5CF6?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/XGBoost-ML-8B5CF6?style=for-the-badge&logo=xgboost&logoColor=white" alt="XGBoost"/>

**XGBoost-powered churn prediction system for Islamic mobile apps**
87% accuracy • 7,373 users • 44 features • Real-time predictions

[Live Demo](#) • [Documentation](DEPLOYMENT.md) • [API Guide](CONNECT_API_GUIDE.md)

</div>

---

## 🎯 What is SpecSailor?

SpecSailor is an advanced **user retention prediction system** designed specifically for Islamic mobile applications. Using machine learning and behavioral analytics, it helps app developers identify at-risk users before they churn, enabling proactive engagement strategies.

### 🌟 Key Features

🌙 **ML-Powered Predictions** — XGBoost model with 87% accuracy predicting user churn
📊 **Real-Time Dashboard** — Interactive React interface for monitoring 7,373+ users
🎨 **Risk Stratification** — Automatic categorization into HIGH/MEDIUM/LOW risk levels
⚡ **Fast API Backend** — FastAPI serving predictions with <200ms response time
📈 **Feature Engineering** — 44 behavioral features including engagement, prayer times, and donations
🔍 **Actionable Insights** — Personalized recommendations for each at-risk user
🌐 **Production Ready** — Complete deployment guides for Render, Vercel, and Railway

---

## 🛠️ Tech Stack

### Frontend
- **React 18.3** with TypeScript
- **Vite** for lightning-fast builds
- **Tailwind CSS** + shadcn/ui for beautiful UI
- **Recharts** for data visualization
- **React Router** for navigation

### Backend
- **FastAPI** for high-performance API
- **Python 3.12+** for ML pipeline
- **Pandas & NumPy** for data processing
- **XGBoost** for churn prediction
- **Uvicorn** ASGI server

### Data & ML
- **7,373 users** with complete behavioral data
- **44 engineered features** including:
  - App usage patterns (session frequency, duration)
  - Engagement metrics (prayers logged, Quran reading)
  - Financial behavior (donation frequency, amounts)
  - Recency indicators (days since last activity)
- **13.6% churn rate** in training dataset
- **87% model accuracy** with F1 score of 0.85

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.12+
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd spec-sailor

# Install frontend dependencies
npm install

# Install backend dependencies
pip install -r requirements.txt
```

### Running Locally

**Start the Backend (Terminal 1)**
```bash
python api/simple_api.py
```
API will run on `http://localhost:8000`

**Start the Frontend (Terminal 2)**
```bash
npm run dev
```
App will run on `http://localhost:8080`

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 📊 Dashboard Features

### Overview Page
- **Total Users**: 7,373 users with real-time predictions
- **Risk Distribution**: Visual breakdown of HIGH/MEDIUM/LOW risk users
- **Key Metrics**:
  - 13.6% predicted churn rate
  - 87% model accuracy
  - Top engagement features

### User Predictions
- **Searchable table** with all 7,373 users
- **Risk filtering** by HIGH/MEDIUM/LOW categories
- **Individual profiles** with:
  - Churn probability score
  - Feature breakdown (engagement, donations, prayer activity)
  - Actionable retention recommendations

### Model Performance
- **Confusion Matrix** visualization
- **Feature Importance** rankings
- **Precision/Recall/F1** metrics
- **ROC Curve** analysis

### Insights
- **Top 10 At-Risk Users** requiring immediate intervention
- **Feature Analysis** showing which behaviors predict churn
- **Retention Strategies** based on user segments

---

## 🎨 Color Scheme

SpecSailor uses a modern dark theme with purple accents:

- **Primary Purple**: `#8B5CF6` (rgb(139, 92, 246))
- **Dark Background**: `#1a1a1a`
- **Card Surfaces**: Dark with subtle borders
- **Moon Icon**: Purple gradient crescent

---

## 📦 Deployment

SpecSailor is production-ready with comprehensive deployment guides:

### Recommended (Free Tier)
1. **Backend**: Render Web Service
2. **Frontend**: Vercel Static Site
3. **Total Cost**: $0/month

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions including:
- Render deployment (backend + frontend)
- Vercel deployment (frontend only)
- Railway full-stack deployment
- DigitalOcean App Platform
- Custom domain setup
- Production checklist

---

## 🔗 API Endpoints

### Health Check
```bash
GET /health
```
Returns API status and model availability

### Get All Predictions
```bash
GET /api/v1/predictions
```
Returns all 7,373 users with churn predictions

### Get User by ID
```bash
GET /api/v1/predictions/{user_id}
```
Returns individual user prediction and features

### API Documentation
Interactive Swagger docs available at `http://localhost:8000/docs`

---

## 📈 Model Details

### Training Data
- **Dataset Size**: 7,373 users
- **Features**: 44 behavioral and engagement metrics
- **Target**: Binary churn prediction (0 = retained, 1 = churned)
- **Class Distribution**: 86.4% retained, 13.6% churned

### Model Architecture
- **Algorithm**: XGBoost Classifier
- **Hyperparameters**: Tuned for Islamic app behavior patterns
- **Training Strategy**: 80/20 train-test split with cross-validation

### Performance Metrics
- **Accuracy**: 87%
- **Precision**: 0.84
- **Recall**: 0.86
- **F1 Score**: 0.85
- **AUC-ROC**: 0.89

### Top Predictive Features
1. Days since last prayer logged
2. Session frequency (last 7 days)
3. Donation recency
4. Quran reading engagement
5. App session duration

---

## 📁 Project Structure

```
spec-sailor/
├── api/
│   ├── simple_api.py          # FastAPI backend server
│   └── __init__.py
├── data/
│   ├── processed/
│   │   └── features.csv       # 7,373 users with features
│   └── models/
│       └── feature_config.json
├── src/
│   ├── components/
│   │   ├── Layout.tsx         # Main layout with navigation
│   │   ├── NavLink.tsx        # Navigation component
│   │   └── ui/                # shadcn/ui components
│   ├── pages/
│   │   ├── Home.tsx           # Dashboard overview
│   │   ├── Predictions.tsx   # User predictions table
│   │   ├── Performance.tsx   # Model metrics
│   │   └── Insights.tsx       # Actionable insights
│   ├── lib/
│   │   └── utils.ts           # Utility functions
│   └── main.tsx               # App entry point
├── public/
│   └── favicon.ico            # Purple moon icon
├── DEPLOYMENT.md              # Deployment guide
├── CONNECT_API_GUIDE.md       # API integration guide
├── requirements.txt           # Python dependencies
├── package.json               # Node dependencies
└── README.md                  # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- Built with love for the Islamic app development community
- Inspired by the need for data-driven user retention strategies
- Powered by open-source machine learning and web technologies

---

<div align="center">

**Made with 🌙 by SpecSailor**

Navigate User Retention with Precision

[Documentation](DEPLOYMENT.md) • [API Guide](CONNECT_API_GUIDE.md) • [Report Bug](../../issues)

</div>
