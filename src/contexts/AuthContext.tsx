import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { apiClient, User, setUserData, clearUserData } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
}

interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  role?: string;
  department?: string;
  phone_number?: string;
  // Company information
  company_name: string;
  company_domain?: string;
  company_industry?: string;
  company_employee_count?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = apiClient.getToken();
      if (token) {
        try {
          const userData = await apiClient.getProfile();
          setUser(userData);
          setUserData(userData);
        } catch (error) {
          console.error('Failed to get user profile:', error);
          // Clear invalid token
          apiClient.clearToken();
          clearUserData();
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string): Promise<void> => {
    try {
      const response = await apiClient.login(email, password);
      console.log('🔍 Login Response:', response);
      console.log('🔍 User is_superuser:', response.user.is_superuser);
      console.log('🔍 Redirect URL:', response.redirect_url);
      
      setUser(response.user);
      setUserData(response.user);
      
      // Redirect based on user role
      if (response.redirect_url) {
        console.log('🚀 Redirecting to:', response.redirect_url);
        window.location.href = response.redirect_url;
      } else {
        // Fallback logic
        const redirectUrl = response.user.is_superuser ? '/superadmin' : '/dashboard';
        console.log('🚀 Fallback redirect to:', redirectUrl);
        window.location.href = redirectUrl;
      }
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (userData: RegisterData): Promise<void> => {
    try {
      const response = await apiClient.register(userData);
      setUser(response.user);
      setUserData(response.user);
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await apiClient.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      clearUserData();
    }
  };

  const updateUser = (userData: Partial<User>): void => {
    if (user) {
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      setUserData(updatedUser);
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
