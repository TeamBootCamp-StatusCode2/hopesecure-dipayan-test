import { useState, useEffect } from 'react';

interface GlobalStats {
  detection_rate: number;
  tests_conducted: number;
  enterprise_clients: number;
  total_campaigns: number;
  last_updated: string;
}

const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`;
  } else if (num >= 100000) {
    return `${Math.round(num / 1000)}K`;
  } else if (num >= 10000) {
    return `${(num / 1000).toFixed(0)}K`;
  } else if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
};

export const useGlobalStats = () => {
  const [stats, setStats] = useState<GlobalStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/global-stats/');
      if (!response.ok) {
        throw new Error('Failed to fetch global statistics');
      }
      const data = await response.json();
      setStats(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching global stats:', err);
      setError(err instanceof Error ? err.message : 'Failed to load statistics');
      // Set fallback data in case of error
      setStats({
        detection_rate: 98,
        tests_conducted: 50000,
        enterprise_clients: 500,
        total_campaigns: 1000,
        last_updated: new Date().toISOString(),
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    
    // Set up polling for real-time updates every 30 seconds
    const interval = setInterval(fetchStats, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const displayStats = stats ? {
    detectionRate: `${Math.round(stats.detection_rate)}%`,
    testsCount: `${formatNumber(stats.tests_conducted)}+`,
    clientsCount: `${formatNumber(stats.enterprise_clients)}+`,
    lastUpdated: stats.last_updated,
  } : null;

  return {
    stats: displayStats,
    loading,
    error,
    refresh: fetchStats,
  };
};
