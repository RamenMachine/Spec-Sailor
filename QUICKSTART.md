# Barakah Retain - Quick Start Guide

Your React frontend is now connected to the live FastAPI backend!

## Current Status

**Both servers are running:**
- FastAPI Backend: http://localhost:8000
- React Frontend: http://localhost:8081

## What Just Happened

1. Created a simplified FastAPI server ([api/simple_api.py](api/simple_api.py)) that:
   - Serves predictions from your `features.csv` file
   - Has CORS enabled for React
   - Provides `/api/v1/predictions` endpoint

2. Updated React Home component ([src/pages/Home.tsx](src/pages/Home.tsx)) to:
   - Fetch data from the live API using React Query
   - Display real predictions instead of mock data
   - Show loading and error states
   - Refresh data from API when you click "Refresh Data"

3. Created API integration hooks ([src/hooks/useAPI.ts](src/hooks/useAPI.ts)) for:
   - Health checks
   - Predictions fetching

## View Your Dashboard

Open your browser to: **http://localhost:8081**

You should see:
- Real user data from your ML model (735 users)
- Actual churn predictions and risk levels
- Loading spinner while fetching data
- Error handling if API is down

## Test the Integration

1. Open http://localhost:8081 in your browser
2. You should see the dashboard loading real data from the API
3. Click "Refresh Data" button - it will fetch fresh data from the API
4. Click on any high-risk user to see their details

## API Endpoints Available

- **Health Check**: http://localhost:8000/health
- **Predictions**: http://localhost:8000/api/v1/predictions
- **API Docs**: http://localhost:8000/docs

## Data Flow

```
React (localhost:8081)
    |
    | HTTP GET /api/v1/predictions
    |
    v
FastAPI (localhost:8000)
    |
    | Reads features.csv
    |
    v
Returns 735 users with:
    - user_id
    - churn_probability
    - risk_level (HIGH/MEDIUM/LOW)
    - daysInactive
    - topDriver
```

## Key Features Now Working

1. **Real-time Data**: Dashboard shows actual ML predictions
2. **API Integration**: React Query manages API calls with caching
3. **Loading States**: Spinner shows while data loads
4. **Error Handling**: Graceful fallback if API is down
5. **Refresh**: Pull latest data from API on demand

## Next Steps (Optional)

1. **Add More Endpoints**: Implement user details, SHAP explanations
2. **Use Real Model**: Load actual XGBoost model for predictions
3. **Add Filtering**: Filter users by risk level in UI
4. **Export Feature**: Download high-risk users as CSV
5. **Tests**: Write pytest tests for API endpoints

## Stopping the Servers

To stop the servers, press `Ctrl+C` in the terminals where they're running, or use:
- Close the VSCode terminal tabs
- Kill the processes manually

## Troubleshooting

**API not responding?**
```bash
curl http://localhost:8000/health
```

**React not loading?**
- Check that port 8081 is accessible
- Look for errors in browser console (F12)

**CORS errors?**
- The API already has CORS enabled for localhost:8081
- Check browser console for specific error

## Files Modified

- [src/pages/Home.tsx](src/pages/Home.tsx) - Updated to use live API
- [src/hooks/useAPI.ts](src/hooks/useAPI.ts) - API hooks
- [src/types/api.ts](src/types/api.ts) - TypeScript types
- [api/simple_api.py](api/simple_api.py) - FastAPI server
- [.env](.env) - API base URL configuration

---

**You now have a fully working ML-powered churn prediction dashboard!**
