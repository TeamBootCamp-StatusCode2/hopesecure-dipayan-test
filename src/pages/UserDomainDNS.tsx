import React from 'react';
import { ArrowLeft } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { useNavigate } from 'react-router-dom';
import DashboardHeader from '@/components/DashboardHeader';
import SuperAdminDomainManager from '@/components/SuperAdminDomainManager';

const UserDomainDNS: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <DashboardHeader />
      
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              onClick={() => navigate('/dashboard')}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Domain DNS Management</h1>
              <p className="text-gray-600">Manage email domains and DNS settings for phishing simulations</p>
            </div>
          </div>
        </div>
      </div>

      {/* Domain DNS Content */}
      <div className="container mx-auto px-6 py-8">
        <div className="bg-white rounded-lg shadow-lg">
          <SuperAdminDomainManager />
        </div>
      </div>
    </div>
  );
};

export default UserDomainDNS;
