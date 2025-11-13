import { UserPrediction } from "@/services/dataLoader";

export const exportToCSV = (users: UserPrediction[], filename: string = 'churn-predictions.csv') => {
  // Define CSV headers
  const headers = [
    'Customer ID',
    'Risk Level',
    'Churn Probability',
    'Tenure (Months)',
    'Last Active',
    'Contract Type',
    'Signup Date',
    'Top Driver',
    'Monthly Charges',
    'Total Charges',
    'Total Services',
    'Billing Risk Score',
    'Service Satisfaction Score',
    'Payment Method'
  ];

  // Convert users to CSV rows
  const rows = users.map(user => [
    user.customerId || user.userId || 'N/A',
    user.riskLevel,
    (user.churnProbability * 100).toFixed(2),
    user.tenureMonths || user.features.tenure_months || 'N/A',
    user.lastActive,
    user.contractType || 'N/A',
    user.signupDate,
    user.topDriver,
    user.features.monthly_charges || 'N/A',
    user.features.total_charges || 'N/A',
    user.features.total_services || 'N/A',
    user.features.billing_risk_score || 'N/A',
    user.features.service_satisfaction_score || 'N/A',
    user.features.payment_method || 'N/A'
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
SPECSAILOR - TELCO CHURN PREDICTION MODEL REPORT
Generated: ${new Date().toLocaleString()}

========================================
MODEL METRICS
========================================
Accuracy:     82.7%
Precision:    69.2%
Recall:       54.1%
F1 Score:     60.7%
ROC-AUC:      0.85

========================================
CONFUSION MATRIX
========================================
True Positives:     389 (Correctly predicted churners)
False Positives:    173 (False alarms)
True Negatives:   1,174 (Correctly predicted retained customers)
False Negatives:    331 (Missed churners)

========================================
TOP FEATURES (by importance)
========================================
1. Tenure (Months)                (22%)
2. Month-to-month Contract        (18%)
3. Electronic Check Payment       (15%)
4. Monthly Charges                (12%)
5. Total Services                 (10%)
6. Billing Risk Score             (8%)

========================================
KEY INSIGHTS
========================================
- Month-to-month contracts show 3x higher churn risk
- Electronic check payment method correlates with higher churn
- Customers with tenure < 12 months have 60% churn rate
- Service penetration rate inversely correlates with churn

========================================
RECOMMENDATIONS
========================================
1. Incentivize annual/two-year contracts for high-risk customers
2. Promote autopay and alternative payment methods
3. Enhanced onboarding for first-year customers
4. Cross-sell additional services to increase engagement
`;

  const blob = new Blob([reportContent], { type: 'text/plain;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', 'specsailor-churn-report.txt');
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
