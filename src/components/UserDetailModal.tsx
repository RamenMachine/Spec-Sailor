import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { UserPrediction } from "@/data/mockData.ts";
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

  // Generate SHAP-like feature contributions
  const shapData = [
    { 
      feature: 'Days Inactive', 
      value: user.features.days_since_last_session > 7 ? 15 : -5,
      description: `${user.features.days_since_last_session} days since last session`
    },
    { 
      feature: 'Ramadan Pattern', 
      value: user.features.ramadan_engagement_ratio > 3 ? 12 : -8,
      description: `${user.features.ramadan_engagement_ratio.toFixed(1)}x engagement during Ramadan`
    },
    { 
      feature: 'Current Streak', 
      value: user.features.streak_current === 0 ? 10 : -10,
      description: `${user.features.streak_current} day streak`
    },
    { 
      feature: 'Weekly Activity', 
      value: user.features.session_frequency_7d < 5 ? 8 : -6,
      description: `${user.features.session_frequency_7d} sessions in last 7 days`
    },
    { 
      feature: 'Quran Reading', 
      value: user.features.quran_reading_pct < 0.3 ? 6 : -7,
      description: `${(user.features.quran_reading_pct * 100).toFixed(0)}% of sessions`
    },
    { 
      feature: 'Prayer Times', 
      value: user.features.prayer_time_interaction_rate < 0.5 ? 5 : -5,
      description: `${(user.features.prayer_time_interaction_rate * 100).toFixed(0)}% interaction rate`
    }
  ].sort((a, b) => Math.abs(b.value) - Math.abs(a.value));

  // Generate intervention recommendation
  const getIntervention = () => {
    if (user.riskLevel === 'HIGH') {
      return {
        title: 'Immediate Intervention Required',
        icon: AlertCircle,
        color: 'risk-high',
        actions: [
          'Send personalized push notification within 24 hours',
          'Offer premium feature trial for 7 days',
          'Recommend content based on past Ramadan activity',
          'Schedule follow-up check in 3 days'
        ],
        template: `As-salamu alaykum ${user.userId}! We noticed you haven't visited in ${user.daysInactive} days. We've prepared special content just for you - check out your personalized Quran reading plan! 📖✨`
      };
    } else if (user.riskLevel === 'MEDIUM') {
      return {
        title: 'Re-engagement Campaign',
        icon: TrendingDown,
        color: 'risk-medium',
        actions: [
          'Include in weekly content digest email',
          'Send Jummah reminder on Friday',
          'Highlight new features or content',
          'Monitor for 7 days'
        ],
        template: `Jummah Mubarak! 🕌 We have new content you might enjoy based on your interests. Take a moment to explore today! 🌟`
      };
    } else {
      return {
        title: 'Maintain Engagement',
        icon: CheckCircle,
        color: 'risk-low',
        actions: [
          'Continue regular content updates',
          'Send streak milestone congratulations',
          'Suggest advanced features',
          'Request feedback/rating'
        ],
        template: `MashAllah! 🌟 You're doing great! Keep up your ${user.features.streak_current}-day streak. Discover what's new this week! 📚`
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
            <span className="font-mono">{user.userId}</span>
            <RiskBadge level={user.riskLevel} />
          </DialogTitle>
          <DialogDescription>
            Detailed churn prediction analysis and intervention recommendations
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
                  {user.daysInactive}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Days Inactive</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-foreground capitalize">
                  {user.subscriptionType}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Subscription</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-foreground">
                  {user.features.streak_current}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Current Streak</p>
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

          {/* User Timeline */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">User Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-24 text-muted-foreground">Signup:</div>
                  <div className="font-medium">{user.signupDate}</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-24 text-muted-foreground">Last Active:</div>
                  <div className="font-medium">{user.lastActive}</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-24 text-muted-foreground">Sessions (7d):</div>
                  <div className="font-medium">{user.features.session_frequency_7d}</div>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-24 text-muted-foreground">Sessions (30d):</div>
                  <div className="font-medium">{user.features.session_frequency_30d}</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  );
};
