import { UserPrediction } from "@/data/mockData.ts";

export const exportToCSV = (users: UserPrediction[], filename: string = 'churn-predictions.csv') => {
  // Define CSV headers
  const headers = [
    'User ID',
    'Risk Level',
    'Churn Probability',
    'Days Inactive',
    'Last Active',
    'Subscription Type',
    'Signup Date',
    'Top Driver',
    'Session Frequency (7d)',
    'Session Frequency (30d)',
    'Current Streak',
    'Ramadan Engagement Ratio',
    'Quran Reading %',
    'Prayer Time Interaction %'
  ];

  // Convert users to CSV rows
  const rows = users.map(user => [
    user.userId,
    user.riskLevel,
    (user.churnProbability * 100).toFixed(2),
    user.daysInactive,
    user.lastActive,
    user.subscriptionType,
    user.signupDate,
    user.topDriver,
    user.features.session_frequency_7d,
    user.features.session_frequency_30d,
    user.features.streak_current,
    user.features.ramadan_engagement_ratio.toFixed(2),
    (user.features.quran_reading_pct * 100).toFixed(2),
    (user.features.prayer_time_interaction_rate * 100).toFixed(2)
  ]);

  // Combine headers and rows
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n');

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

export const exportModelReport = () => {
  const reportContent = `
BARAKAH RETAIN - MODEL PERFORMANCE REPORT
Generated: ${new Date().toLocaleString()}

========================================
MODEL METRICS
========================================
Accuracy:     87.0%
Precision:    84.0%
Recall:       79.0%
F1 Score:     81.0%
ROC-AUC:      0.92

========================================
CONFUSION MATRIX
========================================
True Positives:   1,420 (Correctly predicted churners)
False Positives:    180 (False alarms)
True Negatives:   5,680 (Correctly predicted active users)
False Negatives:    320 (Missed churners)

========================================
TOP FEATURES (by importance)
========================================
1. Days Since Last Session        (18%)
2. Ramadan Engagement Ratio       (15%)
3. Session Frequency (7d)         (12%)
4. Current Streak                 (11%)
5. Quran Reading %                (9%)
6. Prayer Time Interaction        (8%)

========================================
KEY INSIGHTS
========================================
- 68% of Ramadan converts show high churn risk within 30 days
- Streak breaks increase churn probability by 45%
- Regular Quran readers have 20% lower churn rate
- Critical intervention window: Days 7-14 post-Ramadan

========================================
RECOMMENDATIONS
========================================
1. Launch retention campaigns at Day 7, 14, 21 post-Ramadan
2. Implement streak recovery notifications
3. Promote Quran reading features to low-engagement users
4. Send prayer time reminders to declining users
`;

  const blob = new Blob([reportContent], { type: 'text/plain;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', 'barakah-retain-report.txt');
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
