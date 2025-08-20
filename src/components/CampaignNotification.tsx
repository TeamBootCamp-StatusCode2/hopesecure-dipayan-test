import React from 'react';
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface CampaignNotificationProps {
  onClose: () => void;
}

const CampaignNotification: React.FC<CampaignNotificationProps> = ({ onClose }) => {
  const navigate = useNavigate();

  const handleCreateCampaign = () => {
    onClose();
    navigate('/campaign/create');
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md mx-4 shadow-lg">
        <Alert className="border-orange-200 bg-orange-50">
          <AlertTriangle className="h-4 w-4 text-orange-600" />
          <AlertDescription className="text-orange-800">
            <div className="space-y-4">
              <p className="font-semibold">No Active Campaigns Found</p>
              <p>
                You need to create and launch a campaign before accessing the Campaign Monitor. 
                Please create your first campaign to start monitoring phishing simulations.
              </p>
              <div className="flex gap-3 mt-4">
                <Button 
                  onClick={handleCreateCampaign}
                  className="bg-orange-600 hover:bg-orange-700 text-white"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Create Campaign
                </Button>
                <Button 
                  variant="outline" 
                  onClick={onClose}
                  className="border-orange-300 text-orange-700 hover:bg-orange-50"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </AlertDescription>
        </Alert>
      </div>
    </div>
  );
};

export default CampaignNotification;
