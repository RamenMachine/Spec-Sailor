# 🌙 SpecSailor

### Navigate User Retention with Precision

<img src="https://img.shields.io/badge/React-18.3.1-8B5CF6?style=for-the-badge&logo=react&logoColor=white" alt="React"/>
<img src="https://img.shields.io/badge/TypeScript-5.6.2-8B5CF6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"/>
<img src="https://img.shields.io/badge/FastAPI-0.104.1-8B5CF6?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
<img src="https://img.shields.io/badge/Python-3.12-8B5CF6?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/XGBoost-ML-8B5CF6?style=for-the-badge" alt="XGBoost"/>

---

## 📖 Overview

SpecSailor is a **machine learning-powered user retention prediction system** designed for Islamic app developers. It analyzes user behavior patterns to predict churn risk and provides actionable insights for retention strategies.

### Key Features
- 🎯 **Real-time Predictions**: ML-powered churn probability for each user
- 📊 **Interactive Dashboard**: Beautiful dark-themed analytics interface
- 🔍 **Risk Segmentation**: Automatic HIGH/MEDIUM/LOW risk classification
- 💡 **Actionable Insights**: Data-driven retention recommendations
- 🚀 **Production Ready**: Deployed on Railway (backend) with Vercel-ready frontend

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.12+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/spec-sailor.git
cd spec-sailor
```

2. **Install frontend dependencies**
```bash
npm install
```

3. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000
```

5. **Run the application**

Terminal 1 - Start backend:
```bash
python api/simple_api.py
```

Terminal 2 - Start frontend:
```bash
npm run dev
```

6. **Open your browser**
Navigate to `http://localhost:8080`

---

## 📊 Dashboard Features

### 🏠 Home Page
- **Total Users**: 7,373 users with real-time predictions
- **Risk Distribution**: Visual breakdown of HIGH/MEDIUM/LOW risk users
- **Key Metrics**: Churn rate, model accuracy, top features

### 👥 User Predictions
- **Searchable table** with all users and churn probabilities
- **Risk filtering** by category
- **Individual profiles** with detailed feature breakdowns

### 📈 Model Performance
- **Confusion Matrix** visualization
- **Feature Importance** rankings
- **Precision/Recall/F1** metrics

### 💡 Insights
- **Top 10 At-Risk Users** requiring immediate intervention
- **Feature Analysis** showing which behaviors predict churn
- **Retention Strategies** based on ML analysis

---

## 🎨 Color Scheme

SpecSailor uses a modern dark theme with purple accents:

- **Primary Purple**: `#8B5CF6`
- **Dark Background**: `#1a1a1a`
- **Card Surfaces**: Dark with subtle borders
- **Moon Icon**: Purple gradient crescent

---

## 📦 Project Structure

```
spec-sailor/
├── api/                    # Backend API
│   ├── simple_api.py      # FastAPI application
│   └── __init__.py
├── data/                   # Data storage
│   ├── processed/         # Processed features
│   │   └── features.csv   # Pre-generated user features
│   └── models/            # ML models
│       ├── xgboost_model.json
│       └── feature_importance.csv
├── src/                    # Frontend React app
│   ├── components/        # UI components
│   ├── pages/            # Page components
│   ├── hooks/            # React hooks
│   └── types/            # TypeScript types
├── requirements.txt       # Python dependencies
├── package.json          # Node dependencies
└── README.md

```

---

## 🔗 API Endpoints

### Health Check
```bash
GET /health
```

### Get Predictions
```bash
GET /api/v1/predictions
```
Returns churn predictions for all users with risk levels and feature breakdowns.

### API Documentation
```bash
GET /docs
```
Interactive Swagger UI documentation

---

## 🚢 Deployment

### Backend (Railway)
SpecSailor backend is deployed on Railway:
- **URL**: `https://spec-sailor-production.up.railway.app`
- **Status**: ✅ Live
- **Auto-deploy**: Enabled from `main` branch

### Frontend (Vercel)
Frontend can be deployed to Vercel:
1. Connect your GitHub repository
2. Framework: Vite
3. Build command: `npm run build`
4. Output directory: `dist`
5. Environment variable: `VITE_API_BASE_URL=https://spec-sailor-production.up.railway.app`

---

## 🛠️ Tech Stack

### Frontend
- **React 18.3** with TypeScript
- **Vite** for blazing-fast builds
- **TanStack React Query** for data fetching
- **shadcn/ui** components
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **Lucide React** for icons

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas & NumPy** - Data processing
- **Uvicorn** - ASGI server
- **Python 3.12**

### Machine Learning
- **XGBoost** - Gradient boosting classifier
- **Pre-trained model** on 7,373 users
- **Feature engineering** from user behavior data

---

## 📚 Usage

### For Islamic App Developers

1. **Fork this repository**
2. **Replace the data**:
   - Add your user event logs to generate features
   - Train a new model using your data (see ML pipeline in git history)
3. **Customize the features**:
   - Modify feature engineering for your app's metrics
   - Update risk thresholds based on your business needs
4. **Deploy**:
   - Backend to Railway
   - Frontend to Vercel
   - Update API URL in environment variables

### GitHub-Based Workflow

SpecSailor is designed for a **GitHub-centric workflow**:

1. **Data Analysis**: Clone repo → Add your data → Run feature pipeline
2. **Model Training**: Train XGBoost model on your features
3. **Deploy**: Push to GitHub → Automatic deployment
4. **Dashboard**: View predictions in beautiful UI

The frontend is a **showcase/demo interface** - the real power is in using the GitHub workflow to analyze your own data!

---

## 🤝 Contributing

This is a demo project showcasing ML-powered retention prediction. Feel free to:
- Fork for your own Islamic app
- Open issues for bugs
- Submit PRs for improvements

---

## 📄 License

MIT License - feel free to use for your Islamic apps!

---

## 🌟 Acknowledgments

Built with love for the Muslim dev community. May Allah accept our efforts to create beneficial technology.

---

**🌙 SpecSailor - Navigate User Retention with Precision**
