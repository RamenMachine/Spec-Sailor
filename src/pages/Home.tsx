import { Layout } from "@/components/Layout";
import { MetricCard } from "@/components/MetricCard";
import { RiskBadge } from "@/components/RiskBadge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { generateTrendData } from "@/data/mockData";
import { loadPredictions } from "@/services/dataLoader";
import { Users, AlertTriangle, TrendingUp, Activity, Download, RefreshCw, Lightbulb } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useMemo, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserDetailModal } from "@/components/UserDetailModal";
import { exportToCSV } from "@/utils/exportUtils";
import { toast } from "sonner";

interface ApiUser {
  user_id: string;
  churn_probability: number;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  daysInactive: number;
  topDriver: string;
}

const Home = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const trendData = useMemo(() => generateTrendData(), []);
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [modalOpen, setModalOpen] = useState(false);

  // Load predictions from static JSON
  useEffect(() => {
    const fetchData = async () => {
      try {
        const predictions = await loadPredictions();
        setUsers(predictions);
        toast.success(`Loaded ${predictions.length} customers successfully!`);
      } catch (error) {
        console.error('Failed to load predictions:', error);
        toast.error('Failed to load customer data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleExport = () => {
    const highRiskUsers = users.filter(u => u.riskLevel === 'HIGH');
    exportToCSV(highRiskUsers, 'high-risk-customers.csv');
      toast.success(`Exported ${highRiskUsers.length} high-risk customers to CSV`);
  };

  const handleRefresh = async () => {
    setIsLoading(true);
    try {
      const predictions = await loadPredictions();
      setUsers(predictions);
      toast.success('Data refreshed successfully!');
    } catch (error) {
      toast.error('Failed to refresh data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUserClick = (user: any) => {
    setSelectedUser(user);
    setModalOpen(true);
  };

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

  const [showAllUsers, setShowAllUsers] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [riskFilter, setRiskFilter] = useState<'ALL' | 'HIGH' | 'MEDIUM' | 'LOW'>('ALL');
  const usersPerPage = 50;

  const topAtRiskUsers = useMemo(() =>
    users
      .filter(u => u.riskLevel === 'HIGH')
      .sort((a, b) => b.churnProbability - a.churnProbability)
      .slice(0, 10),
    [users]
  );

  const filteredUsers = useMemo(() => {
    const filtered = riskFilter === 'ALL'
      ? users
      : users.filter(u => u.riskLevel === riskFilter);
    return filtered.sort((a, b) => b.churnProbability - a.churnProbability);
  }, [users, riskFilter]);

  const paginatedUsers = useMemo(() => {
    const startIndex = (currentPage - 1) * usersPerPage;
    const endIndex = startIndex + usersPerPage;
    return filteredUsers.slice(startIndex, endIndex);
  }, [filteredUsers, currentPage]);

  const totalPages = Math.ceil(filteredUsers.length / usersPerPage);

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h2 className="text-3xl font-bold text-foreground">Dashboard Overview</h2>
          <p className="text-muted-foreground mt-1">
            Monitor customer churn predictions and retention strategies in real-time
          </p>
        </div>

        {/* Loading State */}
        {isLoading && (
          <Card>
            <CardContent className="py-12">
              <div className="flex flex-col items-center justify-center space-y-4">
                <RefreshCw className="h-8 w-8 animate-spin text-primary" />
                <p className="text-muted-foreground">Loading customer data...</p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Metrics Grid */}
        {!isLoading && (
          <>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <MetricCard
                title="Total Customers"
                value={stats.total.toLocaleString()}
                subtitle="Active customer base"
                icon={Users}
              />
              <MetricCard
                title="High Risk"
                value={stats.high.toLocaleString()}
                subtitle={`${stats.highPct}% of total customers`}
                icon={AlertTriangle}
                variant="high"
                trend={{ value: -5, label: 'from yesterday' }}
              />
              <MetricCard
                title="Medium Risk"
                value={stats.medium.toLocaleString()}
                subtitle={`${stats.mediumPct}% of total customers`}
                icon={TrendingUp}
                variant="medium"
                trend={{ value: 2, label: 'from yesterday' }}
              />
              <MetricCard
                title="Low Risk"
                value={stats.low.toLocaleString()}
                subtitle={`${stats.lowPct}% of total customers`}
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
              Daily count of customers by risk level - showing churn patterns over time
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

        {/* All Users Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <CardTitle>
                  {showAllUsers
                    ? `All Customers (${filteredUsers.length}${riskFilter !== 'ALL' ? ` - ${riskFilter} Risk` : ''})`
                    : 'Top 10 At-Risk Customers'}
                </CardTitle>
                <CardDescription>
                  {showAllUsers
                    ? `Showing ${paginatedUsers.length} of ${filteredUsers.length} customers`
                    : 'Customers with highest churn probability requiring immediate attention'}
                </CardDescription>
              </div>
              <div className="flex gap-2 flex-wrap">
                {showAllUsers && (
                  <div className="flex gap-1">
                    <Button
                      variant={riskFilter === 'ALL' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => {
                        setRiskFilter('ALL');
                        setCurrentPage(1);
                      }}
                    >
                      All ({stats.total})
                    </Button>
                    <Button
                      variant={riskFilter === 'HIGH' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => {
                        setRiskFilter('HIGH');
                        setCurrentPage(1);
                      }}
                    >
                      High ({stats.high})
                    </Button>
                    <Button
                      variant={riskFilter === 'MEDIUM' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => {
                        setRiskFilter('MEDIUM');
                        setCurrentPage(1);
                      }}
                    >
                      Medium ({stats.medium})
                    </Button>
                    <Button
                      variant={riskFilter === 'LOW' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => {
                        setRiskFilter('LOW');
                        setCurrentPage(1);
                      }}
                    >
                      Low ({stats.low})
                    </Button>
                  </div>
                )}
                <Button
                  variant="outline"
                  onClick={() => {
                    setShowAllUsers(!showAllUsers);
                    setCurrentPage(1);
                    setRiskFilter('ALL');
                  }}
                >
                  {showAllUsers ? 'Show Top 10' : 'View All Customers'}
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Customer ID</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Risk Level</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Probability</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Tenure (Months)</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Top Driver</th>
                  </tr>
                </thead>
                <tbody>
                  {(showAllUsers ? paginatedUsers : topAtRiskUsers).map((user) => (
                    <tr
                      key={user.customerId || user.userId}
                      className="border-b hover:bg-muted/50 transition-colors cursor-pointer"
                      onClick={() => handleUserClick(user)}
                    >
                      <td className="py-3 px-4 text-sm font-mono">{user.customerId || user.userId}</td>
                      <td className="py-3 px-4">
                        <RiskBadge level={user.riskLevel} />
                      </td>
                      <td className="py-3 px-4 text-sm font-semibold">{(user.churnProbability * 100).toFixed(1)}%</td>
                      <td className="py-3 px-4 text-sm">{user.tenureMonths || user.daysInactive || 0} months</td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">{user.topDriver}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {showAllUsers && totalPages > 1 && (
              <div className="flex items-center justify-between mt-4 pt-4 border-t">
                <div className="text-sm text-muted-foreground">
                  Page {currentPage} of {totalPages}
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                  >
                    Next
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3">
              <Button variant="outline" className="gap-2" onClick={handleExport}>
                <Download className="h-4 w-4" />
                Export High Risk Customers
              </Button>
              <Button variant="outline" className="gap-2" onClick={handleRefresh}>
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
          </>
        )}
      </div>

      {/* User Detail Modal */}
      <UserDetailModal user={selectedUser} open={modalOpen} onOpenChange={setModalOpen} />
    </Layout>
  );
};

export default Home;
