# SpecSailor - Railway Deployment Guide

Complete step-by-step guide to deploy SpecSailor to Railway.

## Prerequisites
- GitHub account with your SpecSailor repository
- Railway account (sign up at https://railway.app)
- Git installed locally

---

## Step 1: Prepare Your Repository

The following files have been configured for Railway:
- ✅ `Procfile` - Tells Railway how to start the backend
- ✅ `railway.json` - Railway configuration
- ✅ `nixpacks.toml` - Build configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `api/simple_api.py` - Updated to use PORT environment variable

---

## Step 2: Commit and Push Changes

```bash
cd spec-sailor
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

---

## Step 3: Deploy Backend to Railway

### 3.1 Create Railway Account
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign in with GitHub

### 3.2 Deploy from GitHub
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `spec-sailor` repository
4. Railway will auto-detect it as a Python project

### 3.3 Configure Backend Service
Railway will automatically:
- Detect `requirements.txt` and install Python dependencies
- Use the `Procfile` or `nixpacks.toml` start command
- Assign a PORT environment variable
- Generate a public URL

**Important**: Your backend will be available at something like:
`https://spec-sailor-production.up.railway.app`

### 3.4 Verify Backend Deployment
1. Wait for build to complete (2-3 minutes)
2. Click on your service → "Settings" → copy the public URL
3. Test the API:
   - Open `https://your-backend-url.railway.app/health`
   - Should return: `{"status": "healthy", "message": "SpecSailor API is running!"}`
4. Check API docs:
   - Open `https://your-backend-url.railway.app/docs`

---

## Step 4: Deploy Frontend to Railway

### 4.1 Add Frontend Service
1. In your Railway project, click "New"
2. Select "GitHub Repo" again
3. Choose the same `spec-sailor` repository
4. Railway will create a second service

### 4.2 Configure Frontend Build
1. Click on the frontend service
2. Go to "Settings" → "Build"
3. Set build command:
   ```
   npm install && npm run build
   ```
4. Set start command (Railway should auto-detect):
   ```
   npm run preview
   ```

### 4.3 Add Environment Variable
1. In frontend service → "Variables"
2. Add new variable:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: Your backend URL (e.g., `https://spec-sailor-production.up.railway.app`)
3. Click "Add" and redeploy

### 4.4 Configure Vite Preview Server
Create or update `package.json` scripts:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview --host 0.0.0.0 --port $PORT"
  }
}
```

---

## Step 5: Configure CORS (Optional but Recommended)

Update `api/simple_api.py` to only allow your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.railway.app",
        "http://localhost:8080"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push:
```bash
git add api/simple_api.py
git commit -m "Restrict CORS to frontend domain"
git push origin main
```

Railway will auto-redeploy.

---

## Step 6: Test Full Deployment

### 6.1 Test Backend
```bash
# Health check
curl https://your-backend-url.railway.app/health

# Get predictions
curl https://your-backend-url.railway.app/api/v1/predictions
```

### 6.2 Test Frontend
1. Open your frontend URL: `https://your-frontend-url.railway.app`
2. Click "Refresh Data" button
3. Should load 7,373 users
4. Check browser console for any CORS errors
5. Navigate to all 4 pages:
   - Home (Dashboard)
   - User Predictions
   - Model Performance
   - Insights

---

## Step 7: Custom Domain (Optional)

### Backend Domain
1. Go to backend service → "Settings" → "Domains"
2. Click "Add Domain"
3. Enter: `api.specsailor.com`
4. Add CNAME record to your DNS:
   - **Name**: `api`
   - **Value**: Provided by Railway

### Frontend Domain
1. Go to frontend service → "Settings" → "Domains"
2. Click "Add Domain"
3. Enter: `specsailor.com`
4. Add DNS records as provided by Railway

---

## Troubleshooting

### Backend Issues

**Build fails with "No module named 'pandas'"**
- Check `requirements.txt` is in root directory
- Ensure all dependencies are listed

**API returns 502 Bad Gateway**
- Check logs: Service → "Deployments" → Click latest → "View Logs"
- Ensure `PORT` environment variable is used in `simple_api.py`

**Data file not found error**
- Verify `data/processed/features.csv` is committed to git
- Check `.gitignore` doesn't exclude it:
  ```
  !data/processed/features.csv
  ```

### Frontend Issues

**CORS errors in browser console**
- Update `api/simple_api.py` CORS `allow_origins` with frontend URL
- Commit and push changes

**Environment variable not working**
- Check Railway Variables tab has `VITE_API_BASE_URL`
- Environment variables must start with `VITE_` for Vite
- Redeploy after adding variables

**Build succeeds but shows blank page**
- Check browser console for errors
- Verify API URL is correct in `.env` or Railway Variables
- Check that `npm run preview` works locally

---

## Cost & Limits

### Railway Free Tier
- **$5 trial credit** (no credit card required)
- **500 hours/month** of execution time
- **100GB outbound bandwidth**
- **1GB RAM per service**

### Estimated Usage
- **Backend**: ~$3-5/month
- **Frontend**: ~$2-3/month
- **Total**: ~$5-8/month (after free trial)

---

## Monitoring & Logs

### View Logs
1. Railway Dashboard → Select service
2. Click "Deployments"
3. Click on deployment → "View Logs"

### Metrics
1. Service → "Metrics" tab
2. View:
   - CPU usage
   - Memory usage
   - Network traffic
   - Request count

### Alerts (Pro Plan)
- Set up alerts for downtime
- Get notified via email/Slack

---

## Environment Variables Reference

### Backend (Python)
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | Yes | 8000 | Railway assigns this automatically |

### Frontend (React)
| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `VITE_API_BASE_URL` | Yes | `https://spec-sailor-production.up.railway.app` | Backend API URL |

---

## Useful Railway Commands

### Railway CLI (Optional)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run command in Railway environment
railway run npm run dev

# Open project in browser
railway open
```

---

## Quick Checklist

Before deploying, ensure:
- [ ] `requirements.txt` in root with all Python dependencies
- [ ] `Procfile`, `railway.json`, and `nixpacks.toml` created
- [ ] `api/simple_api.py` uses `os.getenv("PORT", 8000)`
- [ ] `data/processed/features.csv` is committed
- [ ] All changes pushed to GitHub
- [ ] Railway account created and connected to GitHub
- [ ] Backend service deployed and tested
- [ ] Frontend service deployed with `VITE_API_BASE_URL` variable
- [ ] Full app tested (load users, navigate pages)

---

## Next Steps After Deployment

1. **Update README**: Add live demo links
2. **Monitor Performance**: Check Railway metrics daily
3. **Set Up Alerts**: Configure uptime monitoring
4. **Optimize**:
   - Add caching for API responses
   - Compress frontend assets
   - Use CDN for static files
5. **Scale** (if needed):
   - Upgrade Railway plan for more resources
   - Add database instead of CSV
   - Implement rate limiting

---

## Support

**Railway Issues**:
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app

**SpecSailor Issues**:
- GitHub Issues: https://github.com/RamenMachine/spec-sailor/issues
- Check logs in Railway Dashboard
- Review CORS settings if frontend can't connect

---

**Congratulations on deploying SpecSailor to Railway!** 🚂🎉

Your ML-powered retention system is now live and accessible worldwide!
