// TypeScript types for SpecSailor API

export interface PredictionData {
  customerId: string;
  churnProbability: number;
  riskLevel: 'HIGH' | 'MEDIUM' | 'LOW';
  tenureMonths: number;
  contractType: string;
  monthlyCharges: number;
  totalServices: number;
  paymentMethod: string;
  topDriver: string;
}

export interface CustomerData {
  customerId: string;
  userId?: string; // For backward compatibility
  churnProbability: number;
  riskLevel: 'HIGH' | 'MEDIUM' | 'LOW';
  tenureMonths?: number;
  daysInactive?: number; // For backward compatibility
  topDriver: string;
  contractType?: string;
  subscriptionType?: string; // For backward compatibility
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
    // Backward compatibility
    days_since_last_session?: number;
    ramadan_engagement_ratio?: number;
    streak_current?: number;
    session_frequency_7d?: number;
    session_frequency_30d?: number;
    quran_reading_pct?: number;
    prayer_time_interaction_rate?: number;
  };
}
