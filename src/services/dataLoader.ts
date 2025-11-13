/**
 * Static Data Loader for SpecSailor
 * Loads pre-generated predictions and model data from public/data folder
 * Replaces the API service for static GitHub Pages deployment
 */

export interface UserPrediction {
  customerId?: string;
  userId?: string;
  churnProbability: number;
  riskLevel: 'HIGH' | 'MEDIUM' | 'LOW';
  tenureMonths?: number;
  daysInactive?: number;
  topDriver: string;
  contractType?: string;
  subscriptionType?: string;
  signupDate: string;
  lastActive: string;
  features: {
    tenure_months?: number;
    monthly_charges?: number;
    total_charges?: number;
    total_services?: number;
    is_monthly_contract?: number;
    has_internet?: number;
    internet_type?: string;
    payment_method?: string;
    billing_risk_score?: number;
    service_satisfaction_score?: number;
  };
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
}

export interface ConfusionMatrix {
  true_positives: number;
  false_positives: number;
  true_negatives: number;
  false_negatives: number;
}

export interface ModelPerformance {
  metrics: ModelMetrics;
  confusion_matrix: ConfusionMatrix;
  training_date: string;
  model_type: string;
  target_achieved: boolean;
}

export interface FeatureImportance {
  feature: string;
  importance: number;
  rank: number;
}

export interface FeatureImportanceResponse {
  features: FeatureImportance[];
  total_features: number;
}

// Cache for loaded data
let predictionsCache: UserPrediction[] | null = null;
let metricsCache: ModelPerformance | null = null;
let featureImportanceCache: FeatureImportanceResponse | null = null;

/**
 * Get the base URL for fetching data files
 */
const getBaseUrl = () => {
  return import.meta.env.BASE_URL || '/';
};

/**
 * Load all predictions from static JSON file
 */
export const loadPredictions = async (): Promise<UserPrediction[]> => {
  if (predictionsCache) {
    return predictionsCache;
  }

  try {
    const baseUrl = getBaseUrl();
    const response = await fetch(`${baseUrl}data/predictions.json`);
    if (!response.ok) {
      throw new Error(`Failed to load predictions: ${response.statusText}`);
    }
    const data = await response.json();
    predictionsCache = data;
    return data;
  } catch (error) {
    console.error('Error loading predictions:', error);
    throw error;
  }
};

/**
 * Load model performance metrics
 */
export const loadModelMetrics = async (): Promise<ModelPerformance> => {
  if (metricsCache) {
    return metricsCache;
  }

  try {
    const baseUrl = getBaseUrl();
    const response = await fetch(`${baseUrl}data/model_metrics.json`);
    if (!response.ok) {
      throw new Error(`Failed to load metrics: ${response.statusText}`);
    }
    const data = await response.json();
    metricsCache = data;
    return data;
  } catch (error) {
    console.error('Error loading metrics:', error);
    throw error;
  }
};

/**
 * Load feature importance data
 */
export const loadFeatureImportance = async (): Promise<FeatureImportanceResponse> => {
  if (featureImportanceCache) {
    return featureImportanceCache;
  }

  try {
    const baseUrl = getBaseUrl();
    const response = await fetch(`${baseUrl}data/feature_importance.json`);
    if (!response.ok) {
      throw new Error(`Failed to load feature importance: ${response.statusText}`);
    }
    const data = await response.json();
    featureImportanceCache = data;
    return data;
  } catch (error) {
    console.error('Error loading feature importance:', error);
    throw error;
  }
};

/**
 * Get a single prediction by customer ID
 */
export const getPredictionById = async (customerId: string): Promise<UserPrediction | null> => {
  const predictions = await loadPredictions();
  return predictions.find(p => p.customerId === customerId || p.userId === customerId) || null;
};

/**
 * Get predictions filtered by risk level
 */
export const getPredictionsByRisk = async (riskLevel: 'HIGH' | 'MEDIUM' | 'LOW'): Promise<UserPrediction[]> => {
  const predictions = await loadPredictions();
  return predictions.filter(p => p.riskLevel === riskLevel);
};

/**
 * Get summary statistics
 */
export const getPredictionStats = async () => {
  const predictions = await loadPredictions();
  const total = predictions.length;
  const high = predictions.filter(p => p.riskLevel === 'HIGH').length;
  const medium = predictions.filter(p => p.riskLevel === 'MEDIUM').length;
  const low = predictions.filter(p => p.riskLevel === 'LOW').length;

  return {
    total,
    high,
    highPct: Math.round((high / total) * 100),
    medium,
    mediumPct: Math.round((medium / total) * 100),
    low,
    lowPct: Math.round((low / total) * 100),
  };
};

/**
 * Clear cache (useful for testing)
 */
export const clearCache = () => {
  predictionsCache = null;
  metricsCache = null;
  featureImportanceCache = null;
};
