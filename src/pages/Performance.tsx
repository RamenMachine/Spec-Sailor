import { Layout } from "@/components/Layout";
import { MetricCard } from "@/components/MetricCard";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { modelMetrics, featureImportance, confusionMatrix } from "@/data/mockData.ts";
import { Target, TrendingUp, Activity, Award, Download } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { exportModelReport } from "@/utils/exportUtils";
import { toast } from "sonner";

const Performance = () => {
  const handleExportReport = () => {
    exportModelReport();
    toast.success('Model report exported successfully!');
  };

  // Prepare confusion matrix data for visualization
  const confusionData = [
    { name: 'True Positive', value: confusionMatrix.truePositive, color: 'hsl(var(--risk-low))' },
    { name: 'False Positive', value: confusionMatrix.falsePositive, color: 'hsl(var(--risk-medium))' },
    { name: 'True Negative', value: confusionMatrix.trueNegative, color: 'hsl(var(--risk-low))' },
    { name: 'False Negative', value: confusionMatrix.falseNegative, color: 'hsl(var(--risk-high))' }
  ];

  // Feature names mapping
  const featureNames: Record<string, string> = {
    'days_since_last_session': 'Days Since Last Session',
    'ramadan_engagement_ratio': 'Ramadan Engagement Ratio',
    'session_frequency_7d': 'Session Frequency (7d)',
    'streak_current': 'Current Streak',
    'quran_reading_pct': 'Quran Reading %',
    'prayer_time_interaction_rate': 'Prayer Time Interaction',
    'session_frequency_30d': 'Session Frequency (30d)',
    'last_10_nights_sessions': 'Last 10 Nights Sessions',
    'jummah_participation_rate': 'Jummah Participation',
    'content_diversity_score': 'Content Diversity',
    'lecture_watch_minutes': 'Lecture Watch Time',
    'friends_count': 'Friends Count'
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
            XGBoost model metrics and evaluation results
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Accuracy"
            value={`${(modelMetrics.accuracy * 100).toFixed(1)}%`}
            subtitle="Target: >85%"
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
            subtitle="Target: >75%"
            icon={Activity}
            variant="low"
          />
          <MetricCard
            title="ROC-AUC"
            value={modelMetrics.rocAuc.toFixed(2)}
            subtitle="Target: >0.90"
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
                  <h4 className="font-semibold text-sm text-primary mb-1">True Positives: {confusionMatrix.truePositive}</h4>
                  <p className="text-xs text-muted-foreground">Users correctly predicted as churners</p>
                </div>
                <div className="p-4 rounded-lg bg-risk-medium/10 border border-risk-medium/20">
                  <h4 className="font-semibold text-sm text-risk-medium mb-1">False Positives: {confusionMatrix.falsePositive}</h4>
                  <p className="text-xs text-muted-foreground">Active users incorrectly flagged as churners</p>
                </div>
                <div className="p-4 rounded-lg bg-primary-light border border-primary/20">
                  <h4 className="font-semibold text-sm text-primary mb-1">True Negatives: {confusionMatrix.trueNegative}</h4>
                  <p className="text-xs text-muted-foreground">Active users correctly predicted as staying</p>
                </div>
                <div className="p-4 rounded-lg bg-risk-high/10 border border-risk-high/20">
                  <h4 className="font-semibold text-sm text-risk-high mb-1">False Negatives: {confusionMatrix.falseNegative}</h4>
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
                <li>• <span className="font-medium text-foreground">Days Since Last Session</span> is the strongest predictor (18% importance)</li>
                <li>• <span className="font-medium text-foreground">Ramadan Engagement Ratio</span> reveals seasonal user patterns (15% importance)</li>
                <li>• <span className="font-medium text-foreground">Recent Activity Metrics</span> (7d frequency, streak) are critical for early detection</li>
                <li>• <span className="font-medium text-foreground">Islamic Content Engagement</span> (Quran, prayer times) correlates with retention</li>
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
                  <p className="text-base font-semibold">2,000 users (20%)</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground">Feature Count</h4>
                  <p className="text-base font-semibold">32 engineered features</p>
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
