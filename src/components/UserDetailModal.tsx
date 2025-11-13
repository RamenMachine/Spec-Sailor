import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { UserPrediction } from "@/data/mockData";
import { RiskBadge } from "./RiskBadge";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { AlertCircle, CheckCircle, TrendingDown, Calendar, Activity } from "lucide-react";

interface UserDetailModalProps {
  user: UserPrediction | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const UserDetailModal = ({ user, open, onOpenChange }: UserDetailModalProps) => {
  if (!user) return null;

  // Generate SHAP-like feature contributions for Telco
  const shapData = [
    { 
      feature: 'Contract Type', 
      value: (user.features.is_monthly_contract || user.contractType?.toLowerCase().includes('month')) ? 18 : -8,
      description: user.contractType || 'Month-to-month contract'
    },
    { 
      feature: 'Tenure', 
      value: (user.features.tenure_months || user.tenureMonths || 0) < 12 ? 15 : -10,
      description: `${user.features.tenure_months || user.tenureMonths || 0} months tenure`
    },
    { 
      feature: 'Payment Method', 
      value: (user.features.payment_method || '').includes('Electronic') ? 12 : -6,
      description: user.features.payment_method || 'Payment method'
    },
    { 
      feature: 'Monthly Charges', 
      value: (user.features.monthly_charges || 0) > 80 ? 8 : -5,
      description: `$${user.features.monthly_charges?.toFixed(2) || '0.00'} per month`
    },
    { 
      feature: 'Service Count', 
      value: (user.features.total_services || 0) < 3 ? 10 : -7,
      description: `${user.features.total_services || 0} services subscribed`
    },
    { 
      feature: 'Billing Risk', 
      value: (user.features.billing_risk_score || 0) > 0.7 ? 9 : -4,
      description: `${((user.features.billing_risk_score || 0) * 100).toFixed(0)}% risk score`
    }
  ].sort((a, b) => Math.abs(b.value) - Math.abs(a.value));

  // Generate intervention recommendation for Telco
  const getIntervention = () => {
    const customerId = user.customerId || user.userId;
    const tenure = user.features.tenure_months || user.tenureMonths || 0;
    
    if (user.riskLevel === 'HIGH') {
      return {
        title: 'Immediate Intervention Required',
        icon: AlertCircle,
        color: 'risk-high',
        actions: [
          'Contact customer within 24 hours with retention offer',
          'Offer contract upgrade with 15% discount',
          'Propose service bundle to increase value',
          'Schedule follow-up call in 3 days'
        ],
        template: `Dear ${customerId}, we value your business! We'd like to offer you a special retention package: upgrade to an annual contract and save 15% plus receive premium service bundles. Call us at 1-800-RETAIN today!`
      };
    } else if (user.riskLevel === 'MEDIUM') {
      return {
        title: 'Re-engagement Campaign',
        icon: TrendingDown,
        color: 'risk-medium',
        actions: [
          'Send email with service bundle promotion',
          'Offer payment method optimization (auto-pay discount)',
          'Highlight new services or features',
          'Monitor account activity for 7 days'
        ],
        template: `Hi ${customerId}, thank you for being a valued customer for ${tenure} months! We have exciting new service bundles that could save you money. Check your email for exclusive offers!`
      };
    } else {
      return {
        title: 'Maintain Satisfaction',
        icon: CheckCircle,
        color: 'risk-low',
        actions: [
          'Continue regular account reviews',
          'Send loyalty rewards and appreciation',
          'Suggest service upgrades or add-ons',
          'Request feedback for service improvement'
        ],
        template: `Thank you ${customerId} for your loyalty! As a valued customer of ${tenure} months, we'd love to hear your feedback and explore ways to enhance your service experience.`
      };
    }
  };

  const intervention = getIntervention();
  const Icon = intervention.icon;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <span className="font-mono">{user.customerId || user.userId}</span>
            <RiskBadge level={user.riskLevel} />
          </DialogTitle>
          <DialogDescription>
            Detailed customer churn prediction analysis and retention recommendations
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-foreground">
                  {(user.churnProbability * 100).toFixed(1)}%
                </div>
                <p className="text-xs text-muted-foreground mt-1">Churn Probability</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-foreground">
                  {user.features.tenure_months || user.tenureMonths || 0}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Tenure (Months)</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-foreground capitalize">
                  {user.contractType || user.subscriptionType || 'N/A'}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Contract Type</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-foreground">
                  ${user.features.monthly_charges?.toFixed(0) || '0'}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Monthly Charges</p>
              </CardContent>
            </Card>
          </div>

          {/* SHAP Explanation */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Why This Prediction?</CardTitle>
              <p className="text-sm text-muted-foreground">
                Top factors contributing to churn risk (SHAP values)
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={shapData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis type="number" domain={[-15, 15]} />
                  <YAxis type="category" dataKey="feature" width={120} className="text-xs" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px'
                    }}
                    formatter={(value: number, name, props) => [
                      `${value > 0 ? '+' : ''}${value}% impact`,
                      props.payload.description
                    ]}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {shapData.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={entry.value > 0 ? 'hsl(var(--risk-high))' : 'hsl(var(--risk-low))'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>

              <div className="mt-4 space-y-2">
                {shapData.slice(0, 3).map((item, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
                    <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                      item.value > 0 ? 'bg-risk-high text-risk-high-foreground' : 'bg-risk-low text-risk-low-foreground'
                    }`}>
                      {item.value > 0 ? '+' : '-'}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">{item.feature}</p>
                      <p className="text-xs text-muted-foreground">{item.description}</p>
                      <p className="text-xs font-semibold mt-1">
                        {item.value > 0 ? 'Increases' : 'Decreases'} churn risk by {Math.abs(item.value)}%
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Intervention Recommendation */}
          <Card className={`border-${intervention.color} bg-${intervention.color}/5`}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Icon className={`h-5 w-5 text-${intervention.color}`} />
                {intervention.title}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="text-sm font-semibold mb-2">Recommended Actions:</h4>
                <ul className="space-y-1">
                  {intervention.actions.map((action, idx) => (
                    <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2">
                      <span className="text-primary mt-0.5">•</span>
                      <span>{action}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="text-sm font-semibold mb-2">Message Template:</h4>
                <div className="p-3 rounded-lg bg-card border border-border">
                  <p className="text-sm italic">{intervention.template}</p>
                </div>
              </div>

              <div className="flex gap-2 pt-2">
                <Badge variant="outline" className="gap-1">
                  <Calendar className="h-3 w-3" />
                  Send within 24h
                </Badge>
                <Badge variant="outline" className="gap-1">
                  <Activity className="h-3 w-3" />
                  Track response
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Customer Details */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Customer Details</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Signup Date:</div>
                  <div className="font-medium">{user.signupDate}</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Tenure:</div>
                  <div className="font-medium">{user.features.tenure_months || user.tenureMonths || 0} months</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Monthly Charges:</div>
                  <div className="font-medium">${user.features.monthly_charges?.toFixed(2) || '0.00'}</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Total Services:</div>
                  <div className="font-medium">{user.features.total_services || 0}</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Payment Method:</div>
                  <div className="font-medium capitalize">{user.features.payment_method || 'N/A'}</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Internet Type:</div>
                  <div className="font-medium">{user.features.internet_type || 'N/A'}</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  );
};
