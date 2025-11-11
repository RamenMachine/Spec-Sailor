import { Layout } from "@/components/Layout";
import { MetricCard } from "@/components/MetricCard";
import { RiskBadge } from "@/components/RiskBadge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { generateMockUsers, generateTrendData } from "@/data/mockData";
import { Users, AlertTriangle, TrendingUp, Activity, Download, RefreshCw, Lightbulb } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useMemo } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();
  const users = useMemo(() => generateMockUsers(1000), []);
  const trendData = useMemo(() => generateTrendData(), []);

  const stats = useMemo(() => {
    const total = users.length;
    const high = users.filter(u => u.riskLevel === 'HIGH').length;
    const medium = users.filter(u => u.riskLevel === 'MEDIUM').length;
    const low = users.filter(u => u.riskLevel === 'LOW').length;

    return {
      total,
      high,
      highPct: Math.round((high / total) * 100),
      medium,
      mediumPct: Math.round((medium / total) * 100),
      low,
      lowPct: Math.round((low / total) * 100)
    };
  }, [users]);

  const topAtRiskUsers = useMemo(() => 
    users
      .filter(u => u.riskLevel === 'HIGH')
      .sort((a, b) => b.churnProbability - a.churnProbability)
      .slice(0, 10),
    [users]
  );

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h2 className="text-3xl font-bold text-foreground">Dashboard Overview</h2>
          <p className="text-muted-foreground mt-1">
            Monitor user retention and churn predictions in real-time
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Total Users"
            value={stats.total.toLocaleString()}
            subtitle="Active user base"
            icon={Users}
          />
          <MetricCard
            title="High Risk"
            value={stats.high.toLocaleString()}
            subtitle={`${stats.highPct}% of total users`}
            icon={AlertTriangle}
            variant="high"
            trend={{ value: -5, label: 'from yesterday' }}
          />
          <MetricCard
            title="Medium Risk"
            value={stats.medium.toLocaleString()}
            subtitle={`${stats.mediumPct}% of total users`}
            icon={TrendingUp}
            variant="medium"
            trend={{ value: 2, label: 'from yesterday' }}
          />
          <MetricCard
            title="Low Risk"
            value={stats.low.toLocaleString()}
            subtitle={`${stats.lowPct}% of total users`}
            icon={Activity}
            variant="low"
            trend={{ value: 3, label: 'from yesterday' }}
          />
        </div>

        {/* Churn Risk Trend Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Churn Risk Trend (Last 30 Days)</CardTitle>
            <CardDescription>
              Daily count of users by risk level - showing post-Ramadan patterns
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  dataKey="date" 
                  className="text-xs"
                  tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis className="text-xs" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="highRisk" 
                  stroke="hsl(var(--risk-high))" 
                  strokeWidth={2}
                  name="High Risk"
                  dot={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="mediumRisk" 
                  stroke="hsl(var(--risk-medium))" 
                  strokeWidth={2}
                  name="Medium Risk"
                  dot={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="lowRisk" 
                  stroke="hsl(var(--risk-low))" 
                  strokeWidth={2}
                  name="Low Risk"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Top 10 At-Risk Users */}
        <Card>
          <CardHeader>
            <CardTitle>Top 10 At-Risk Users</CardTitle>
            <CardDescription>
              Users with highest churn probability requiring immediate attention
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">User ID</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Risk Level</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Probability</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Days Inactive</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Top Driver</th>
                  </tr>
                </thead>
                <tbody>
                  {topAtRiskUsers.map((user) => (
                    <tr key={user.userId} className="border-b hover:bg-muted/50 transition-colors">
                      <td className="py-3 px-4 text-sm font-mono">{user.userId}</td>
                      <td className="py-3 px-4">
                        <RiskBadge level={user.riskLevel} />
                      </td>
                      <td className="py-3 px-4 text-sm font-semibold">{(user.churnProbability * 100).toFixed(1)}%</td>
                      <td className="py-3 px-4 text-sm">{user.daysInactive} days</td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">{user.topDriver}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3">
              <Button variant="outline" className="gap-2">
                <Download className="h-4 w-4" />
                Export All Predictions
              </Button>
              <Button variant="outline" className="gap-2">
                <RefreshCw className="h-4 w-4" />
                Refresh Data
              </Button>
              <Button 
                variant="default" 
                className="gap-2 bg-primary hover:bg-primary/90"
                onClick={() => navigate('/insights')}
              >
                <Lightbulb className="h-4 w-4" />
                View Insights
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
};

export default Home;
