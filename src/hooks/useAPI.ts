import { useQuery } from '@tanstack/react-query';
import { checkHealth } from '@/services/api';

export const useAPIHealth = () => {
  return useQuery({
    queryKey: ['api-health'],
    queryFn: checkHealth,
    refetchInterval: 30000, // Check every 30s
    retry: 3,
    staleTime: 10000, // Consider data stale after 10s
  });
};

export const usePredictions = () => {
  return useQuery({
    queryKey: ['predictions'],
    queryFn: async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/predictions`
      );
      if (!response.ok) throw new Error('API Error');
      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
};
