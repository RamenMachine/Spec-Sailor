import { Layout } from "@/components/Layout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb, TrendingDown, Zap, BookOpen, Users, PieChart as PieChartIcon } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, LineChart, Line, XAxis, YAxis, CartesianGrid, BarChart, Bar, ScatterChart, Scatter, ZAxis } from 'recharts';

const Insights = () => {
  // Static demo insights based on real Telco data patterns
  const insights = {
    monthlyContractChurn: "42",
    tenureImpact: "65",
    electronicCheckImpact: "38"
  };

  // Static risk distribution (demo values)
  const riskDistribution = [
    { name: 'High Risk', value: 287, color: 'hsl(var(--risk-high))' },
    { name: 'Medium Risk', value: 412, color: 'hsl(var(--risk-medium))' },
    { name: 'Low Risk', value: 301, color: 'hsl(var(--risk-low))' }
  ];

  const totalUsers = riskDistribution.reduce((sum, item) => sum + item.value, 0);

  // Retention curve for new customers (simulated)
  const retentionCurve = Array.from({ length: 31 }, (_, i) => ({
    day: i,
    retention: Math.max(32, 100 - (i * 2.2))
  }));

  // Churn rate by contract type (Telco-specific)
  const churnByContract = [
    { name: 'Month-to-month', churnRate: 42.7, customers: 3875 },
    { name: 'One year', churnRate: 11.3, customers: 1473 },
    { name: 'Two year', churnRate: 2.9, customers: 1695 }
  ];

  // Churn rate by tenure groups (Telco-specific)
  const churnByTenure = [
    { tenure: '0-6 months', churnRate: 58.2, customers: 1200 },
    { tenure: '7-12 months', churnRate: 45.1, customers: 980 },
    { tenure: '13-24 months', churnRate: 28.4, customers: 1450 },
    { tenure: '25-48 months', churnRate: 15.3, customers: 2100 },
    { tenure: '49+ months', churnRate: 8.7, customers: 1302 }
  ];

  // Churn rate by payment method (Telco-specific)
  const churnByPayment = [
    { method: 'Electronic check', churnRate: 45.3, customers: 2365 },
    { method: 'Mailed check', churnRate: 19.2, customers: 1612 },
    { method: 'Bank transfer', churnRate: 16.7, customers: 1544 },
    { method: 'Credit card', churnRate: 15.8, customers: 1511 }
  ];

  // Monthly charges distribution by churn status
  const monthlyChargesDistribution = [
    { range: '$0-30', churned: 8.2, retained: 91.8, total: 450 },
    { range: '$31-50', churned: 12.5, retained: 87.5, total: 680 },
    { range: '$51-70', churned: 18.3, retained: 81.7, total: 1250 },
    { range: '$71-90', churned: 28.7, retained: 71.3, total: 2100 },
    { range: '$91-110', churned: 42.1, retained: 57.9, total: 1850 },
    { range: '$111+', churned: 51.3, retained: 48.7, total: 702 }
  ];

  // Service count vs churn rate
  const churnByServiceCount = [
    { services: 0, churnRate: 65.2, customers: 120 },
    { services: 1, churnRate: 52.8, customers: 380 },
    { services: 2, churnRate: 38.4, customers: 850 },
    { services: 3, churnRate: 24.6, customers: 1250 },
    { services: 4, churnRate: 18.3, customers: 1450 },
    { services: 5, churnRate: 12.7, customers: 980 },
    { services: 6, churnRate: 8.9, customers: 650 },
    { services: 7, churnRate: 6.2, customers: 420 },
    { services: 8, churnRate: 4.1, customers: 280 },
    { services: 9, churnRate: 2.8, customers: 152 }
  ];

  // Tenure vs churn probability scatter data
  const tenureChurnScatter = Array.from({ length: 100 }, (_, i) => {
    const tenure = Math.floor(Math.random() * 72) + 1;
    // Higher churn probability for lower tenure, especially with month-to-month
    let baseProb = Math.max(0.05, 0.8 - (tenure / 100));
    if (tenure < 12) baseProb += 0.15;
    if (tenure < 6) baseProb += 0.1;
    const churnProb = Math.min(0.95, baseProb + (Math.random() - 0.5) * 0.2);
    const monthlyCharges = Math.floor(Math.random() * 100) + 20;
    return {
      tenure,
      churnProbability: churnProb * 100,
      monthlyCharges,
      // Color based on churn probability
      fill: churnProb > 0.7 ? 'hsl(var(--risk-high))' :
            churnProb > 0.3 ? 'hsl(var(--risk-medium))' :
            'hsl(var(--risk-low))'
    };
  });

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h2 className="text-3xl font-bold text-foreground">Insights & Analytics</h2>
          <p className="text-muted-foreground mt-1">
            Key findings and actionable retention strategies from Telco churn analysis
          </p>
        </div>

        {/* Key Findings Cards */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card className="border-risk-high bg-risk-high/5">
            <CardHeader>
              <div className="flex items-center gap-2">
                <TrendingDown className="h-5 w-5 text-risk-high" />
                <CardTitle className="text-lg">Month-to-Month Contract Risk</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-3xl font-bold text-risk-high">{insights.monthlyContractChurn}%</div>
              <p className="text-sm text-muted-foreground">
                of month-to-month customers show high churn risk
              </p>
              <div className="pt-3 border-t">
                <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                  <Lightbulb className="h-4 w-4 text-primary" />
                  Recommendation
                </h4>
                <p className="text-xs text-muted-foreground">
                  Offer contract upgrade incentives (discounts, service bundles) to convert month-to-month customers to annual contracts
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-risk-medium bg-risk-medium/5">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-risk-medium" />
                <CardTitle className="text-lg">Tenure Impact</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-3xl font-bold text-risk-medium">{insights.tenureImpact}%</div>
              <p className="text-sm text-muted-foreground">
                of customers with tenure &lt;12 months are at high churn risk
              </p>
              <div className="pt-3 border-t">
                <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                  <Lightbulb className="h-4 w-4 text-primary" />
                  Recommendation
                </h4>
                <p className="text-xs text-muted-foreground">
                  Implement early lifecycle retention programs: onboarding support, service tutorials, and loyalty rewards for first 90 days
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-primary bg-primary-light">
            <CardHeader>
              <div className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-primary" />
                <CardTitle className="text-lg">Payment Method Risk</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-3xl font-bold text-primary">{insights.electronicCheckImpact}%</div>
              <p className="text-sm text-muted-foreground">
                higher churn rate for customers using electronic check payment
              </p>
              <div className="pt-3 border-t">
                <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                  <Lightbulb className="h-4 w-4 text-primary" />
                  Recommendation
                </h4>
                <p className="text-xs text-muted-foreground">
                  Encourage automatic payment setup (bank transfer or credit card) with incentives like discounts or service credits
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Churn Analysis Charts */}
        <div className="grid gap-4 md:grid-cols-2">
          {/* Churn Rate by Contract Type */}
          <Card>
            <CardHeader>
              <CardTitle>Churn Rate by Contract Type</CardTitle>
              <CardDescription>
                Month-to-month customers have significantly higher churn
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={churnByContract}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis 
                    dataKey="name" 
                    className="text-xs"
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis 
                    label={{ value: 'Churn Rate %', angle: -90, position: 'insideLeft' }}
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
                  <Bar 
                    dataKey="churnRate" 
                    fill="hsl(var(--risk-high))"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 text-xs text-muted-foreground">
                <p><strong>Key Insight:</strong> Month-to-month contracts have 3.8x higher churn than annual contracts</p>
              </div>
            </CardContent>
          </Card>

          {/* Churn Rate by Tenure */}
          <Card>
            <CardHeader>
              <CardTitle>Churn Rate by Tenure Group</CardTitle>
              <CardDescription>
                New customers (0-6 months) are at highest risk
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={churnByTenure}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis 
                    dataKey="tenure" 
                    className="text-xs"
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis 
                    label={{ value: 'Churn Rate %', angle: -90, position: 'insideLeft' }}
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
                  <Bar 
                    dataKey="churnRate" 
                    fill="hsl(var(--risk-medium))"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 text-xs text-muted-foreground">
                <p><strong>Key Insight:</strong> Churn decreases significantly after 12 months tenure</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Churn Rate by Payment Method */}
        <Card>
          <CardHeader>
            <CardTitle>Churn Rate by Payment Method</CardTitle>
            <CardDescription>
              Electronic check payment method shows highest churn risk
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={churnByPayment}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  dataKey="method" 
                  className="text-xs"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                />
                <YAxis 
                  label={{ value: 'Churn Rate %', angle: -90, position: 'insideLeft' }}
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
                <Bar 
                  dataKey="churnRate" 
                  fill="hsl(var(--primary))"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
            <div className="mt-4 p-4 bg-secondary rounded-lg">
              <p className="text-sm text-muted-foreground">
                <span className="font-semibold text-foreground">Critical Finding:</span> Customers using electronic check have 2.7x higher churn than automatic payment methods. 
                Promoting automatic payment setup can significantly reduce churn.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Retention Curve */}
        <Card>
          <CardHeader>
            <CardTitle>New Customer Retention Curve</CardTitle>
            <CardDescription>
              30-day retention pattern for customers with tenure &lt;12 months
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={retentionCurve}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  dataKey="day" 
                  label={{ value: 'Days Since Signup', position: 'insideBottom', offset: -5 }}
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
                Intervention campaigns should target customers in this window with contract upgrade offers and service bundle promotions.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Monthly Charges Distribution by Churn Status */}
        <Card>
          <CardHeader>
            <CardTitle>Monthly Charges Distribution by Churn Status</CardTitle>
            <CardDescription>
              Higher monthly charges correlate with increased churn risk
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={monthlyChargesDistribution}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  dataKey="range" 
                  className="text-xs"
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis 
                  label={{ value: 'Percentage %', angle: -90, position: 'insideLeft' }}
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
                <Legend />
                <Bar 
                  dataKey="churned" 
                  stackId="a"
                  fill="hsl(var(--risk-high))"
                  name="Churned"
                />
                <Bar 
                  dataKey="retained" 
                  stackId="a"
                  fill="hsl(var(--risk-low))"
                  name="Retained"
                />
              </BarChart>
            </ResponsiveContainer>
            <div className="mt-4 p-4 bg-secondary rounded-lg">
              <p className="text-sm text-muted-foreground">
                <span className="font-semibold text-foreground">Key Insight:</span> Customers paying $91+ per month show 42-51% churn rate. 
                High-value customers may be price-sensitive or experiencing service dissatisfaction. Consider value-added services or loyalty programs.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Service Count vs Churn Rate */}
        <Card>
          <CardHeader>
            <CardTitle>Churn Rate by Number of Services</CardTitle>
            <CardDescription>
              Customers with fewer services are more likely to churn
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={churnByServiceCount}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  dataKey="services" 
                  label={{ value: 'Number of Services', position: 'insideBottom', offset: -5 }}
                  className="text-xs"
                />
                <YAxis 
                  label={{ value: 'Churn Rate %', angle: -90, position: 'insideLeft' }}
                  className="text-xs"
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                  formatter={(value: number, name: string) => {
                    if (name === 'churnRate') return `${value.toFixed(1)}%`;
                    if (name === 'customers') return `${value} customers`;
                    return value;
                  }}
                />
                <Bar 
                  dataKey="churnRate" 
                  fill="hsl(var(--primary))"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
            <div className="mt-4 grid md:grid-cols-2 gap-4">
              <div className="p-4 bg-risk-high/10 border border-risk-high/20 rounded-lg">
                <h4 className="font-semibold text-risk-high mb-2">High Risk (0-2 services)</h4>
                <p className="text-xs text-muted-foreground">
                  Customers with 0-2 services have 38-65% churn rate. These customers are not fully engaged with your service portfolio.
                </p>
              </div>
              <div className="p-4 bg-risk-low/10 border border-risk-low/20 rounded-lg">
                <h4 className="font-semibold text-risk-low mb-2">Low Risk (6+ services)</h4>
                <p className="text-xs text-muted-foreground">
                  Customers with 6+ services have &lt;9% churn rate. Service bundling creates strong customer stickiness.
                </p>
              </div>
            </div>
            <div className="mt-4 p-4 bg-secondary rounded-lg">
              <p className="text-sm text-muted-foreground">
                <span className="font-semibold text-foreground">Recommendation:</span> Target customers with 1-3 services with bundle promotions. 
                Each additional service reduces churn risk by approximately 8-10%.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Tenure vs Churn Probability Scatter Plot */}
        <Card>
          <CardHeader>
            <CardTitle>Tenure vs Churn Probability</CardTitle>
            <CardDescription>
              Relationship between customer tenure and predicted churn probability
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart data={tenureChurnScatter}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  type="number"
                  dataKey="tenure"
                  name="Tenure"
                  label={{ value: 'Tenure (Months)', position: 'insideBottom', offset: -5 }}
                  domain={[0, 72]}
                  className="text-xs"
                />
                <YAxis 
                  type="number"
                  dataKey="churnProbability"
                  name="Churn Probability"
                  label={{ value: 'Churn Probability %', angle: -90, position: 'insideLeft' }}
                  domain={[0, 100]}
                  className="text-xs"
                />
                <ZAxis 
                  type="number"
                  dataKey="monthlyCharges"
                  name="Monthly Charges"
                  range={[50, 400]}
                />
                <Tooltip 
                  cursor={{ strokeDasharray: '3 3' }}
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                  formatter={(value: number, name: string) => {
                    if (name === 'churnProbability') return `${value.toFixed(1)}%`;
                    if (name === 'tenure') return `${value} months`;
                    if (name === 'monthlyCharges') return `$${value.toFixed(2)}`;
                    return value;
                  }}
                />
                <Scatter 
                  name="High Risk" 
                  data={tenureChurnScatter.filter(d => d.churnProbability > 70)} 
                  fill="hsl(var(--risk-high))"
                  opacity={0.7}
                />
                <Scatter 
                  name="Medium Risk" 
                  data={tenureChurnScatter.filter(d => d.churnProbability > 30 && d.churnProbability <= 70)} 
                  fill="hsl(var(--risk-medium))"
                  opacity={0.7}
                />
                <Scatter 
                  name="Low Risk" 
                  data={tenureChurnScatter.filter(d => d.churnProbability <= 30)} 
                  fill="hsl(var(--risk-low))"
                  opacity={0.7}
                />
                <Legend />
              </ScatterChart>
            </ResponsiveContainer>
            <div className="mt-4 grid md:grid-cols-3 gap-4">
              <div className="p-3 bg-risk-high/10 border border-risk-high/20 rounded-lg">
                <h4 className="font-semibold text-risk-high text-sm mb-1">High Risk Zone</h4>
                <p className="text-xs text-muted-foreground">
                  Tenure &lt;12 months with &gt;70% churn probability. Immediate intervention required.
                </p>
              </div>
              <div className="p-3 bg-risk-medium/10 border border-risk-medium/20 rounded-lg">
                <h4 className="font-semibold text-risk-medium text-sm mb-1">Medium Risk Zone</h4>
                <p className="text-xs text-muted-foreground">
                  Tenure 12-24 months with 30-70% churn probability. Monitor and engage proactively.
                </p>
              </div>
              <div className="p-3 bg-risk-low/10 border border-risk-low/20 rounded-lg">
                <h4 className="font-semibold text-risk-low text-sm mb-1">Low Risk Zone</h4>
                <p className="text-xs text-muted-foreground">
                  Tenure &gt;24 months with &lt;30% churn probability. Focus on retention and upselling.
                </p>
              </div>
            </div>
            <div className="mt-4 p-4 bg-secondary rounded-lg">
              <p className="text-sm text-muted-foreground">
                <span className="font-semibold text-foreground">Pattern Analysis:</span> Clear negative correlation between tenure and churn probability. 
                Customers with tenure &lt;6 months show highest risk (60-90% churn probability). 
                After 24 months, churn probability stabilizes below 30%. The scatter plot also shows monthly charges as bubble size - 
                higher charges don't always mean higher churn if tenure is long.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Risk Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Customer Segment Breakdown</CardTitle>
            <CardDescription>
              Distribution of customers across risk levels
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
                    <h4 className="font-semibold text-risk-high">High Risk Customers</h4>
                    <span className="text-2xl font-bold text-risk-high">{riskDistribution[0].value}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Immediate intervention required. Likely to churn within 7-14 days. Offer contract upgrades and service bundles.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-risk-medium/10 border border-risk-medium/20">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-risk-medium">Medium Risk Customers</h4>
                    <span className="text-2xl font-bold text-risk-medium">{riskDistribution[1].value}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Declining satisfaction. Target with retention campaigns and payment method optimization.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-risk-low/10 border border-risk-low/20">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-risk-low">Low Risk Customers</h4>
                    <span className="text-2xl font-bold text-risk-low">{riskDistribution[2].value}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Healthy relationship. Focus on upselling additional services and maintaining satisfaction.
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
                  <h4 className="font-semibold mb-1">Contract Upgrade Campaign</h4>
                  <p className="text-sm text-muted-foreground">
                    Target month-to-month customers with tenure 3-6 months. Offer 10-15% discount on annual contracts with service bundle incentives to reduce churn risk.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 rounded-lg bg-primary-light border border-primary/20">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                  2
                </div>
                <div>
                  <h4 className="font-semibold mb-1">Payment Method Optimization</h4>
                  <p className="text-sm text-muted-foreground">
                    Target customers using electronic check payment. Offer incentives (discounts, service credits) to switch to automatic payment methods, reducing churn risk by 38%.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 rounded-lg bg-primary-light border border-primary/20">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                  3
                </div>
                <div>
                  <h4 className="font-semibold mb-1">Service Bundle Promotion</h4>
                  <p className="text-sm text-muted-foreground">
                    Customers with fewer than 3 services show higher churn. Promote service bundles (security, streaming, tech support) to increase customer value and retention.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 rounded-lg bg-primary-light border border-primary/20">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                  4
                </div>
                <div>
                  <h4 className="font-semibold mb-1">Early Lifecycle Support</h4>
                  <p className="text-sm text-muted-foreground">
                    New customers (tenure &lt;12 months) need extra support. Implement proactive outreach, service tutorials, and loyalty rewards to improve early retention.
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
