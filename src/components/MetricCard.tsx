import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: {
    value: number;
    label: string;
  };
  variant?: 'default' | 'high' | 'medium' | 'low';
}

export const MetricCard = ({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  trend,
  variant = 'default'
}: MetricCardProps) => {
  const variantClasses = {
    default: 'border-border',
    high: 'border-risk-high bg-risk-high/5',
    medium: 'border-risk-medium bg-risk-medium/5',
    low: 'border-risk-low bg-risk-low/5'
  };

  const iconClasses = {
    default: 'text-primary bg-primary-light',
    high: 'text-risk-high bg-risk-high/10',
    medium: 'text-risk-medium bg-risk-medium/10',
    low: 'text-risk-low bg-risk-low/10'
  };

  return (
    <Card className={`${variantClasses[variant]}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <div className={`rounded-lg p-2 ${iconClasses[variant]}`}>
          <Icon className="h-4 w-4" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-foreground">{value}</div>
        {subtitle && (
          <p className="text-xs text-muted-foreground mt-1">
            {subtitle}
          </p>
        )}
        {trend && (
          <p className="text-xs text-muted-foreground mt-1">
            <span className={trend.value > 0 ? 'text-green-600' : 'text-red-600'}>
              {trend.value > 0 ? '+' : ''}{trend.value}%
            </span>{' '}
            {trend.label}
          </p>
        )}
      </CardContent>
    </Card>
  );
};
