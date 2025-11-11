import { Badge } from "@/components/ui/badge";
import { RiskLevel } from "@/data/mockData";

interface RiskBadgeProps {
  level: RiskLevel;
  showIcon?: boolean;
}

export const RiskBadge = ({ level, showIcon = true }: RiskBadgeProps) => {
  const config = {
    HIGH: {
      label: 'High Risk',
      icon: '🔴',
      className: 'bg-risk-high text-risk-high-foreground hover:bg-risk-high/90'
    },
    MEDIUM: {
      label: 'Medium Risk',
      icon: '🟡',
      className: 'bg-risk-medium text-risk-medium-foreground hover:bg-risk-medium/90'
    },
    LOW: {
      label: 'Low Risk',
      icon: '🟢',
      className: 'bg-risk-low text-risk-low-foreground hover:bg-risk-low/90'
    }
  };

  const { label, icon, className } = config[level];

  return (
    <Badge className={className}>
      {showIcon && <span className="mr-1">{icon}</span>}
      {label}
    </Badge>
  );
};
