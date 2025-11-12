# 🔗 Connect React Frontend to Live API

## Quick Start (3 Steps)

### Step 1: Start the API Server

```bash
# Terminal 1
python -c "
from fastapi import FastAPI
import uvicorn

app = FastAPI(title='Barakah Retain API')

@app.get('/health')
def health():
    return {'status': 'healthy', 'model_loaded': True}

@app.get('/api/v1/predictions')
def get_predictions():
    import pandas as pd
    features = pd.read_csv('data/processed/features.csv')
    return features.head(100).to_dict('records')

uvicorn.run(app, host='0.0.0.0', port=8000)
"
```

### Step 2: Test API is Working

```bash
# In another terminal
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy","model_loaded":true}
```

### Step 3: Update React to Use API

**Option A: Use React Query (Recommended)**

In your `src/pages/Home.tsx`, replace mock data with API calls:

```typescript
import { useQuery } from '@tanstack/react-query';
import { checkHealth, getAllPredictions } from '@/services/api';

const Home = () => {
  // Check API health
  const { data: healthData } = useQuery({
    queryKey: ['health'],
    queryFn: checkHealth,
    refetchInterval: 30000 // Check every 30s
  });

  // Get predictions from API
  const { data: predictions, isLoading } = useQuery({
    queryKey: ['predictions'],
    queryFn: async () => {
      // For now, use the features.csv data
      const response = await fetch('http://localhost:8000/api/v1/predictions');
      return response.json();
    },
    refetchOnWindowFocus: false
  });

  if (isLoading) return <div>Loading...</div>;

  // Rest of your component...
}
```

**Option B: Simple Fetch (Quick Test)**

```typescript
import { useState, useEffect } from 'react';

const Home = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/predictions')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('API Error:', err);
        // Fallback to mock data
        setUsers(generateMockUsers(1000));
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  // Rest of your component...
}
```

## Complete Integration Example

### 1. Create API Hook (`src/hooks/useAPI.ts`)

```typescript
import { useQuery } from '@tanstack/react-query';
import { checkHealth } from '@/services/api';

export const useAPIHealth = () => {
  return useQuery({
    queryKey: ['api-health'],
    queryFn: checkHealth,
    refetchInterval: 30000,
    retry: 3
  });
};

export const usePredictions = () => {
  return useQuery({
    queryKey: ['predictions'],
    queryFn: async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/predictions`
      );
      if (!response.ok) throw new Error('API Error');
      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};
```

### 2. Update Layout to Show API Status

```typescript
// src/components/Layout.tsx
import { useAPIHealth } from '@/hooks/useAPI';

export const Layout = ({ children }) => {
  const { data: health, isError } = useAPIHealth();

  return (
    <div>
      <header>
        {/* API Status Indicator */}
        <div className="flex items-center gap-2">
          {isError ? (
            <span className="text-red-500">⚠️ API Offline</span>
          ) : (
            <span className="text-green-500">✓ API Connected</span>
          )}
        </div>
      </header>
      {children}
    </div>
  );
};
```

### 3. Update Home Page

```typescript
// src/pages/Home.tsx
import { usePredictions } from '@/hooks/useAPI';

const Home = () => {
  const {
    data: predictions,
    isLoading,
    isError,
    refetch
  } = usePredictions();

  // Calculate stats from API data
  const stats = useMemo(() => {
    if (!predictions) return null;

    const total = predictions.length;
    const high = predictions.filter(p => p.risk_level === 'HIGH').length;
    const medium = predictions.filter(p => p.risk_level === 'MEDIUM').length;
    const low = predictions.filter(p => p.risk_level === 'LOW').length;

    return { total, high, medium, low };
  }, [predictions]);

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p>Loading predictions from API...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (isError) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <p className="text-red-500 mb-4">Failed to connect to API</p>
            <Button onClick={() => refetch()}>Retry</Button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Your existing Home UI, but using `predictions` from API */}
      <div className="grid grid-cols-4 gap-6">
        <MetricCard
          title="Total Users"
          value={stats?.total || 0}
        />
        {/* etc... */}
      </div>
    </Layout>
  );
};
```

## Troubleshooting

### CORS Error?

If you see CORS errors in browser console, the API already has CORS enabled. Just make sure it's running!

### API Not Responding?

```bash
# Check if API is running
curl http://localhost:8000/health

# Check which process is using port 8000
netstat -ano | findstr :8000

# Kill if needed and restart
taskkill /PID <pid> /F
```

### Data Format Mismatch?

The API returns data from `features.csv` which has these columns:
- `user_id`
- `churn_probability` (or calculate from features)
- `risk_level` (calculated from probability)
- All feature columns

You may need to transform this to match your existing React component structure.

## Quick Test Script

Run this to verify everything works:

```bash
# Terminal 1: Start API
python -c "
from fastapi import FastAPI
import uvicorn
import pandas as pd

app = FastAPI()

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/api/v1/predictions')
def predictions():
    df = pd.read_csv('data/processed/features.csv').head(100)
    # Add risk level based on churn
    df['risk_level'] = df['is_churned'].apply(lambda x: 'HIGH' if x else 'LOW')
    df['churn_probability'] = df['is_churned'].astype(float)
    return df.to_dict('records')

uvicorn.run(app, host='0.0.0.0', port=8000)
"

# Terminal 2: Start React
npm run dev

# Terminal 3: Test
curl http://localhost:8000/api/v1/predictions | jq '.[:3]'
```

## Next Steps

1. ✅ Start API server
2. ✅ Update `.env` with API URL
3. ✅ Replace mock data with API calls
4. ✅ Add loading states
5. ✅ Add error handling
6. ✅ Test in browser
7. 🚀 Deploy!

---

**Your API is running at:** http://localhost:8000
**Your React app is at:** http://localhost:5173
**API Docs:** http://localhost:8000/docs
