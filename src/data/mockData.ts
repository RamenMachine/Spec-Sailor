// Minimal mock data file for trend generation and types
// Main data now loaded from static JSON files

export type RiskLevel = 'HIGH' | 'MEDIUM' | 'LOW';

// Generate trend data for Telco churn patterns
export function generateTrendData() {
  const data = [];
  const baseDate = new Date('2024-10-11'); // 30 days before base date

  for (let i = 0; i < 30; i++) {
    const date = new Date(baseDate);
    date.setDate(date.getDate() + i);

    // Simulate realistic Telco churn patterns
    const dayOfWeek = date.getDay();
    const baseHigh = 450;
    const baseMedium = 1200;
    const baseLow = 5700;

    // Add variation based on day of week (weekends might have different patterns)
    const dayVariation = dayOfWeek === 0 || dayOfWeek === 6 ? 30 : 0;
    const trendVariation = (Math.sin(i / 5) * 40) + (Math.random() * 80 - 40);

    data.push({
      date: date.toISOString().split('T')[0],
      highRisk: Math.max(200, Math.floor(baseHigh + trendVariation + dayVariation)),
      mediumRisk: Math.max(800, Math.floor(baseMedium + trendVariation * 1.5 + dayVariation)),
      lowRisk: Math.max(5000, Math.floor(baseLow + trendVariation * 2 + dayVariation))
    });
  }

  return data;
}
