import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface SuperAdminRouteProps {
  children: React.ReactNode;
}

const SuperAdminRoute: React.FC<SuperAdminRouteProps> = ({ children }) => {
  const { user, isAuthenticated, isLoading } = useAuth();

  console.log('🔍 SuperAdminRoute Debug:', {
    isAuthenticated,
    isLoading,
    user,
    is_superuser: user?.is_superuser
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    console.log('❌ Not authenticated, redirecting to signin');
    return <Navigate to="/signin" replace />;
  }

  // Check if user is super admin
  if (!user?.is_superuser) {
    console.log('❌ Not super admin, redirecting to dashboard');
    return <Navigate to="/dashboard" replace />;
  }

  console.log('✅ Super admin access granted');
  return <>{children}</>;
};

export default SuperAdminRoute;
