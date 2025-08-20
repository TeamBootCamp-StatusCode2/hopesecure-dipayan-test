import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Activity,
  AlertTriangle, 
  Shield, 
  Users, 
  TrendingUp,
  Clock,
  Globe,
  Database,
  Settings,
  Eye,
  RefreshCw,
  Filter,
  Download,
  Search
} from "lucide-react";
import { apiClient } from '@/lib/api';

interface ActivityLog {
  id: number;
  user: string;
  user_name: string;
  organization: string;
  action_type: string;
  action_display: string;
  description: string;
  severity: string;
  severity_display: string;
  ip_address: string;
  timestamp: string;
  metadata: any;
}

interface SystemAlert {
  id: number;
  alert_type: string;
  alert_type_display: string;
  title: string;
  description: string;
  severity: string;
  severity_display: string;
  status: string;
  status_display: string;
  organization: string;
  created_by: string;
  created_at: string;
  resolved_at?: string;
  resolved_by?: string;
}

interface DashboardOverview {
  activity_stats: {
    total_activities_24h: number;
    total_activities_7d: number;
    critical_activities_24h: number;
    login_attempts_24h: number;
    failed_logins_24h: number;
    security_events_24h: number;
  };
  alert_stats: {
    active_alerts: number;
    critical_alerts: number;
    security_alerts: number;
    new_alerts_24h: number;
  };
  critical_activities: Array<{
    action: string;
    description: string;
    severity: string;
    user: string;
    timestamp: string;
  }>;
  recent_alerts: Array<{
    title: string;
    severity: string;
    alert_type: string;
    created_at: string;
  }>;
  system_health: {
    overall_status: string;
    uptime_percentage: number;
    active_users_24h: number;
    active_organizations: number;
  };
}

