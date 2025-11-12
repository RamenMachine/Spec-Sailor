import { Layout } from "@/components/Layout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb, TrendingDown, Zap, BookOpen, Users, PieChart as PieChartIcon } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';

const Insights = () => {
  // Static demo insights based on real data patterns
  const insights = {
    ramadanChurnRate: "42",
    streakImpact: "45",
    quranImpact: "20"
  };

  // Static risk distribution (demo values)
  const riskDistribution = [
    { name: 'High Risk', value: 287, color: 'hsl(var(--risk-high))' },
    { name: 'Medium Risk', value: 412, color: 'hsl(var(--risk-medium))' },
    { name: 'Low Risk', value: 301, color: 'hsl(var(--risk-low))' }
  ];

  const totalUsers = riskDistribution.reduce((sum, item) => sum + item.value, 0);

  // Retention curve for Ramadan cohort (simulated)
  const retentionCurve = Array.from({ length: 31 }, (_, i) => ({
    day: i,
    retention: Math.max(32, 100 - (i * 2.2))
  }));

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h2 className="text-3xl font-bold text-foreground">Insights & Analytics</h2>
          <p className="text-muted-foreground mt-1">
            Key findings and actionable recommendations from churn analysis
          </p>
        </div>

        {/* Key Findings Cards */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card className="border-risk-high bg-risk-high/5">
            <CardHeader>
              <div className="flex items-center gap-2">
                <TrendingDown className="h-5 w-5 text-risk-high" />
                <CardTitle className="text-lg">Post-Ramadan Drop-off</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-3xl font-bold text-risk-high">{insights.ramadanChurnRate}%</div>
              <p className="text-sm text-muted-foreground">
                of Ramadan converts show high churn risk within 30 days
              </p>
              <div className="pt-3 border-t">
                <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                  <Lightbulb className="h-4 w-4 text-primary" />
                  Recommendation
                </h4>
                <p className="text-xs text-muted-foreground">
                  Launch targeted retention campaign at Day 7 post-Ramadan with personalized content reminders
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-risk-medium bg-risk-medium/5">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-risk-medium" />
                <CardTitle className="text-lg">Engagement Streak Impact</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-3xl font-bold text-risk-medium">+{insights.streakImpact}%</div>
              <p className="text-sm text-muted-foreground">
                increase in churn probability when streak breaks
              </p>
              <div className="pt-3 border-t">
                <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                  <Lightbulb className="h-4 w-4 text-primary" />
                  Recommendation
                </h4>
                <p className="text-xs text-muted-foreground">
                  Implement streak recovery notifications and grace periods to maintain engagement momentum
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-primary bg-primary-light">
            <CardHeader>
              <div className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-primary" />
                <CardTitle className="text-lg">Quran Reading Effect</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-3xl font-bold text-primary">{insights.quranImpact}%</div>
              <p className="text-sm text-muted-foreground">
                lower churn rate among regular Quran readers
              </p>
              <div className="pt-3 border-t">
                <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                  <Lightbulb className="h-4 w-4 text-primary" />
                  Recommendation
                </h4>
                <p className="text-xs text-muted-foreground">
                  Promote Quran reading features through onboarding and personalized content suggestions
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Retention Curve */}
        <Card>
          <CardHeader>
            <CardTitle>Ramadan Cohort Retention Curve</CardTitle>
            <CardDescription>
              30-day retention pattern for users who joined during Ramadan 2024
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={retentionCurve}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  dataKey="day" 
                  label={{ value: 'Days After Ramadan', position: 'insideBottom', offset: -5 }}
                  className="text-xs"
                />
                <YAxis 
                  label={{ value: 'Retention %', angle: -90, position: 'insideLeft' }}
                  className="text-xs"
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                  formatter={(value: number) => `${value.toFixed(1)}%`}
                />
                <Line 
                  type="monotone" 
                  dataKey="retention" 
                  stroke="hsl(var(--primary))" 
                  strokeWidth={3}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>

            <div className="mt-4 p-4 bg-secondary rounded-lg">
              <p className="text-sm text-muted-foreground">
                <span className="font-semibold text-foreground">Critical Window:</span> Days 7-14 show steepest decline. 
                Intervention campaigns should target users in this window with personalized re-engagement strategies.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Risk Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>User Segment Breakdown</CardTitle>
            <CardDescription>
              Distribution of users across risk levels
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={riskDistribution}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    label={(entry) => `${((entry.value / totalUsers) * 100).toFixed(1)}%`}
                  >
                    {riskDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>

              <div className="space-y-3">
                <div className="p-4 rounded-lg bg-risk-high/10 border border-risk-high/20">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-risk-high">High Risk Users</h4>
                    <span className="text-2xl font-bold text-risk-high">{riskDistribution[0].value}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Immediate intervention required. Likely to churn within 7-14 days.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-risk-medium/10 border border-risk-medium/20">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-risk-medium">Medium Risk Users</h4>
                    <span className="text-2xl font-bold text-risk-medium">{riskDistribution[1].value}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Declining engagement. Target with re-engagement campaigns.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-risk-low/10 border border-risk-low/20">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-risk-low">Low Risk Users</h4>
                    <span className="text-2xl font-bold text-risk-low">{riskDistribution[2].value}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Healthy engagement. Focus on retention and satisfaction.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Actionable Recommendations */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Users className="h-5 w-5 text-primary" />
              <CardTitle>Actionable Recommendations</CardTitle>
            </div>
            <CardDescription>
              Data-driven strategies to improve retention
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex gap-4 p-4 rounded-lg bg-primary-light border border-primary/20">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                  1
                </div>
                <div>
                  <h4 className="font-semibold mb-1">Post-Ramadan Retention Campaign</h4>
                  <p className="text-sm text-muted-foreground">
                    Launch automated campaigns at Day 7, 14, and 21 post-Ramadan targeting high-risk converts with personalized content based on their Ramadan activity patterns.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 rounded-lg bg-primary-light border border-primary/20">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                  2
                </div>
                <div>
                  <h4 className="font-semibold mb-1">Streak Recovery System</h4>
                  <p className="text-sm text-muted-foreground">
                    Implement grace periods and recovery notifications when streaks are at risk. Users with broken streaks show 45% higher churn probability.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 rounded-lg bg-primary-light border border-primary/20">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                  3
                </div>
                <div>
                  <h4 className="font-semibold mb-1">Content Personalization</h4>
                  <p className="text-sm text-muted-foreground">
                    Promote Quran reading features to low-engagement users. Regular Quran readers show 20% lower churn rates across all cohorts.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 rounded-lg bg-primary-light border border-primary/20">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                  4
                </div>
                <div>
                  <h4 className="font-semibold mb-1">Prayer Time Engagement</h4>
                  <p className="text-sm text-muted-foreground">
                    Send prayer time reminders to users with declining prayer time interaction rates. This feature strongly correlates with long-term retention.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
};

export default Insights;
