// Mock data for Telco Customer Churn model performance metrics
// Based on XGBoost model evaluation results

export type RiskLevel = 'HIGH' | 'MEDIUM' | 'LOW';

export interface UserPrediction {
  customerId?: string;
  userId?: string; // For backward compatibility
  churnProbability: number;
  riskLevel: RiskLevel;
  tenureMonths?: number;
  daysInactive?: number; // For backward compatibility
  topDriver: string;
  contractType?: string;
  subscriptionType?: 'free' | 'basic' | 'premium' | 'monthly' | 'yearly' | 'biennial'; // For backward compatibility
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
    // Backward compatibility fields
    days_since_last_session?: number;
    ramadan_engagement_ratio?: number;
    streak_current?: number;
    session_frequency_7d?: number;
    session_frequency_30d?: number;
    quran_reading_pct?: number;
    prayer_time_interaction_rate?: number;
  };
}

export const modelMetrics = {
  accuracy: 0.81,
  precision: 0.78,
  recall: 0.73,
  rocAuc: 0.87
};

export const featureImportance = [
  { feature: 'contract_type_Month-to-month', importance: 0.22 },
  { feature: 'tenure_months', importance: 0.18 },
  { feature: 'payment_method_Electronic check', importance: 0.15 },
  { feature: 'monthly_charges', importance: 0.12 },
  { feature: 'total_services', importance: 0.10 },
  { feature: 'is_monthly_contract', importance: 0.08 },
  { feature: 'billing_risk_score', importance: 0.07 },
  { feature: 'early_lifecycle_risk', importance: 0.05 },
  { feature: 'total_charges', importance: 0.04 },
  { feature: 'service_penetration_rate', importance: 0.03 },
  { feature: 'has_premium_internet', importance: 0.02 },
  { feature: 'payment_reliability_score', importance: 0.02 }
];

export const confusionMatrix = {
  truePositive: 1028,
  falsePositive: 152,
  trueNegative: 456,
  falseNegative: 78
};