const AdminMonitoringDashboard: React.FC = () => {
  const [overview, setOverview] = useState<DashboardOverview | null>(null);
  const [activityLogs, setActivityLogs] = useState<ActivityLog[]>([]);
  const [systemAlerts, setSystemAlerts] = useState<SystemAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      setRefreshing(true);
      const [overviewData, logsData, alertsData] = await Promise.all([
        apiClient.getAdminDashboardOverview(),
        apiClient.getActivityLogs({ days: 7, page_size: 20 }),
        apiClient.getSystemAlerts({ status: 'active', page_size: 10 })
      ]);

      setOverview(overviewData);
      setActivityLogs(logsData.logs || []);
      setSystemAlerts(alertsData.alerts || []);
    } catch (error) {
      console.error('Failed to fetch admin dashboard data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-white';
      case 'low': return 'bg-blue-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-500';
      case 'warning': return 'text-yellow-500';
      case 'critical': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const formatTimeAgo = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-blue-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Loading Admin Monitoring Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-blue-900 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <Shield className="h-8 w-8 text-red-400" />
          <div>
            <h1 className="text-3xl font-bold text-white">Admin Monitoring Dashboard</h1>
            <p className="text-gray-300">Real-time system monitoring and security oversight</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button 
            onClick={fetchData} 
            disabled={refreshing}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button variant="outline" className="text-white border-white/20">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* System Health Overview */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-black/30 border-white/10 text-white">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-300 flex items-center gap-2">
                <Activity className="h-4 w-4" />
                System Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${getStatusColor(overview.system_health.overall_status)}`}>
                {overview.system_health.overall_status.toUpperCase()}
              </div>
              <p className="text-xs text-gray-400">{overview.system_health.uptime_percentage}% uptime</p>
            </CardContent>
          </Card>

          <Card className="bg-black/30 border-white/10 text-white">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-300 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4" />
                Active Alerts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-400">
                {overview.alert_stats.active_alerts}
              </div>
              <p className="text-xs text-gray-400">
                {overview.alert_stats.critical_alerts} critical
              </p>
            </CardContent>
          </Card>

          <Card className="bg-black/30 border-white/10 text-white">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-300 flex items-center gap-2">
                <Shield className="h-4 w-4" />
                Security Events
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-400">
                {overview.activity_stats.security_events_24h}
              </div>
              <p className="text-xs text-gray-400">last 24 hours</p>
            </CardContent>
          </Card>

          <Card className="bg-black/30 border-white/10 text-white">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-300 flex items-center gap-2">
                <Users className="h-4 w-4" />
                Active Users
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-400">
                {overview.system_health.active_users_24h}
              </div>
              <p className="text-xs text-gray-400">last 24 hours</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-black/30 border-white/10">
          <TabsTrigger value="overview" className="data-[state=active]:bg-blue-600">
            Overview
          </TabsTrigger>
          <TabsTrigger value="logs" className="data-[state=active]:bg-blue-600">
            Activity Logs
          </TabsTrigger>
          <TabsTrigger value="alerts" className="data-[state=active]:bg-blue-600">
            System Alerts
          </TabsTrigger>
          <TabsTrigger value="analytics" className="data-[state=active]:bg-blue-600">
            Analytics
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Critical Activities */}
            <Card className="bg-black/30 border-white/10 text-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-red-400" />
                  Critical Activities
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Recent high-priority security events
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {overview?.critical_activities.map((activity, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-white/5 rounded-lg">
                    <Badge className={getSeverityColor(activity.severity)}>
                      {activity.severity}
                    </Badge>
                    <div className="flex-1">
                      <p className="font-medium">{activity.action}</p>
                      <p className="text-sm text-gray-400">{activity.description}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-gray-500">{activity.user}</span>
                        <span className="text-xs text-gray-500">•</span>
                        <span className="text-xs text-gray-500">
                          {formatTimeAgo(activity.timestamp)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Recent Alerts */}
            <Card className="bg-black/30 border-white/10 text-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-yellow-400" />
                  Recent Alerts
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Latest system alerts requiring attention
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {overview?.recent_alerts.map((alert, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-white/5 rounded-lg">
                    <Badge className={getSeverityColor(alert.severity)}>
                      {alert.severity}
                    </Badge>
                    <div className="flex-1">
                      <p className="font-medium">{alert.title}</p>
                      <p className="text-sm text-gray-400">{alert.alert_type}</p>
                      <span className="text-xs text-gray-500">
                        {formatTimeAgo(alert.created_at)}
                      </span>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Activity Statistics */}
          <Card className="bg-black/30 border-white/10 text-white">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-blue-400" />
                Activity Statistics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">
                    {overview?.activity_stats.total_activities_24h}
                  </div>
                  <p className="text-xs text-gray-400">Activities (24h)</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">
                    {overview?.activity_stats.login_attempts_24h}
                  </div>
                  <p className="text-xs text-gray-400">Login Attempts</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-400">
                    {overview?.activity_stats.failed_logins_24h}
                  </div>
                  <p className="text-xs text-gray-400">Failed Logins</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-400">
                    {overview?.activity_stats.security_events_24h}
                  </div>
                  <p className="text-xs text-gray-400">Security Events</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-400">
                    {overview?.activity_stats.critical_activities_24h}
                  </div>
                  <p className="text-xs text-gray-400">Critical Events</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-cyan-400">
                    {overview?.activity_stats.total_activities_7d}
                  </div>
                  <p className="text-xs text-gray-400">Weekly Total</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Activity Logs Tab */}
        <TabsContent value="logs" className="space-y-6">
          <Card className="bg-black/30 border-white/10 text-white">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Activity Logs
              </CardTitle>
              <CardDescription className="text-gray-400">
                Detailed system activity and user actions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {activityLogs.map((log) => (
                  <div key={log.id} className="flex items-start gap-3 p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                    <Badge className={getSeverityColor(log.severity)}>
                      {log.severity}
                    </Badge>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium">{log.action_display}</span>
                        <span className="text-sm text-gray-400">•</span>
                        <span className="text-sm text-gray-400">{log.user_name}</span>
                      </div>
                      <p className="text-sm text-gray-300">{log.description}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-gray-500">
                          <Globe className="h-3 w-3 inline mr-1" />
                          {log.ip_address}
                        </span>
                        <span className="text-xs text-gray-500">•</span>
                        <span className="text-xs text-gray-500">
                          <Clock className="h-3 w-3 inline mr-1" />
                          {formatTimeAgo(log.timestamp)}
                        </span>
                        <span className="text-xs text-gray-500">•</span>
                        <span className="text-xs text-gray-500">{log.organization}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* System Alerts Tab */}
        <TabsContent value="alerts" className="space-y-6">
          <Card className="bg-black/30 border-white/10 text-white">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                System Alerts
              </CardTitle>
              <CardDescription className="text-gray-400">
                Active security and system alerts
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {systemAlerts.map((alert) => (
                  <div key={alert.id} className="flex items-start gap-3 p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                    <Badge className={getSeverityColor(alert.severity)}>
                      {alert.severity}
                    </Badge>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium">{alert.title}</h4>
                        <Badge variant="outline" className="text-xs">
                          {alert.status_display}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-300 mb-2">{alert.description}</p>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-500">{alert.alert_type_display}</span>
                        <span className="text-xs text-gray-500">•</span>
                        <span className="text-xs text-gray-500">{alert.organization}</span>
                        <span className="text-xs text-gray-500">•</span>
                        <span className="text-xs text-gray-500">
                          {formatTimeAgo(alert.created_at)}
                        </span>
                      </div>
                    </div>
                    <Button size="sm" variant="outline" className="text-white border-white/20">
                      <Eye className="h-3 w-3 mr-1" />
                      View
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="bg-black/30 border-white/10 text-white">
              <CardHeader>
                <CardTitle>Security Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Failed Login Rate</span>
                    <Badge className="bg-red-500">
                      {overview?.activity_stats.failed_logins_24h || 0} today
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Security Events</span>
                    <Badge className="bg-orange-500">
                      {overview?.activity_stats.security_events_24h || 0} today
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Critical Alerts</span>
                    <Badge className="bg-red-600">
                      {overview?.alert_stats.critical_alerts || 0} active
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-black/30 border-white/10 text-white">
              <CardHeader>
                <CardTitle>System Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>System Uptime</span>
                    <Badge className="bg-green-500">
                      {overview?.system_health.uptime_percentage || 0}%
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Active Organizations</span>
                    <Badge className="bg-blue-500">
                      {overview?.system_health.active_organizations || 0}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Active Users (24h)</span>
                    <Badge className="bg-purple-500">
                      {overview?.system_health.active_users_24h || 0}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdminMonitoringDashboard;
