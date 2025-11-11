import { Layout } from "@/components/Layout";
import { RiskBadge } from "@/components/RiskBadge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { generateMockUsers, RiskLevel } from "@/data/mockData";
import { Search, Filter } from "lucide-react";
import { useMemo, useState } from "react";

const Predictions = () => {
  const allUsers = useMemo(() => generateMockUsers(1000), []);
  const [searchQuery, setSearchQuery] = useState("");
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [subscriptionFilter, setSubscriptionFilter] = useState<string>("all");

  const filteredUsers = useMemo(() => {
    return allUsers.filter(user => {
      const matchesSearch = user.userId.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesRisk = riskFilter === "all" || user.riskLevel === riskFilter;
      const matchesSubscription = subscriptionFilter === "all" || user.subscriptionType === subscriptionFilter;
      
      return matchesSearch && matchesRisk && matchesSubscription;
    });
  }, [allUsers, searchQuery, riskFilter, subscriptionFilter]);

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h2 className="text-3xl font-bold text-foreground">User Predictions</h2>
          <p className="text-muted-foreground mt-1">
            Browse and filter all user churn predictions
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
              Refine the user list based on your criteria
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Search User ID</label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="e.g., user-0001"
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
                <label className="text-sm font-medium text-foreground">Subscription</label>
                <Select value={subscriptionFilter} onValueChange={setSubscriptionFilter}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Subscriptions</SelectItem>
                    <SelectItem value="free">Free</SelectItem>
                    <SelectItem value="basic">Basic</SelectItem>
                    <SelectItem value="premium">Premium</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="mt-4 flex items-center gap-2">
              <span className="text-sm text-muted-foreground">
                Showing {filteredUsers.length} of {allUsers.length} users
              </span>
            </div>
          </CardContent>
        </Card>

        {/* Users Table */}
        <Card>
          <CardHeader>
            <CardTitle>User List</CardTitle>
            <CardDescription>
              Click on any user to view detailed predictions and explanations
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
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Last Active</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Subscription</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Top Driver</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.slice(0, 50).map((user) => (
                    <tr 
                      key={user.userId} 
                      className="border-b hover:bg-muted/50 transition-colors cursor-pointer"
                    >
                      <td className="py-3 px-4 text-sm font-mono">{user.userId}</td>
                      <td className="py-3 px-4">
                        <RiskBadge level={user.riskLevel} />
                      </td>
                      <td className="py-3 px-4 text-sm font-semibold">
                        {(user.churnProbability * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-4 text-sm">{user.daysInactive} days</td>
                      <td className="py-3 px-4 text-sm">{user.lastActive}</td>
                      <td className="py-3 px-4">
                        <Badge variant="outline" className="capitalize">
                          {user.subscriptionType}
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
    </Layout>
  );
};

export default Predictions;
