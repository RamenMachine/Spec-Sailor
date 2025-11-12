# SpecSailor - Deployment Guide

This guide will help you deploy both the FastAPI backend and React frontend.

## Prerequisites

- Git repository set up
- Python 3.12+ installed
- Node.js 18+ installed
- Domain name (optional but recommended)

## Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

#### Backend Deployment (FastAPI)

1. **Create a Render account** at https://render.com

2. **Prepare the backend**:
   - Create `requirements.txt` in the root:
     ```
     fastapi
     uvicorn[standard]
     pandas
     numpy
     python-multipart
     ```

3. **Create Render web service**:
   - Go to Render Dashboard → New → Web Service
   - Connect your GitHub repository
   - Configure:
     - **Name**: specsailor-api
     - **Region**: Choose closest to your users
     - **Branch**: main
     - **Root Directory**: Leave empty or set to `api/`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python api/simple_api.py`
     - **Instance Type**: Free

4. **Environment Variables** (if needed):
   - None required for basic setup

5. **Deploy**: Click "Create Web Service"
   - Your API will be available at: `https://specsailor-api.onrender.com`

#### Frontend Deployment (React)

1. **Update API URL**:
   - Edit `.env`:
     ```
     VITE_API_BASE_URL=https://specsailor-api.onrender.com
     ```

2. **Create Render static site**:
   - Go to Render Dashboard → New → Static Site
   - Connect your GitHub repository
   - Configure:
     - **Name**: specsailor
     - **Branch**: main
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`

3. **Deploy**: Click "Create Static Site"
   - Your app will be available at: `https://specsailor.onrender.com`

---

### Option 2: Vercel (Frontend) + Render (Backend)

#### Backend: Same as Option 1 above

#### Frontend (Vercel):

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Update API URL** in `.env`:
   ```
   VITE_API_BASE_URL=https://specsailor-api.onrender.com
   ```

3. **Deploy**:
   ```bash
   vercel --prod
   ```

4. **Follow prompts**:
   - Project name: specsailor
   - Framework: Vite
   - Build command: `npm run build`
   - Output directory: `dist`

---

### Option 3: Railway (Full Stack)

1. **Create Railway account** at https://railway.app

2. **Backend Deployment**:
   - New Project → Deploy from GitHub
   - Select your repository
   - Railway auto-detects Python
   - Add start command: `python api/simple_api.py`
   - Set port: 8000

3. **Frontend Deployment**:
   - Same project → New Service → GitHub
   - Build command: `npm install && npm run build`
   - Start command: `npm run preview`
   - Environment variable:
     ```
     VITE_API_BASE_URL=<your-backend-url>
     ```

---

### Option 4: DigitalOcean App Platform

1. **Create DigitalOcean account**

2. **Backend**:
   - Apps → Create App → GitHub
   - Select repository
   - Detect Python
   - Run command: `python api/simple_api.py`

3. **Frontend**:
   - Add Component → Static Site
   - Build: `npm run build`
   - Output: `dist`

---

## Production Checklist

### Backend (`api/simple_api.py`)

- [ ] Update CORS origins to specific domain (not `*`):
  ```python
  allow_origins=["https://your-frontend-domain.com"]
  ```

- [ ] Add environment variables for sensitive config
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure rate limiting
- [ ] Set up logging

### Frontend

- [ ] Update `.env` with production API URL
- [ ] Remove console.logs
- [ ] Enable production build optimizations
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Configure CDN for assets
- [ ] Add analytics (optional)

### Data Files

Make sure these files are included in deployment:
- `data/processed/features.csv` (7,373 users)
- `data/models/feature_config.json`

### Environment Variables

**Backend**:
- None required for basic setup

**Frontend**:
- `VITE_API_BASE_URL`: Your backend URL
- `NODE_ENV=production`

---

## Testing Deployment

1. **Health Check**:
   ```bash
   curl https://your-backend-url/health
   ```

2. **API Test**:
   ```bash
   curl https://your-backend-url/api/v1/predictions
   ```

3. **Frontend Test**:
   - Open `https://your-frontend-url`
   - Click "Refresh Data"
   - Verify 7,373 users load
   - Check console for errors

---

## Custom Domain Setup

### Frontend (Render/Vercel)
1. Go to Settings → Custom Domain
2. Add your domain (e.g., `specsailor.com`)
3. Update DNS records (provided by platform)

### Backend (Render)
1. Go to Settings → Custom Domain
2. Add subdomain (e.g., `api.specsailor.com`)
3. Update DNS records

---

## Troubleshooting

### CORS Errors
- Update `allow_origins` in `api/simple_api.py`
- Ensure frontend uses correct API URL

### Build Failures
- Check Node.js version (18+)
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

### API 500 Errors
- Check `features.csv` exists in deployment
- Verify Python dependencies installed

### Slow API Response
- First load reads 7,373 users from CSV (may take 2-3 seconds)
- Consider caching or database upgrade for production

---

## Cost Estimation

### Free Tier (Sufficient for Demo/Portfolio)
- **Render**: Free tier for both frontend and backend
- **Vercel**: Free tier (100GB bandwidth/month)
- **Railway**: $5 trial credit

### Paid Tier (Production)
- **Render**: $7/month (backend) + free (frontend)
- **Vercel**: $20/month (Pro)
- **Railway**: ~$10/month
- **DigitalOcean**: $12/month (App Platform)

---

## Recommended Deployment Path

For a portfolio/demo project:
1. **Deploy Backend to Render** (Free tier)
2. **Deploy Frontend to Vercel** (Free tier)
3. **Total Cost: $0**

For production:
1. **Backend**: Render Starter ($7/month)
2. **Frontend**: Vercel Pro ($20/month)
3. **Total Cost**: ~$27/month

---

## Post-Deployment

1. **Monitor Performance**:
   - Set up uptime monitoring (UptimeRobot, StatusCake)
   - Track API response times

2. **Share Your Project**:
   - Add live URL to README
   - Update portfolio
   - Share on LinkedIn/Twitter

3. **Iterate**:
   - Collect user feedback
   - Monitor error logs
   - Optimize performance

---

## Need Help?

- Check logs in deployment platform
- Review CORS and environment variables
- Ensure data files are included in build

**Congratulations on deploying SpecSailor!** 🎉