// Generate mock Telco customers for testing
export function generateMockUsers(count: number): UserPrediction[] {
  const users: UserPrediction[] = [];
  const contractTypes = ['monthly', 'yearly', 'biennial'];
  const paymentMethods = ['Electronic check', 'Bank transfer (automatic)', 'Credit card (automatic)', 'Mailed check'];
  const internetTypes = ['DSL', 'Fiber optic', 'No'];
  const baseDate = new Date('2024-11-10');

  for (let i = 0; i < count; i++) {
    // Generate customer ID in Telco format (e.g., 7590-VHVEG)
    const customerId = `${Math.floor(Math.random() * 9000) + 1000}-${Math.random().toString(36).substring(2, 7).toUpperCase()}`;
    
    // Generate realistic Telco feature values
    const tenureMonths = Math.floor(Math.random() * 73); // 0-72 months
    const monthlyCharges = Math.random() * 100 + 18.25; // $18.25-$118.25
    const totalCharges = monthlyCharges * tenureMonths * (0.8 + Math.random() * 0.4); // Some variation
    const totalServices = Math.floor(Math.random() * 10); // 0-9 services
    const isMonthlyContract = Math.random() > 0.45; // 55% month-to-month
    const contractType = isMonthlyContract ? 'monthly' : (Math.random() > 0.5 ? 'yearly' : 'biennial');
    const hasInternet = Math.random() > 0.1; // 90% have internet
    const internetType = hasInternet ? (Math.random() > 0.4 ? 'Fiber optic' : 'DSL') : 'No';
    const paymentMethod = paymentMethods[Math.floor(Math.random() * paymentMethods.length)];
    const billingRiskScore = (isMonthlyContract ? 0.3 : 0) + (paymentMethod === 'Electronic check' ? 0.5 : 0) + (Math.random() * 0.2);
    const serviceSatisfactionScore = (internetType === 'Fiber optic' ? 0.2 : 0.1) + (totalServices / 9) * 0.5 + Math.random() * 0.3;
    
    // Calculate churn probability based on Telco features
    let churnProbability = 0.3;
    if (isMonthlyContract) churnProbability += 0.25;
    if (tenureMonths < 12) churnProbability += 0.2;
    if (paymentMethod === 'Electronic check') churnProbability += 0.15;
    if (totalServices < 3) churnProbability += 0.1;
    if (billingRiskScore > 0.7) churnProbability += 0.1;
    churnProbability += (Math.random() - 0.5) * 0.15;
    churnProbability = Math.max(0.05, Math.min(0.95, churnProbability));
    
    // Determine risk level
    let riskLevel: RiskLevel;
    if (churnProbability >= 0.70) {
      riskLevel = 'HIGH';
    } else if (churnProbability >= 0.30) {
      riskLevel = 'MEDIUM';
    } else {
      riskLevel = 'LOW';
    }
    
    // Generate top driver for Telco
    let topDriver = 'Multiple factors';
    if (isMonthlyContract && paymentMethod === 'Electronic check') {
      topDriver = 'Month-to-month contract with electronic check';
    } else if (tenureMonths < 12 && monthlyCharges > 80) {
      topDriver = 'Low tenure with high monthly charges';
    } else if (totalServices < 3 && tenureMonths < 12) {
      topDriver = 'Few services and short tenure';
    } else if (billingRiskScore > 0.7) {
      topDriver = 'High billing risk profile';
    } else if (tenureMonths < 12 && isMonthlyContract) {
      topDriver = 'Early lifecycle risk (new customer, month-to-month)';
    }
    
    // Generate dates
    const daysSinceSignup = tenureMonths * 30;
    const signupDate = new Date(baseDate);
    signupDate.setDate(signupDate.getDate() - daysSinceSignup);
    const lastActive = new Date(baseDate);
    lastActive.setDate(lastActive.getDate() - Math.floor(Math.random() * 7)); // Active within last week
    
    users.push({
      customerId,
      userId: customerId, // For backward compatibility
      churnProbability,
      riskLevel,
      tenureMonths,
      daysInactive: Math.floor(Math.random() * 7), // For backward compatibility
      topDriver,
      contractType,
      subscriptionType: contractType as any, // For backward compatibility
      signupDate: signupDate.toISOString().split('T')[0],
      lastActive: lastActive.toISOString().split('T')[0],
      features: {
        tenure_months: tenureMonths,
        monthly_charges: monthlyCharges,
        total_charges: totalCharges,
        total_services: totalServices,
        is_monthly_contract: isMonthlyContract ? 1 : 0,
        has_internet: hasInternet ? 1 : 0,
        internet_type: internetType,
        payment_method: paymentMethod,
        billing_risk_score: billingRiskScore,
        service_satisfaction_score: serviceSatisfactionScore,
        // Backward compatibility
        days_since_last_session: Math.floor(Math.random() * 7),
        ramadan_engagement_ratio: 0,
        streak_current: 0,
        session_frequency_7d: 0,
        session_frequency_30d: 0,
        quran_reading_pct: 0,
        prayer_time_interaction_rate: 0,
      }
    });
  }
  
  return users;
}

// Generate trend data for Telco churn patterns
export function generateTrendData() {
  const data = [];
  const baseDate = new Date('2024-10-11'); // 30 days before base date
  
  for (let i = 0; i < 30; i++) {
    const date = new Date(baseDate);
    date.setDate(date.getDate() + i);
    
    // Simulate realistic Telco churn patterns
    const dayOfWeek = date.getDay();
    const baseHigh = 450;
    const baseMedium = 1200;
    const baseLow = 5700;
    
    // Add variation based on day of week (weekends might have different patterns)
    const dayVariation = dayOfWeek === 0 || dayOfWeek === 6 ? 30 : 0;
    const trendVariation = (Math.sin(i / 5) * 40) + (Math.random() * 80 - 40);
    
    data.push({
      date: date.toISOString().split('T')[0],
      highRisk: Math.max(200, Math.floor(baseHigh + trendVariation + dayVariation)),
      mediumRisk: Math.max(800, Math.floor(baseMedium + trendVariation * 1.5 + dayVariation)),
      lowRisk: Math.max(5000, Math.floor(baseLow + trendVariation * 2 + dayVariation))
    });
  }
  
  return data;
}
