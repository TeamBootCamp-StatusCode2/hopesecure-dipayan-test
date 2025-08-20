import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { clearUserData } from '../lib/api';

interface LogoutButtonProps {
  className?: string;
  children?: React.ReactNode;
}

const LogoutButton: React.FC<LogoutButtonProps> = ({ className = '', children = 'Logout' }) => {
  const { logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
      
      // Additional cleanup to ensure complete user data isolation
      clearUserData();
      
      // Clear any remaining user-specific state
      window.location.href = '/signin';
    } catch (error) {
      console.error('Logout failed:', error);
      
      // Even if logout fails, clear local data and redirect
      clearUserData();
      window.location.href = '/signin';
    }
  };

  return (
    <button
      onClick={handleLogout}
      className={`text-red-600 hover:text-red-800 ${className}`}
    >
      {children}
    </button>
  );
};

export default LogoutButton;
