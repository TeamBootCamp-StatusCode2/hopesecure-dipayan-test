import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Users, 
  Building2, 
  Shield, 
  Activity,
  Eye,
  Settings,
  BarChart3,
  AlertTriangle,
  Database,
  Monitor,
  Globe,
  Server,
  Mail
} from "lucide-react";
import { apiClient } from '@/lib/api';
import LogoutButton from '@/components/LogoutButton';
import AdminMonitoringDashboard from '@/components/AdminMonitoringDashboard';

interface SystemStats {
  total_organizations: number;
  total_users: number;
  total_employees: number;
  total_campaigns: number;
  total_templates: number;
  super_admins: number;
  org_admins: number;
  active_organizations: number;
  total_email_accounts?: number;
  total_domains?: number;
}

interface Organization {
  id: number;
  name: string;
  domain: string;
  industry: string;
  employee_count: string;
  admin_email: string;
  user_count: number;
  employee_count_actual: number;
  campaign_count: number;
  template_count: number;
  created_at: string;
}

const SuperAdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'organizations' | 'users' | 'system' | 'monitoring'>('overview');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch system statistics
        const statsResponse = await apiClient.getSystemStats();
        setStats(statsResponse);

        // Fetch all organizations
        const orgsResponse = await apiClient.getAllOrganizations();
        setOrganizations(orgsResponse.organizations);
      } catch (error) {
        console.error('Failed to fetch super admin data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-blue-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Loading Super Admin Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-blue-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Shield className="h-8 w-8 text-red-400" />
              <div>
                <h1 className="text-2xl font-bold text-white">Super Admin Dashboard</h1>
                <p className="text-gray-300 text-sm">System Management & Monitoring</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-gray-300 text-sm">System Administrator</span>
              <LogoutButton className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors" />
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Navigation Tabs */}
        <div className="flex space-x-1 mb-8 bg-black/20 rounded-lg p-1">
          {[
            { id: 'overview', label: 'Overview', icon: BarChart3 },
            { id: 'organizations', label: 'Organizations', icon: Building2 },
            { id: 'users', label: 'Users', icon: Users },
            { id: 'monitoring', label: 'Monitoring', icon: Monitor },
            { id: 'system', label: 'System', icon: Settings }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition-colors ${
                activeTab === tab.id 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-300 hover:bg-white/10'
              }`}
            >
              <tab.icon className="h-4 w-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && stats && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Total Organizations</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.total_organizations}</div>
                  <p className="text-xs text-gray-400">{stats.active_organizations} active</p>
                </CardContent>
              </Card>

              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Total Users</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.total_users}</div>
                  <p className="text-xs text-gray-400">{stats.org_admins} admins</p>
                </CardContent>
              </Card>

              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Total Campaigns</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.total_campaigns}</div>
                  <p className="text-xs text-gray-400">across all orgs</p>
                </CardContent>
              </Card>

              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Templates</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.total_templates}</div>
                  <p className="text-xs text-gray-400">available</p>
                </CardContent>
              </Card>
              
              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Email Accounts</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.total_email_accounts || 0}</div>
                  <p className="text-xs text-gray-400">configured</p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Organizations */}
            <Card className="bg-black/20 border-white/10 text-white">
              <CardHeader>
                <CardTitle>Recent Organizations</CardTitle>
                <CardDescription className="text-gray-400">Latest registered organizations</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {organizations.slice(0, 5).map((org) => (
                    <div key={org.id} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                      <div>
                        <h4 className="font-medium">{org.name || 'Unnamed Organization'}</h4>
                        <p className="text-sm text-gray-400">{org.admin_email}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm">{org.user_count} users</p>
                        <p className="text-xs text-gray-400">{org.campaign_count} campaigns</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Organizations Tab */}
        {activeTab === 'organizations' && (
          <div className="space-y-6">
            <Card className="bg-black/20 border-white/10 text-white">
              <CardHeader>
                <CardTitle>All Organizations</CardTitle>
                <CardDescription className="text-gray-400">Manage and monitor all registered organizations</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {organizations.map((org) => (
                    <div key={org.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold">{org.name || 'Unnamed Organization'}</h3>
                          <p className="text-gray-400">{org.domain || 'No domain set'}</p>
                          <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                            <div>
                              <span className="text-gray-400">Industry:</span>
                              <p>{org.industry}</p>
                            </div>
                            <div>
                              <span className="text-gray-400">Size:</span>
                              <p>{org.employee_count}</p>
                            </div>
                            <div>
                              <span className="text-gray-400">Users:</span>
                              <p>{org.user_count}</p>
                            </div>
                            <div>
                              <span className="text-gray-400">Campaigns:</span>
                              <p>{org.campaign_count}</p>
                            </div>
                          </div>
                          <div className="mt-2">
                            <span className="text-gray-400">Admin:</span>
                            <p>{org.admin_email}</p>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button 
                            size="sm" 
                            variant="outline" 
                            className="text-white border-white/20"
                            onClick={() => window.open(`/dashboard?org=${org.id}`, '_blank')}
                          >
                            <Globe className="h-4 w-4 mr-1" />
                            Manage Domains
                          </Button>
                          <Button size="sm" variant="outline" className="text-white border-white/20">
                            <Eye className="h-4 w-4 mr-1" />
                            View Details
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && stats && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader>
                  <CardTitle>User Roles</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span>Super Admins:</span>
                    <span className="font-bold text-red-400">{stats.super_admins}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Org Admins:</span>
                    <span className="font-bold text-blue-400">{stats.org_admins}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Total Users:</span>
                    <span className="font-bold">{stats.total_users}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader>
                  <CardTitle>Activity Overview</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span>Active Orgs:</span>
                    <span className="font-bold text-green-400">{stats.active_organizations}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Total Employees:</span>
                    <span className="font-bold">{stats.total_employees}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-black/20 border-white/10 text-white">
                <CardHeader>
                  <CardTitle>System Health</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2 text-green-400">
                    <Activity className="h-4 w-4" />
                    <span>System Operational</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* System Tab */}
        {activeTab === 'system' && (
          <div className="space-y-6">
            <Card className="bg-black/20 border-white/10 text-white">
              <CardHeader>
                <CardTitle>System Management</CardTitle>
                <CardDescription className="text-gray-400">Administrative tools and system controls</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <Button className="p-6 h-auto flex-col items-start bg-green-600/20 border-green-500/30 hover:bg-green-600/30">
                    <Users className="h-6 w-6 mb-2" />
                    <h3 className="font-semibold">User Management</h3>
                    <p className="text-sm text-gray-400 text-left">Manage users across all organizations</p>
                  </Button>
                  
                  <Button className="p-6 h-auto flex-col items-start bg-purple-600/20 border-purple-500/30 hover:bg-purple-600/30">
                    <Building2 className="h-6 w-6 mb-2" />
                    <h3 className="font-semibold">Organization Control</h3>
                    <p className="text-sm text-gray-400 text-left">Monitor and manage organizations</p>
                  </Button>
                  
                  <Button className="p-6 h-auto flex-col items-start bg-orange-600/20 border-orange-500/30 hover:bg-orange-600/30">
                    <BarChart3 className="h-6 w-6 mb-2" />
                    <h3 className="font-semibold">Analytics</h3>
                    <p className="text-sm text-gray-400 text-left">System-wide analytics and reports</p>
                  </Button>
                  
                  <Button className="p-6 h-auto flex-col items-start bg-red-600/20 border-red-500/30 hover:bg-red-600/30">
                    <AlertTriangle className="h-6 w-6 mb-2" />
                    <h3 className="font-semibold">Security Monitoring</h3>
                    <p className="text-sm text-gray-400 text-left">Monitor security across all organizations</p>
                  </Button>
                  
                  <Button className="p-6 h-auto flex-col items-start bg-teal-600/20 border-teal-500/30 hover:bg-teal-600/30">
                    <Server className="h-6 w-6 mb-2" />
                    <h3 className="font-semibold">System Health</h3>
                    <p className="text-sm text-gray-400 text-left">Monitor system status and performance</p>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Monitoring Tab */}
        {activeTab === 'monitoring' && (
          <div className="space-y-6">
            <AdminMonitoringDashboard />
          </div>
        )}
      </div>
    </div>
  );
};

export default SuperAdminDashboard;
