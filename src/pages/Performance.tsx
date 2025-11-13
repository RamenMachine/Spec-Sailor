import { Layout } from "@/components/Layout";
import { MetricCard } from "@/components/MetricCard";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { loadModelMetrics, loadFeatureImportance } from "@/services/dataLoader";
import { Target, TrendingUp, Activity, Award, Download } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { exportModelReport } from "@/utils/exportUtils";
import { toast } from "sonner";
import { useEffect, useState } from "react";

const Performance = () => {
  const [modelMetrics, setModelMetrics] = useState<any>(null);
  const [featureImportance, setFeatureImportance] = useState<any[]>([]);
  const [confusionMatrix, setConfusionMatrix] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metrics, importance] = await Promise.all([
          loadModelMetrics(),
          loadFeatureImportance()
        ]);
        setModelMetrics(metrics.metrics);
        setConfusionMatrix(metrics.confusion_matrix);
        setFeatureImportance(importance.features);
      } catch (error) {
        console.error('Failed to load model data:', error);
        toast.error('Failed to load model performance data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleExportReport = () => {
    exportModelReport();
    toast.success('Model report exported successfully!');
  };

  if (isLoading || !modelMetrics || !confusionMatrix) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[400px]">
          <p className="text-muted-foreground">Loading model performance data...</p>
        </div>
      </Layout>
    );
  }

  // Prepare confusion matrix data for visualization
  const confusionData = [
    { name: 'True Positive', value: confusionMatrix.true_positives, color: 'hsl(var(--risk-low))' },
    { name: 'False Positive', value: confusionMatrix.false_positives, color: 'hsl(var(--risk-medium))' },
    { name: 'True Negative', value: confusionMatrix.true_negatives, color: 'hsl(var(--risk-low))' },
    { name: 'False Negative', value: confusionMatrix.false_negatives, color: 'hsl(var(--risk-high))' }
  ];

  // Feature names mapping for Telco features
  const featureNames: Record<string, string> = {
    'tenure_months': 'Tenure (Months)',
    'contract_type_Month-to-month': 'Month-to-month Contract',
    'payment_method_Electronic check': 'Electronic Check Payment',
    'monthly_charges': 'Monthly Charges',
    'total_services': 'Total Services',
    'is_monthly_contract': 'Monthly Contract',
    'billing_risk_score': 'Billing Risk Score',
    'early_lifecycle_risk': 'Early Lifecycle Risk',
    'total_charges': 'Total Charges',
    'service_penetration_rate': 'Service Penetration Rate',
    'has_premium_internet': 'Premium Internet (Fiber)',
    'payment_reliability_score': 'Payment Reliability'
  };

  const featureChartData = featureImportance.map(f => ({
    name: featureNames[f.feature] || f.feature,
    importance: Math.round(f.importance * 100)
  }));

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h2 className="text-3xl font-bold text-foreground">Model Performance</h2>
          <p className="text-muted-foreground mt-1">
            XGBoost model metrics and evaluation results for Telco customer churn prediction
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Accuracy"
            value={`${(modelMetrics.accuracy * 100).toFixed(1)}%`}
            subtitle="Target: >80%"
            icon={Target}
            variant="low"
          />
          <MetricCard
            title="Precision"
            value={`${(modelMetrics.precision * 100).toFixed(1)}%`}
            subtitle="Target: >80%"
            icon={TrendingUp}
            variant="low"
          />
          <MetricCard
            title="Recall"
            value={`${(modelMetrics.recall * 100).toFixed(1)}%`}
            subtitle="Target: >70%"
            icon={Activity}
            variant="low"
          />
          <MetricCard
            title="ROC-AUC"
            value={modelMetrics.roc_auc.toFixed(2)}
            subtitle="Target: >0.85"
            icon={Award}
            variant="low"
          />
        </div>

        {/* Confusion Matrix */}
        <Card>
          <CardHeader>
            <CardTitle>Confusion Matrix</CardTitle>
            <CardDescription>
              Model prediction accuracy breakdown on test set
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={confusionData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label={(entry) => `${entry.name}: ${entry.value}`}
                    >
                      {confusionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="space-y-3">
                <div className="p-4 rounded-lg bg-primary-light border border-primary/20">
                  <h4 className="font-semibold text-sm text-primary mb-1">True Positives: {confusionMatrix.true_positives}</h4>
                  <p className="text-xs text-muted-foreground">Customers correctly predicted as churners</p>
                </div>
                <div className="p-4 rounded-lg bg-risk-medium/10 border border-risk-medium/20">
                  <h4 className="font-semibold text-sm text-risk-medium mb-1">False Positives: {confusionMatrix.false_positives}</h4>
                  <p className="text-xs text-muted-foreground">Active customers incorrectly flagged as churners</p>
                </div>
                <div className="p-4 rounded-lg bg-primary-light border border-primary/20">
                  <h4 className="font-semibold text-sm text-primary mb-1">True Negatives: {confusionMatrix.true_negatives}</h4>
                  <p className="text-xs text-muted-foreground">Active customers correctly predicted as staying</p>
                </div>
                <div className="p-4 rounded-lg bg-risk-high/10 border border-risk-high/20">
                  <h4 className="font-semibold text-sm text-risk-high mb-1">False Negatives: {confusionMatrix.false_negatives}</h4>
                  <p className="text-xs text-muted-foreground">Churners missed by the model</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Feature Importance */}
        <Card>
          <CardHeader>
            <CardTitle>Feature Importance</CardTitle>
            <CardDescription>
              Top 12 features driving churn predictions (based on SHAP values)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={featureChartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis type="number" className="text-xs" />
                <YAxis 
                  type="category" 
                  dataKey="name" 
                  width={200}
                  className="text-xs"
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                  formatter={(value) => `${value}% importance`}
                />
                <Bar dataKey="importance" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>

            <div className="mt-6 p-4 bg-secondary rounded-lg">
              <h4 className="font-semibold text-sm mb-2">Key Insights:</h4>
              <ul className="text-sm space-y-1 text-muted-foreground">
                <li>• <span className="font-medium text-foreground">Contract Type</span> is the strongest predictor - month-to-month customers churn more</li>
                <li>• <span className="font-medium text-foreground">Tenure</span> reveals lifecycle patterns - new customers are at higher risk</li>
                <li>• <span className="font-medium text-foreground">Payment Method</span> (electronic check) is a key churn indicator</li>
                <li>• <span className="font-medium text-foreground">Monthly Charges</span> and service bundle completeness correlate with retention</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Model Info */}
        <Card>
          <CardHeader>
            <CardTitle>Model Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground">Algorithm</h4>
                  <p className="text-base font-semibold">XGBoost (Gradient Boosting)</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground">Model Version</h4>
                  <p className="text-base font-semibold">v1.0.0</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground">Training Date</h4>
                  <p className="text-base font-semibold">November 10, 2024</p>
                </div>
              </div>
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground">Test Set Size</h4>
                  <p className="text-base font-semibold">1,407 customers (20%)</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground">Feature Count</h4>
                  <p className="text-base font-semibold">60+ engineered features</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground">Retraining Schedule</h4>
                  <p className="text-base font-semibold">Weekly (automated)</p>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-6 border-t">
              <Button onClick={handleExportReport} className="gap-2">
                <Download className="h-4 w-4" />
                Download Model Report
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
};

export default Performance;
