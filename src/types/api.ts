export interface PredictionData {
  user_id: string;
  churn_probability: number;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  daysInactive: number;
  session_frequency_7d: number;
  avg_session_duration: number;
  ramadan_engagement_ratio: number;
  is_churned: boolean;
  topDriver: string;
}

export interface UserData {
  userId: string;
  churnProbability: number;
  riskLevel: 'HIGH' | 'MEDIUM' | 'LOW';
  daysInactive: number;
  topDriver: string;
}
