import { Layout } from "@/components/Layout";
import { RiskBadge } from "@/components/RiskBadge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { generateMockUsers, RiskLevel } from "@/data/mockData";
import { Search, Filter, Download, ArrowUpDown } from "lucide-react";
import { useMemo, useState } from "react";
import { UserDetailModal } from "@/components/UserDetailModal";
import { exportToCSV } from "@/utils/exportUtils";
import { toast } from "sonner";

const Predictions = () => {
  const allUsers = useMemo(() => generateMockUsers(1000), []);
  const [searchQuery, setSearchQuery] = useState("");
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [subscriptionFilter, setSubscriptionFilter] = useState<string>("all");
  const [sortField, setSortField] = useState<'probability' | 'inactive' | 'userId' | 'tenure'>('probability');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [selectedUser, setSelectedUser] = useState<typeof allUsers[0] | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const filteredUsers = useMemo(() => {
    let filtered = allUsers.filter(user => {
      const customerId = (user.customerId || user.userId || '').toLowerCase();
      const matchesSearch = customerId.includes(searchQuery.toLowerCase());
      const matchesRisk = riskFilter === "all" || user.riskLevel === riskFilter;
      const contractType = (user.contractType || user.subscriptionType || '').toLowerCase();
      const matchesContract = subscriptionFilter === "all" || 
        (subscriptionFilter === "monthly" && contractType.includes("month")) ||
        (subscriptionFilter === "yearly" && contractType.includes("year")) ||
        (subscriptionFilter === "biennial" && contractType.includes("two")) ||
        contractType === subscriptionFilter;
      
      return matchesSearch && matchesRisk && matchesContract;
    });

    // Apply sorting
    filtered.sort((a, b) => {
      let aVal, bVal;
      
      if (sortField === 'probability') {
        aVal = a.churnProbability;
        bVal = b.churnProbability;
      } else if (sortField === 'inactive' || sortField === 'tenure') {
        aVal = a.tenureMonths || a.daysInactive || 0;
        bVal = b.tenureMonths || b.daysInactive || 0;
      } else {
        aVal = a.customerId || a.userId || '';
        bVal = b.customerId || b.userId || '';
        return sortDirection === 'asc' 
          ? String(aVal).localeCompare(String(bVal))
          : String(bVal).localeCompare(String(aVal));
      }
      
      return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
    });

    return filtered;
  }, [allUsers, searchQuery, riskFilter, subscriptionFilter, sortField, sortDirection]);

  const handleSort = (field: typeof sortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const handleExport = () => {
    exportToCSV(filteredUsers, 'filtered-predictions.csv');
      toast.success(`Exported ${filteredUsers.length} customers to CSV`);
  };

  const handleUserClick = (user: typeof allUsers[0]) => {
    setSelectedUser(user);
    setModalOpen(true);
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h2 className="text-3xl font-bold text-foreground">Customer Predictions</h2>
          <p className="text-muted-foreground mt-1">
            Browse and filter all customer churn predictions
          </p>
        </div>

        {/* Filters Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Filter className="h-5 w-5 text-primary" />
              <CardTitle>Filters</CardTitle>
            </div>
            <CardDescription>
              Refine the customer list based on your criteria
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Search Customer ID</label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="e.g., 7590-VHVEG"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Risk Level</label>
                <Select value={riskFilter} onValueChange={setRiskFilter}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Risk Levels</SelectItem>
                    <SelectItem value="HIGH">High Risk</SelectItem>
                    <SelectItem value="MEDIUM">Medium Risk</SelectItem>
                    <SelectItem value="LOW">Low Risk</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Contract Type</label>
                <Select value={subscriptionFilter} onValueChange={setSubscriptionFilter}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Contracts</SelectItem>
                    <SelectItem value="monthly">Month-to-month</SelectItem>
                    <SelectItem value="yearly">One year</SelectItem>
                    <SelectItem value="biennial">Two year</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="mt-4 flex items-center justify-between">
              <span className="text-sm text-muted-foreground">
                Showing {filteredUsers.length} of {allUsers.length} customers
              </span>
              <Button variant="outline" size="sm" className="gap-2" onClick={handleExport}>
                <Download className="h-4 w-4" />
                Export Filtered Results
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Users Table */}
        <Card>
          <CardHeader>
            <CardTitle>Customer List</CardTitle>
            <CardDescription>
              Click on any customer to view detailed predictions and explanations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th 
                      className="text-left py-3 px-4 text-sm font-medium text-muted-foreground cursor-pointer hover:text-foreground"
                      onClick={() => handleSort('userId')}
                    >
                      <div className="flex items-center gap-1">
                        Customer ID
                        <ArrowUpDown className="h-3 w-3" />
                      </div>
                    </th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Risk Level</th>
                    <th 
                      className="text-left py-3 px-4 text-sm font-medium text-muted-foreground cursor-pointer hover:text-foreground"
                      onClick={() => handleSort('probability')}
                    >
                      <div className="flex items-center gap-1">
                        Probability
                        <ArrowUpDown className="h-3 w-3" />
                      </div>
                    </th>
                    <th 
                      className="text-left py-3 px-4 text-sm font-medium text-muted-foreground cursor-pointer hover:text-foreground"
                      onClick={() => handleSort('inactive')}
                    >
                      <div className="flex items-center gap-1">
                        Tenure (Months)
                        <ArrowUpDown className="h-3 w-3" />
                      </div>
                    </th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Signup Date</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Contract Type</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Top Driver</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.slice(0, 50).map((user) => (
                    <tr 
                      key={user.customerId || user.userId} 
                      className="border-b hover:bg-muted/50 transition-colors cursor-pointer"
                      onClick={() => handleUserClick(user)}
                    >
                      <td className="py-3 px-4 text-sm font-mono">{user.customerId || user.userId}</td>
                      <td className="py-3 px-4">
                        <RiskBadge level={user.riskLevel} />
                      </td>
                      <td className="py-3 px-4 text-sm font-semibold">
                        {(user.churnProbability * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-4 text-sm">{user.tenureMonths || user.daysInactive || 0} months</td>
                      <td className="py-3 px-4 text-sm">{user.signupDate || user.lastActive}</td>
                      <td className="py-3 px-4">
                        <Badge variant="outline" className="capitalize">
                          {user.contractType || user.subscriptionType}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">
                        {user.topDriver}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {filteredUsers.length > 50 && (
              <div className="mt-4 text-center text-sm text-muted-foreground">
                Showing first 50 results. Use filters to narrow down the list.
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* User Detail Modal */}
      <UserDetailModal user={selectedUser} open={modalOpen} onOpenChange={setModalOpen} />
    </Layout>
  );
};

export default Predictions;
