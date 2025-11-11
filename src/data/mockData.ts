// Mock data for Barakah Retain dashboard

export type RiskLevel = 'HIGH' | 'MEDIUM' | 'LOW';

export interface UserPrediction {
  userId: string;
  churnProbability: number;
  riskLevel: RiskLevel;
  daysInactive: number;
  lastActive: string;
  subscriptionType: 'free' | 'basic' | 'premium';
  signupDate: string;
  topDriver: string;
  features: {
    days_since_last_session: number;
    session_frequency_7d: number;
    session_frequency_30d: number;
    ramadan_engagement_ratio: number;
    streak_current: number;
    quran_reading_pct: number;
    prayer_time_interaction_rate: number;
  };
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  rocAuc: number;
}

export interface FeatureImportance {
  feature: string;
  importance: number;
  rank: number;
}

// Generate realistic user predictions
export const generateMockUsers = (count: number = 1000): UserPrediction[] => {
  const users: UserPrediction[] = [];
  const subscriptionTypes: ('free' | 'basic' | 'premium')[] = ['free', 'basic', 'premium'];
  
  const topDrivers = [
    'No activity for 15+ days',
    'Post-Ramadan drop-off',
    'Streak break',
    'Low Quran engagement',
    'No prayer time interaction',
    'Ramadan-only user pattern',
    'Low content diversity',
    'No social interaction'
  ];

  for (let i = 0; i < count; i++) {
    const churnProb = Math.random();
    let riskLevel: RiskLevel;
    
    if (churnProb > 0.7) riskLevel = 'HIGH';
    else if (churnProb > 0.3) riskLevel = 'MEDIUM';
    else riskLevel = 'LOW';

    const daysInactive = riskLevel === 'HIGH' 
      ? Math.floor(Math.random() * 20) + 10
      : riskLevel === 'MEDIUM'
      ? Math.floor(Math.random() * 10) + 3
      : Math.floor(Math.random() * 3);

    const lastActiveDate = new Date();
    lastActiveDate.setDate(lastActiveDate.getDate() - daysInactive);

    const signupDate = new Date();
    signupDate.setDate(signupDate.getDate() - Math.floor(Math.random() * 180) - 30);

    users.push({
      userId: `user-${String(i + 1).padStart(4, '0')}`,
      churnProbability: Math.round(churnProb * 100) / 100,
      riskLevel,
      daysInactive,
      lastActive: lastActiveDate.toISOString().split('T')[0],
      subscriptionType: subscriptionTypes[Math.floor(Math.random() * subscriptionTypes.length)],
      signupDate: signupDate.toISOString().split('T')[0],
      topDriver: topDrivers[Math.floor(Math.random() * topDrivers.length)],
      features: {
        days_since_last_session: daysInactive,
        session_frequency_7d: Math.max(0, Math.floor((1 - churnProb) * 15)),
        session_frequency_30d: Math.max(0, Math.floor((1 - churnProb) * 60)),
        ramadan_engagement_ratio: Math.random() * 5 + (riskLevel === 'HIGH' ? 3 : 0),
        streak_current: Math.max(0, Math.floor((1 - churnProb) * 30)),
        quran_reading_pct: Math.max(0, Math.random() * (1 - churnProb)),
        prayer_time_interaction_rate: Math.max(0, Math.random() * (1 - churnProb))
      }
    });
  }

  return users;
};

export const modelMetrics: ModelMetrics = {
  accuracy: 0.87,
  precision: 0.84,
  recall: 0.79,
  f1Score: 0.81,
  rocAuc: 0.92
};

export const featureImportance: FeatureImportance[] = [
  { feature: 'days_since_last_session', importance: 0.18, rank: 1 },
  { feature: 'ramadan_engagement_ratio', importance: 0.15, rank: 2 },
  { feature: 'session_frequency_7d', importance: 0.12, rank: 3 },
  { feature: 'streak_current', importance: 0.11, rank: 4 },
  { feature: 'quran_reading_pct', importance: 0.09, rank: 5 },
  { feature: 'prayer_time_interaction_rate', importance: 0.08, rank: 6 },
  { feature: 'session_frequency_30d', importance: 0.07, rank: 7 },
  { feature: 'last_10_nights_sessions', importance: 0.06, rank: 8 },
  { feature: 'jummah_participation_rate', importance: 0.05, rank: 9 },
  { feature: 'content_diversity_score', importance: 0.04, rank: 10 },
  { feature: 'lecture_watch_minutes', importance: 0.03, rank: 11 },
  { feature: 'friends_count', importance: 0.02, rank: 12 }
];

// Generate historical trend data (last 30 days)
export const generateTrendData = () => {
  const data = [];
  const today = new Date();
  
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    
    // Simulate post-Ramadan trend (higher risk in early days, declining)
    const baseRisk = 150;
    const trend = Math.max(50, baseRisk - i * 2);
    const variance = Math.random() * 20 - 10;
    
    data.push({
      date: date.toISOString().split('T')[0],
      highRisk: Math.floor(trend + variance),
      mediumRisk: Math.floor((trend + variance) * 1.5),
      lowRisk: Math.floor((trend + variance) * 2)
    });
  }
  
  return data;
};

export const confusionMatrix = {
  truePositive: 1420,
  falsePositive: 180,
  trueNegative: 5680,
  falseNegative: 320
};
