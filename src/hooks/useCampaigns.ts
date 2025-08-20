import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

export interface Campaign {
  id: number;
  name: string;
  status: string;
  created_at: string;
  emails_sent: number;
  links_clicked: number;
  credentials_submitted: number;
}

export const useCampaigns = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getCampaigns();
      // Ensure data is always an array
      const campaignsArray = Array.isArray(data) ? data : [];
      setCampaigns(campaignsArray);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch campaigns:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch campaigns');
      setCampaigns([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCampaigns();
  }, []);

  // Ensure campaigns is always an array before using array methods
  const campaignsArray = Array.isArray(campaigns) ? campaigns : [];
  
  const hasActiveCampaigns = campaignsArray.some(campaign => 
    campaign.status === 'active' || campaign.status === 'running'
  );

  const hasAnyCampaigns = campaignsArray.length > 0;

  return {
    campaigns,
    loading,
    error,
    hasActiveCampaigns,
    hasAnyCampaigns,
    refetch: fetchCampaigns
  };
};
