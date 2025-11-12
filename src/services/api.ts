/**
 * API Service Layer for Barakah Retain
 * Connects React frontend to FastAPI backend
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = 30000; // 30 seconds

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add API key if needed
    const apiKey = import.meta.env.VITE_API_KEY;
    if (apiKey) {
      config.headers['X-API-Key'] = apiKey;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message);
    } else {
      // Error setting up request
      console.error('Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Types
export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  model_version: string;
  timestamp: string;
}

export interface UserPrediction {
  user_id: string;
  churn_probability: number;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  top_risk_factors: string[];
}

export interface BatchPredictionResponse {
  predictions: UserPrediction[];
  total_users: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
}

export interface FeatureContribution {
  feature: string;
  value: number;
  shap_value: number;
  impact: string;
  explanation: string;
}

export interface SHAPExplanation {
  user_id: string;
  churn_probability: number;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  base_value: number;
  prediction: number;
  top_positive_contributors: FeatureContribution[];
  top_negative_contributors: FeatureContribution[];
  explanations: string[];
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

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
}

export interface ConfusionMatrix {
  true_negatives: number;
  false_positives: number;
  false_negatives: number;
  true_positives: number;
}

export interface ModelPerformanceResponse {
  metrics: ModelMetrics;
  confusion_matrix: ConfusionMatrix;
  training_date: string;
  model_type: string;
  target_achieved: boolean;
}

// API Methods

/**
 * Health check
 */
export const checkHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>('/health');
  return response.data;
};

/**
 * Get prediction for single user
 */
export const predictUser = async (userId: string): Promise<UserPrediction> => {
  const response = await apiClient.get<UserPrediction>(`/api/v1/predict/user/${userId}`);
  return response.data;
};

/**
 * Get batch predictions
 */
export const predictBatch = async (users: any[]): Promise<BatchPredictionResponse> => {
  const response = await apiClient.post<BatchPredictionResponse>('/api/v1/predict/batch', {
    users,
  });
  return response.data;
};

/**
 * Get SHAP explanation for user
 */
export const explainUser = async (userId: string): Promise<SHAPExplanation> => {
  const response = await apiClient.get<SHAPExplanation>(`/api/v1/explain/${userId}`);
  return response.data;
};

/**
 * Get feature importance
 */
export const getFeatureImportance = async (): Promise<FeatureImportanceResponse> => {
  const response = await apiClient.get<FeatureImportanceResponse>('/api/v1/model/feature-importance');
  return response.data;
};

/**
 * Get model performance metrics
 */
export const getModelPerformance = async (): Promise<ModelPerformanceResponse> => {
  const response = await apiClient.get<ModelPerformanceResponse>('/api/v1/model/performance');
  return response.data;
};

/**
 * Get all predictions (from features.csv via API if available, or mock)
 */
export const getAllPredictions = async (): Promise<UserPrediction[]> => {
  try {
    // In production, this would be a paginated endpoint
    // For now, we'll use a mock or batch predict
    const response = await apiClient.get<UserPrediction[]>('/api/v1/predictions/all');
    return response.data;
  } catch (error) {
    // Fallback: return empty array or mock data
    console.warn('All predictions endpoint not available, using fallback');
    return [];
  }
};

/**
 * Get predictions with filters
 */
export const getFilteredPredictions = async (filters: {
  risk_level?: string;
  subscription_type?: string;
  limit?: number;
  offset?: number;
}): Promise<UserPrediction[]> => {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined) {
      params.append(key, value.toString());
    }
  });

  try {
    const response = await apiClient.get<UserPrediction[]>(`/api/v1/predictions?${params}`);
    return response.data;
  } catch (error) {
    console.warn('Filtered predictions not available');
    return [];
  }
};

/**
 * Check if API is available
 */
export const isApiAvailable = async (): Promise<boolean> => {
  try {
    await checkHealth();
    return true;
  } catch (error) {
    return false;
  }
};

/**
 * Error handler utility
 */
export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.detail || error.response.data?.error || error.message;
      return `API Error: ${message}`;
    } else if (error.request) {
      // Request made but no response
      return 'Network Error: Unable to reach the server. Please check your connection.';
    }
  }
  return 'An unexpected error occurred. Please try again.';
};

// Export default client for advanced usage
export default apiClient;
