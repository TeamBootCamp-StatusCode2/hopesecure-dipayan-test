import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { 
  Plus, 
  BarChart3, 
  Users, 
  Shield, 
  Clock, 
  Target, 
  ChevronRight, 
  FileText, 
  Settings,
  Mail,
  Award,
  TrendingUp,
  Pencil,
  CheckCircle,
  Eye,
  Trash2,
  Home,
  RotateCcw,
  Square,
  Crown
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useCampaigns } from "@/hooks/useCampaigns";
import CampaignNotification from "@/components/CampaignNotification";
import { useAuth } from "@/contexts/AuthContext";

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [recentCampaigns, setRecentCampaigns] = useState([]);
  const [draftCampaigns, setDraftCampaigns] = useState([]);
  const [publishedCampaigns, setPublishedCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCampaignNotification, setShowCampaignNotification] = useState(false);
  const { campaigns, hasActiveCampaigns, hasAnyCampaigns, loading: campaignsLoading } = useCampaigns();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Set recent campaigns from the campaigns hook
        setRecentCampaigns(campaigns.slice(0, 3)); // Get most recent 3
        
        // Get campaigns from localStorage
        const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
        
        // Filter draft campaigns
        const drafts = storedCampaigns.filter(campaign => campaign.status === 'draft');
        setDraftCampaigns(drafts.slice(0, 3)); // Get most recent 3 drafts
        
        // Filter published campaigns (scheduled, active, completed)
        const published = storedCampaigns.filter(campaign => 
          campaign.status === 'scheduled' || 
          campaign.status === 'active' || 
          campaign.status === 'completed'
        );
        setPublishedCampaigns(published.slice(0, 3)); // Get most recent 3 published
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        setRecentCampaigns([]);
        setDraftCampaigns([]);
        setPublishedCampaigns([]);
      } finally {
        setLoading(false);
      }
    };

    if (!campaignsLoading) {
      fetchDashboardData();
    }
  }, [campaigns, campaignsLoading]);

  const handleCampaignMonitorClick = () => {
    // Check if user has any campaigns
    if (!hasAnyCampaigns) {
      setShowCampaignNotification(true);
      return;
    }
    
    // If campaigns exist, navigate to campaign monitor
    navigate('/campaign/execute');
  };

  const [stats, setStats] = useState([
    {
      title: "Total Campaigns",
      value: "0",
      change: "No data",
      icon: Target,
      color: "text-security-blue"
    },
    {
      title: "Employees Tested",
      value: "0",
      change: "No data", 
      icon: Users,
      color: "text-security-green"
    },
    {
      title: "Risk Score",
      value: "N/A",
      change: "No data",
      icon: Shield,
      color: "text-yellow-600"
    },
    {
      title: "Avg Click Rate",
      value: "0%",
      change: "No data",
      icon: BarChart3,
      color: "text-security-green"
    }
  ]);

  // Update stats when campaigns data changes
  useEffect(() => {
    if (!campaignsLoading && campaigns.length > 0) {
      const totalClicks = campaigns.reduce((sum, campaign) => sum + (campaign.links_clicked || 0), 0);
      const totalSent = campaigns.reduce((sum, campaign) => sum + (campaign.emails_sent || 0), 0);
      const totalSubmissions = campaigns.reduce((sum, campaign) => sum + (campaign.credentials_submitted || 0), 0);
      const clickRate = totalSent > 0 ? ((totalClicks / totalSent) * 100).toFixed(1) : "0";

      setStats([
        {
          title: "Total Campaigns",
          value: campaigns.length.toString(),
          change: hasActiveCampaigns ? "Active campaigns running" : "No active campaigns",
          icon: Target,
          color: "text-security-blue"
        },
        {
          title: "Employees Tested",
          value: totalSent.toString(),
          change: totalSent > 0 ? "Emails sent" : "No tests sent", 
          icon: Users,
          color: "text-security-green"
        },
        {
          title: "Risk Score",
          value: totalSubmissions > 0 ? "High" : "Low",
          change: `${totalSubmissions} submissions`,
          icon: Shield,
          color: totalSubmissions > 0 ? "text-red-600" : "text-green-600"
        },
        {
          title: "Avg Click Rate",
          value: `${clickRate}%`,
          change: totalClicks > 0 ? `${totalClicks} clicks` : "No clicks",
          icon: BarChart3,
          color: "text-security-green"
        }
      ]);
    }
  }, [campaigns, campaignsLoading, hasActiveCampaigns]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Active": return "bg-security-green";
      case "Completed": return "bg-security-blue";
      case "Scheduled": return "bg-yellow-500";
      default: return "bg-gray-500";
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-hero text-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">Security Campaign Dashboard</h1>
              <p className="text-gray-300">Monitor and manage your cybersecurity awareness campaigns</p>
            </div>
            <div className="flex gap-3">
              <Button 
                variant="outline" 
                size="lg" 
                className="w-fit bg-white/10 text-white border-white/20 hover:bg-white/20"
                onClick={() => navigate('/')}
              >
                <Home className="h-5 w-5 mr-2" />
                Home
              </Button>
              {user?.is_superuser && (
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="w-fit bg-yellow-500/20 text-yellow-100 border-yellow-400/30 hover:bg-yellow-500/30"
                  onClick={() => navigate('/superadmin')}
                >
                  <Crown className="h-5 w-5 mr-2" />
                  Super Admin Panel
                </Button>
              )}
              <Button 
                variant="accent" 
                size="lg" 
                className="w-fit"
                onClick={() => navigate('/campaign/create')}
              >
                <Plus className="h-5 w-5 mr-2" />
                New Campaign
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index} className="border border-border hover:shadow-card transition-smooth">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <stat.icon className={`h-8 w-8 ${stat.color}`} />
                  <Badge variant="secondary" className="text-xs">
                    {stat.change}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-1">{stat.title}</p>
                  <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Recent Campaigns */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-xl">Recent Campaigns</CardTitle>
                <CardDescription>Track the performance of your latest security tests</CardDescription>
              </div>
              <Button variant="outline" onClick={() => {
                if (recentCampaigns.length === 0) {
                  // No recent campaigns, redirect to create campaign
                  navigate('/campaign/create');
                } else {
                  // Has campaigns, go to campaigns list (or use existing route)
                  navigate('/campaigns');
                }
              }}>
                {recentCampaigns.length === 0 ? (
                  <>
                    <Plus className="h-4 w-4 mr-2" />
                    Create Campaign
                  </>
                ) : (
                  <>
                    View All
                    <ChevronRight className="h-4 w-4 ml-2" />
                  </>
                )}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {recentCampaigns.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p className="mb-4">No recent campaigns yet.</p>
                <Button onClick={() => navigate('/campaign/create')} className="bg-security-blue hover:bg-security-blue/90">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Your First Campaign
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {recentCampaigns.map((campaign) => (
                  <div key={campaign.id} className="border border-border rounded-lg p-4 hover:shadow-sm transition-smooth">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <h3 className="font-semibold text-foreground">{campaign.name}</h3>
                        <Badge className={`${getStatusColor(campaign.status)} text-white`}>
                          {campaign.status}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Clock className="h-4 w-4" />
                        {campaign.date}
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Targets</p>
                        <p className="font-semibold text-foreground">{campaign.targets}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Opened</p>
                        <p className="font-semibold text-security-blue">
                          {campaign.opened} ({campaign.targets > 0 ? Math.round((campaign.opened / campaign.targets) * 100) : 0}%)
                        </p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Clicked</p>
                        <p className="font-semibold text-yellow-600">
                          {campaign.clicked} ({campaign.targets > 0 ? Math.round((campaign.clicked / campaign.targets) * 100) : 0}%)
                        </p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Submitted</p>
                        <p className="font-semibold text-red-600">
                          {campaign.submitted} ({campaign.targets > 0 ? Math.round((campaign.submitted / campaign.targets) * 100) : 0}%)
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Draft Campaigns */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-orange-600" />
                  Draft Campaigns
                </CardTitle>
                <CardDescription>Manage your saved draft campaigns</CardDescription>
              </div>
              <Button variant="outline" size="sm" onClick={() => navigate('/campaign/create')}>
                <Plus className="h-4 w-4 mr-2" />
                New Draft
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {draftCampaigns.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No draft campaigns found</p>
                <p className="text-sm">Create a campaign and save as draft to see it here</p>
              </div>
            ) : (
              <div className="space-y-4">
                {draftCampaigns.map((campaign) => (
                  <div key={campaign.id} className="border border-border rounded-lg p-4 hover:shadow-sm transition-smooth">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <h3 className="font-semibold text-foreground">{campaign.name}</h3>
                        <Badge className="bg-orange-100 text-orange-800 border-orange-200">
                          Draft
                        </Badge>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => navigate('/campaign/create', { state: { editCampaign: campaign } })}
                        >
                          <Pencil className="h-4 w-4 mr-1" />
                          Edit
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            // Convert draft to active campaign
                            const updatedCampaign = { ...campaign, status: 'scheduled' };
                            const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
                            const updatedCampaigns = storedCampaigns.map(c => c.id === campaign.id ? updatedCampaign : c);
                            localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
                            setDraftCampaigns(prev => prev.filter(c => c.id !== campaign.id));
                            alert('Draft campaign launched successfully!');
                          }}
                        >
                          <Target className="h-4 w-4 mr-1" />
                          Launch
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            if (confirm('Are you sure you want to delete this draft campaign?')) {
                              // Delete draft campaign
                              const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
                              const updatedCampaigns = storedCampaigns.filter(c => c.id !== campaign.id);
                              localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
                              setDraftCampaigns(prev => prev.filter(c => c.id !== campaign.id));
                              alert('Draft campaign deleted successfully!');
                            }
                          }}
                          className="text-red-600 hover:text-red-700 hover:border-red-300"
                        >
                          <Trash2 className="h-4 w-4 mr-1" />
                          Delete
                        </Button>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Campaign Type</p>
                        <p className="font-semibold text-foreground">{campaign.campaign_type}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Target Emails</p>
                        <p className="font-semibold text-security-blue">{campaign.target_emails?.length || 0}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Created</p>
                        <p className="font-semibold text-muted-foreground">
                          {campaign.created_at ? new Date(campaign.created_at).toLocaleDateString() : 'Unknown'}
                        </p>
                      </div>
                    </div>
                    
                    {campaign.description && (
                      <div className="mt-3 pt-3 border-t">
                        <p className="text-sm text-muted-foreground">{campaign.description}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Published Campaigns */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  Published Campaigns
                </CardTitle>
                <CardDescription>Track your active and completed campaigns</CardDescription>
              </div>
              <Button variant="outline" size="sm" onClick={() => {
                if (publishedCampaigns.length === 0) {
                  // No published campaigns, redirect to create campaign
                  navigate('/campaign/create');
                } else {
                  // Has campaigns, go to campaign execution/monitoring
                  const firstCampaign = publishedCampaigns[0];
                  navigate('/campaign/execute', { state: { campaign: firstCampaign } });
                }
              }}>
                {publishedCampaigns.length === 0 ? (
                  <Plus className="h-4 w-4 mr-2" />
                ) : (
                  <Eye className="h-4 w-4 mr-2" />
                )}
                {publishedCampaigns.length === 0 ? 'Create Campaign' : 'View All'}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {publishedCampaigns.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <CheckCircle className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No published campaigns found</p>
                <p className="text-sm">Launch a campaign to see it here</p>
              </div>
            ) : (
              <div className="space-y-4">
                {publishedCampaigns.map((campaign) => (
                  <div key={campaign.id} className="border border-border rounded-lg p-4 hover:shadow-sm transition-smooth">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <h3 className="font-semibold text-foreground">{campaign.name}</h3>
                        <Badge className={`${
                          campaign.status === 'active' ? 'bg-green-100 text-green-800 border-green-200' :
                          campaign.status === 'scheduled' ? 'bg-blue-100 text-blue-800 border-blue-200' :
                          campaign.status === 'completed' ? 'bg-gray-100 text-gray-800 border-gray-200' :
                          'bg-orange-100 text-orange-800 border-orange-200'
                        }`}>
                          {campaign.status === 'active' ? 'Active' :
                           campaign.status === 'scheduled' ? 'Scheduled' :
                           campaign.status === 'completed' ? 'Completed' : campaign.status}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => navigate('/campaign/execute', { state: { campaign } })}
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          View
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => navigate('/campaign/create', { state: { editCampaign: campaign } })}
                        >
                          <Pencil className="h-4 w-4 mr-1" />
                          Edit
                        </Button>
                        {campaign.status === 'scheduled' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              // Start the campaign
                              const updatedCampaign = { ...campaign, status: 'active' };
                              const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
                              const updatedCampaigns = storedCampaigns.map(c => c.id === campaign.id ? updatedCampaign : c);
                              localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
                              setPublishedCampaigns(prev => prev.map(c => c.id === campaign.id ? updatedCampaign : c));
                              alert('Campaign started successfully!');
                            }}
                          >
                            <Target className="h-4 w-4 mr-1" />
                            Start
                          </Button>
                        )}
                        {campaign.status === 'active' && (
                          <>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                if (confirm('Are you sure you want to stop this campaign?')) {
                                  // Stop the campaign
                                  const updatedCampaign = { ...campaign, status: 'completed' };
                                  const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
                                  const updatedCampaigns = storedCampaigns.map(c => c.id === campaign.id ? updatedCampaign : c);
                                  localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
                                  setPublishedCampaigns(prev => prev.map(c => c.id === campaign.id ? updatedCampaign : c));
                                  alert('Campaign stopped successfully!');
                                }
                              }}
                              className="text-orange-600 hover:text-orange-700 hover:border-orange-300"
                            >
                              <Square className="h-4 w-4 mr-1" />
                              Stop
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                if (confirm('Are you sure you want to restart this campaign? This will reset its progress.')) {
                                  // Restart the campaign
                                  const updatedCampaign = { 
                                    ...campaign, 
                                    status: 'active',
                                    start_date: new Date().toISOString(),
                                    // Reset any progress metrics if needed
                                  };
                                  const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
                                  const updatedCampaigns = storedCampaigns.map(c => c.id === campaign.id ? updatedCampaign : c);
                                  localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
                                  setPublishedCampaigns(prev => prev.map(c => c.id === campaign.id ? updatedCampaign : c));
                                  alert('Campaign restarted successfully!');
                                }
                              }}
                              className="text-blue-600 hover:text-blue-700 hover:border-blue-300"
                            >
                              <RotateCcw className="h-4 w-4 mr-1" />
                              Restart
                            </Button>
                          </>
                        )}
                        {campaign.status === 'completed' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              if (confirm('Are you sure you want to restart this completed campaign?')) {
                                // Restart completed campaign
                                const updatedCampaign = { 
                                  ...campaign, 
                                  status: 'active',
                                  start_date: new Date().toISOString(),
                                  // Reset any progress metrics if needed
                                };
                                const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
                                const updatedCampaigns = storedCampaigns.map(c => c.id === campaign.id ? updatedCampaign : c);
                                localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
                                setPublishedCampaigns(prev => prev.map(c => c.id === campaign.id ? updatedCampaign : c));
                                alert('Campaign restarted successfully!');
                              }
                            }}
                            className="text-blue-600 hover:text-blue-700 hover:border-blue-300"
                          >
                            <RotateCcw className="h-4 w-4 mr-1" />
                            Restart
                          </Button>
                        )}
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            if (confirm('Are you sure you want to delete this campaign? This action cannot be undone.')) {
                              // Delete published campaign
                              const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
                              const updatedCampaigns = storedCampaigns.filter(c => c.id !== campaign.id);
                              localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
                              setPublishedCampaigns(prev => prev.filter(c => c.id !== campaign.id));
                              alert('Campaign deleted successfully!');
                            }
                          }}
                          className="text-red-600 hover:text-red-700 hover:border-red-300"
                        >
                          <Trash2 className="h-4 w-4 mr-1" />
                          Delete
                        </Button>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Campaign Type</p>
                        <p className="font-semibold text-foreground">{campaign.campaign_type}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Target Emails</p>
                        <p className="font-semibold text-security-blue">{campaign.target_emails?.length || 0}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Status</p>
                        <p className="font-semibold text-green-600">
                          {campaign.status === 'active' ? 'Running' :
                           campaign.status === 'scheduled' ? 'Pending' :
                           campaign.status === 'completed' ? 'Finished' : 'Unknown'}
                        </p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Schedule Date</p>
                        <p className="font-semibold text-muted-foreground">
                          {campaign.scheduled_date ? new Date(campaign.scheduled_date).toLocaleDateString() : 'Not set'}
                        </p>
                      </div>
                    </div>
                    
                    {campaign.description && (
                      <div className="mt-3 pt-3 border-t">
                        <p className="text-sm text-muted-foreground">{campaign.description}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <Card className="border border-border hover:shadow-card transition-smooth cursor-pointer" onClick={() => navigate('/campaign/create')}>
            <CardHeader className="text-center">
              <Plus className="h-12 w-12 text-security-blue mx-auto mb-4" />
              <CardTitle>Create Campaign</CardTitle>
              <CardDescription>Launch a new phishing simulation</CardDescription>
            </CardHeader>
          </Card>
          
          <Card className="border border-border hover:shadow-card transition-smooth cursor-pointer" onClick={() => navigate('/templates')}>
            <CardHeader className="text-center">
              <Mail className="h-12 w-12 text-purple-600 mx-auto mb-4" />
              <CardTitle>Template Management</CardTitle>
              <CardDescription>Create and manage email templates</CardDescription>
            </CardHeader>
          </Card>
          
          <Card className="border border-border hover:shadow-card transition-smooth cursor-pointer" onClick={() => navigate('/employees')}>
            <CardHeader className="text-center">
              <Users className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <CardTitle>Employee Management</CardTitle>
              <CardDescription>Manage employee profiles and training</CardDescription>
            </CardHeader>
          </Card>
          
          <Card className="border border-border hover:shadow-card transition-smooth cursor-pointer" onClick={() => navigate('/reports')}>
            <CardHeader className="text-center">
              <TrendingUp className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <CardTitle>Advanced Reports</CardTitle>
              <CardDescription>Comprehensive analytics and insights</CardDescription>
            </CardHeader>
          </Card>

          <Card className="border border-border hover:shadow-card transition-smooth cursor-pointer" onClick={handleCampaignMonitorClick}>
            <CardHeader className="text-center">
              <Target className="h-12 w-12 text-orange-600 mx-auto mb-4" />
              <CardTitle>Campaign Monitor</CardTitle>
              <CardDescription>Monitor live campaign execution</CardDescription>
            </CardHeader>
          </Card>

          <Card className="border border-border hover:shadow-card transition-smooth cursor-pointer" onClick={() => navigate('/settings')}>
            <CardHeader className="text-center">
              <Settings className="h-12 w-12 text-gray-600 mx-auto mb-4" />
              <CardTitle>Settings</CardTitle>
              <CardDescription>Configure platform settings</CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>

      {/* Campaign Notification Modal */}
      {showCampaignNotification && (
        <CampaignNotification onClose={() => setShowCampaignNotification(false)} />
      )}
    </div>
  );
};

export default Dashboard;