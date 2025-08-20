import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  ArrowLeft, 
  Play, 
  Pause, 
  StopCircle, 
  Users, 
  Mail, 
  MousePointer, 
  Download, 
  Shield, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Eye,
  Target,
  TrendingUp,
  FileText
} from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

const CampaignExecution = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [campaignStatus, setCampaignStatus] = useState<'ready' | 'launching' | 'active' | 'paused' | 'completed'>('ready');
  const [progress, setProgress] = useState(0);
  const [emailsSent, setEmailsSent] = useState(0);
  const [currentCampaign, setCurrentCampaign] = useState<any>(null);
  const [employees, setEmployees] = useState<any[]>([]);
  const [activityLog, setActivityLog] = useState<any[]>([]);
  
  // Load real campaign data
  useEffect(() => {
    // Get campaign from navigation state or localStorage
    let campaign = location.state?.campaign;
    
    if (!campaign) {
      // Try to get the first active campaign from localStorage
      const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
      const activeCampaigns = storedCampaigns.filter(c => c.status === 'active' || c.status === 'scheduled');
      campaign = activeCampaigns[0];
    }
    
    if (campaign) {
      setCurrentCampaign(campaign);
      setCampaignStatus(campaign.status === 'active' ? 'active' : 'ready');
      
      // Set initial progress if campaign is already active
      if (campaign.status === 'active') {
        setProgress(Math.random() * 50 + 25); // Random progress for demo
        setEmailsSent(Math.floor((progress / 100) * (campaign.target_emails?.length || 0)));
      }
    }
    
    // Load employees
    const storedEmployees = JSON.parse(localStorage.getItem('hopesecure_employees') || '[]');
    setEmployees(storedEmployees);
    
    // Initialize activity log
    setActivityLog([]);
  }, [location.state]);
  
  // Function to parse emails from various formats (comma-separated, line-separated, etc.)
  const parseEmailList = (emailString: string): string[] => {
    if (!emailString.trim()) return [];
    
    return emailString
      .split(/[,\n\r;]+/) // Split by comma, newline, carriage return, or semicolon
      .map(email => email.trim())
      .filter(email => email && email.includes('@')) // Basic email validation
      .filter((email, index, arr) => arr.indexOf(email) === index); // Remove duplicates
  };
  
  // Get campaign data or use defaults
  const campaignData = currentCampaign || {
    name: "No Campaign Selected",
    description: "Please select a campaign from the dashboard",
    campaign_type: "Unknown",
    target_emails: [],
    template_id: null,
    status: 'ready'
  };
  
  const targetEmails = currentCampaign?.target_emails || [];
  const totalEmails = targetEmails.length;

  const handleStartCampaign = () => {
    if (!currentCampaign) {
      alert('No campaign selected. Please go back to dashboard and select a campaign.');
      return;
    }
    
    setCampaignStatus('launching');
    
    // Update campaign status in localStorage
    const storedCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
    const updatedCampaigns = storedCampaigns.map(c => 
      c.id === currentCampaign.id ? { ...c, status: 'active' } : c
    );
    localStorage.setItem('hopesecure_campaigns', JSON.stringify(updatedCampaigns));
  };

  // Simulate real campaign progress with real employee data
  useEffect(() => {
    if (campaignStatus === 'launching') {
      const timer = setTimeout(() => {
        setCampaignStatus('active');
        setProgress(5);
        
        // Add initial activity log entry
        if (targetEmails.length > 0) {
          const randomEmail = targetEmails[Math.floor(Math.random() * targetEmails.length)];
          const employee = employees.find(emp => emp.email === randomEmail);
          setActivityLog([{
            id: Date.now(),
            type: 'email_sent',
            email: randomEmail,
            name: employee?.name || randomEmail.split('@')[0],
            department: employee?.department || 'Unknown',
            action: 'Campaign started',
            timestamp: new Date().toISOString(),
            icon: 'mail'
          }]);
        }
      }, 3000);
      return () => clearTimeout(timer);
    }

    if (campaignStatus === 'active' && targetEmails.length > 0) {
      const interval = setInterval(() => {
        setProgress(prev => {
          const newProgress = Math.min(prev + Math.random() * 3, 100);
          const newEmailsSent = Math.floor((newProgress / 100) * totalEmails);
          setEmailsSent(newEmailsSent);
          
          // Generate realistic activity logs
          if (Math.random() < 0.3 && newEmailsSent > 0) { // 30% chance to generate activity
            const randomEmail = targetEmails[Math.floor(Math.random() * Math.min(newEmailsSent, targetEmails.length))];
            const employee = employees.find(emp => emp.email === randomEmail);
            const activities = ['opened_email', 'clicked_link', 'entered_credentials', 'downloaded_attachment'];
            const activityType = activities[Math.floor(Math.random() * activities.length)];
            
            const actionTexts = {
              opened_email: 'opened email',
              clicked_link: 'clicked phishing link', 
              entered_credentials: 'entered credentials',
              downloaded_attachment: 'downloaded attachment'
            };
            
            setActivityLog(prev => [{
              id: Date.now() + Math.random(),
              type: activityType,
              email: randomEmail,
              name: employee?.name || randomEmail.split('@')[0],
              department: employee?.department || 'Unknown',
              action: actionTexts[activityType],
              timestamp: new Date().toISOString(),
              icon: activityType === 'opened_email' ? 'eye' : 
                    activityType === 'clicked_link' ? 'mouse-pointer' :
                    activityType === 'entered_credentials' ? 'alert-triangle' : 'download'
            }, ...prev.slice(0, 9)]); // Keep only last 10 activities
          }
          
          if (newProgress >= 100) {
            setCampaignStatus('completed');
          }
          return newProgress;
        });
      }, 4000); // Slower update rate for more realistic feel
      return () => clearInterval(interval);
    }
  }, [campaignStatus, totalEmails, targetEmails, employees]);

  const handlePauseCampaign = () => {
    setCampaignStatus(campaignStatus === 'paused' ? 'active' : 'paused');
  };

  const handleStopCampaign = () => {
    setCampaignStatus('completed');
  };

  const getStatusBadge = () => {
    switch (campaignStatus) {
      case 'ready':
        return <Badge variant="outline" className="bg-gray-50 text-gray-700 border-gray-200"><Target className="w-3 h-3 mr-1" />Ready to Launch</Badge>;
      case 'launching':
        return <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200"><Clock className="w-3 h-3 mr-1" />Launching</Badge>;
      case 'active':
        return <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200"><Play className="w-3 h-3 mr-1" />Active</Badge>;
      case 'paused':
        return <Badge variant="outline" className="bg-yellow-50 text-yellow-700 border-yellow-200"><Pause className="w-3 h-3 mr-1" />Paused</Badge>;
      case 'completed':
        return <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-200"><CheckCircle className="w-3 h-3 mr-1" />Completed</Badge>;
    }
  };

  // Real-time stats based on actual campaign progress
  const realTimeStats = {
    emailsOpened: campaignStatus === 'ready' ? 0 : Math.floor(emailsSent * 0.65),
    linksClicked: campaignStatus === 'ready' ? 0 : Math.floor(emailsSent * 0.23),
    credentialsEntered: campaignStatus === 'ready' ? 0 : Math.floor(emailsSent * 0.08),
    attachmentsDownloaded: campaignStatus === 'ready' ? 0 : Math.floor(emailsSent * 0.05)
  };

  // Generate vulnerable employees list from actual employees and activity
  const vulnerableEmployees = activityLog
    .filter(activity => activity.type !== 'email_sent')
    .reduce((acc, activity) => {
      const existing = acc.find(emp => emp.email === activity.email);
      if (existing) {
        if (!existing.actions.includes(activity.action)) {
          existing.actions.push(activity.action);
        }
      } else {
        acc.push({
          name: activity.name,
          email: activity.email,
          department: activity.department,
          actions: [activity.action],
          riskLevel: activity.type === 'entered_credentials' ? 'High' : 
                    activity.type === 'clicked_link' ? 'Medium' : 'Low'
        });
      }
      return acc;
    }, [])
    .slice(0, 5); // Show top 5 vulnerable employees

  // Calculate department statistics based on real employee data and activity
  const getDepartmentAnalysis = () => {
    if (!employees.length || !targetEmails.length) {
      return [];
    }

    // Get employees who are targets of this campaign
    const targetEmployees = employees.filter(emp => 
      targetEmails.includes(emp.email)
    );

    // Group by department
    const departmentGroups = targetEmployees.reduce((acc, emp) => {
      const dept = emp.department || 'Unknown';
      if (!acc[dept]) {
        acc[dept] = [];
      }
      acc[dept].push(emp);
      return acc;
    }, {});

    // Calculate vulnerability for each department based on activity log
    return Object.keys(departmentGroups).map(dept => {
      const deptEmployees = departmentGroups[dept];
      const totalInDept = deptEmployees.length;
      
      // Count vulnerable employees (those who appeared in activity log with risky actions)
      const vulnerableEmails = activityLog
        .filter(activity => 
          activity.department === dept && 
          (activity.type === 'clicked_link' || 
           activity.type === 'entered_credentials' || 
           activity.type === 'downloaded_attachment')
        )
        .map(activity => activity.email);
      
      const uniqueVulnerable = [...new Set(vulnerableEmails)];
      const vulnerableCount = uniqueVulnerable.length;
      const vulnerabilityRate = totalInDept > 0 ? Math.round((vulnerableCount / totalInDept) * 100) : 0;

      return {
        dept,
        total: totalInDept,
        vulnerable: vulnerableCount,
        rate: vulnerabilityRate
      };
    })
    .filter(dept => dept.total > 0) // Only show departments with employees
    .sort((a, b) => b.rate - a.rate); // Sort by vulnerability rate descending
  };

  const departmentAnalysis = getDepartmentAnalysis();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/dashboard')}
              className="hover:bg-white/50"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Campaign Execution</h1>
              <p className="text-gray-600 mt-1">
                {campaignData.name} - {campaignData.campaign_type || 'Unknown Type'}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {getStatusBadge()}
          </div>
        </div>

        {/* Campaign Summary */}
        <Card className="mb-8 bg-blue-50 border-blue-200">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm font-medium text-blue-800">Campaign Template</p>
                <p className="text-lg font-semibold text-blue-900">{campaignData.template}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-blue-800">Target Department</p>
                <p className="text-lg font-semibold text-blue-900">{campaignData.department}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-blue-800">Total Recipients</p>
                <p className="text-lg font-semibold text-blue-900">{totalEmails} employees</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Campaign Control Panel */}
        <Card className="mb-8 border-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center text-xl">
                  <Target className="h-5 w-5 mr-2 text-security-blue" />
                  Campaign Control Panel
                </CardTitle>
                <CardDescription>Monitor and control your phishing simulation campaign</CardDescription>
              </div>
              <div className="flex space-x-2">
                {campaignStatus === 'ready' && (
                  <Button 
                    variant="default" 
                    onClick={handleStartCampaign}
                    className="hover:bg-green-600 bg-green-700"
                  >
                    <Play className="h-4 w-4 mr-2" />
                    Start Campaign
                  </Button>
                )}
                {campaignStatus === 'active' && (
                  <Button 
                    variant="outline" 
                    onClick={handlePauseCampaign}
                    className="hover:bg-yellow-50"
                  >
                    <Pause className="h-4 w-4 mr-2" />
                    Pause
                  </Button>
                )}
                {campaignStatus === 'paused' && (
                  <Button 
                    variant="outline" 
                    onClick={handlePauseCampaign}
                    className="hover:bg-green-50"
                  >
                    <Play className="h-4 w-4 mr-2" />
                    Resume
                  </Button>
                )}
                {(campaignStatus === 'active' || campaignStatus === 'paused') && (
                  <Button 
                    variant="destructive" 
                    onClick={handleStopCampaign}
                  >
                    <StopCircle className="h-4 w-4 mr-2" />
                    Stop Campaign
                  </Button>
                )}
                {campaignStatus === 'completed' && (
                  <Button 
                    variant="default"
                    onClick={() => navigate('/dashboard')}
                  >
                    <FileText className="h-4 w-4 mr-2" />
                    View Full Report
                  </Button>
                )}
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {campaignStatus === 'ready' && (
                <Alert>
                  <Target className="h-4 w-4" />
                  <AlertDescription>
                    Campaign is ready to launch. Click "Start Campaign" to begin sending emails to {totalEmails} target recipients.
                  </AlertDescription>
                </Alert>
              )}
              {campaignStatus === 'launching' && (
                <Alert>
                  <Clock className="h-4 w-4" />
                  <AlertDescription>
                    Campaign is being launched. Emails are being sent to {totalEmails} target recipients...
                  </AlertDescription>
                </Alert>
              )}
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="text-sm font-medium">Email Delivery Progress</div>
                  <Badge variant="outline">{emailsSent} / {totalEmails} sent</Badge>
                </div>
                <div className="text-sm text-gray-600">{Math.round(progress)}% complete</div>
              </div>
              {campaignStatus !== 'ready' && (
                <Progress value={progress} className="h-3" />
              )}
              {campaignStatus === 'ready' && (
                <div className="h-3 bg-gray-100 rounded-full">
                  <div className="h-full bg-gray-300 rounded-full w-0 transition-all duration-300"></div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Target Email Summary */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center text-lg">
              <Users className="h-5 w-5 mr-2 text-blue-600" />
              Target Recipients ({totalEmails} emails)
            </CardTitle>
            <CardDescription>Campaign will be sent to the following email addresses</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 max-h-40 overflow-y-auto">
              {targetEmails.map((email, index) => (
                <div key={index} className="flex items-center space-x-2 p-2 bg-gray-50 rounded text-sm">
                  <Mail className="h-3 w-3 text-gray-400" />
                  <span className="truncate">{email}</span>
                  {emailsSent > index && (
                    <CheckCircle className="h-3 w-3 text-green-500 flex-shrink-0" />
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Real-time Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Emails Opened</p>
                  <p className="text-2xl font-bold text-blue-600">{realTimeStats.emailsOpened}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {emailsSent > 0 ? `${Math.round((realTimeStats.emailsOpened / emailsSent) * 100)}%` : '0%'} open rate
                  </p>
                </div>
                <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Eye className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Links Clicked</p>
                  <p className="text-2xl font-bold text-yellow-600">{realTimeStats.linksClicked}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {emailsSent > 0 ? `${Math.round((realTimeStats.linksClicked / emailsSent) * 100)}%` : '0%'} click rate
                  </p>
                </div>
                <div className="h-12 w-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <MousePointer className="h-6 w-6 text-yellow-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Credentials Entered</p>
                  <p className="text-2xl font-bold text-red-600">{realTimeStats.credentialsEntered}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {emailsSent > 0 ? `${Math.round((realTimeStats.credentialsEntered / emailsSent) * 100)}%` : '0%'} compromise rate
                  </p>
                </div>
                <div className="h-12 w-12 bg-red-100 rounded-lg flex items-center justify-center">
                  <AlertTriangle className="h-6 w-6 text-red-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Downloads</p>
                  <p className="text-2xl font-bold text-purple-600">{realTimeStats.attachmentsDownloaded}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {emailsSent > 0 ? `${Math.round((realTimeStats.attachmentsDownloaded / emailsSent) * 100)}%` : '0%'} download rate
                  </p>
                </div>
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Download className="h-6 w-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Analysis */}
        <Tabs defaultValue="vulnerable" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="vulnerable">Vulnerable Employees</TabsTrigger>
            <TabsTrigger value="timeline">Activity Timeline</TabsTrigger>
            <TabsTrigger value="departments">Department Analysis</TabsTrigger>
          </TabsList>

          <TabsContent value="vulnerable">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="h-5 w-5 mr-2 text-red-600" />
                  Employees Who Fell for the Simulation
                </CardTitle>
                <CardDescription>
                  These employees require immediate security awareness training
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {vulnerableEmployees.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      <Shield className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                      <p className="text-lg font-medium">No vulnerable employees detected yet</p>
                      <p className="text-sm">Start the campaign to begin tracking employee interactions</p>
                    </div>
                  ) : (
                    vulnerableEmployees.map((employee, index) => (
                      <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3">
                            <div>
                              <p className="font-medium">{employee.name}</p>
                              <p className="text-sm text-gray-600">{employee.email}</p>
                            </div>
                            <Badge variant="outline">{employee.department}</Badge>
                          </div>
                          <div className="mt-2 flex space-x-2">
                            {employee.actions.map((action, actionIndex) => (
                              <Badge key={actionIndex} variant="secondary" className="text-xs">
                                {action}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <Badge 
                            variant={employee.riskLevel === 'High' ? 'destructive' : employee.riskLevel === 'Medium' ? 'outline' : 'secondary'}
                          >
                            {employee.riskLevel} Risk
                          </Badge>
                          <Button variant="outline" size="sm">
                            Assign Training
                          </Button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="timeline">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Clock className="h-5 w-5 mr-2 text-blue-600" />
                  Real-time Activity Timeline
                </CardTitle>
                <CardDescription>
                  Live feed of employee interactions with the phishing simulation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {activityLog.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      <Clock className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                      <p className="text-lg font-medium">No activity yet</p>
                      <p className="text-sm">Activity will appear here once the campaign starts</p>
                    </div>
                  ) : (
                    activityLog.map((activity) => {
                      const getActivityIcon = (type: string) => {
                        switch (type) {
                          case 'opened_email': return <Eye className="h-4 w-4 text-blue-600" />;
                          case 'clicked_link': return <MousePointer className="h-4 w-4 text-yellow-600" />;
                          case 'entered_credentials': return <AlertTriangle className="h-4 w-4 text-red-600" />;
                          case 'downloaded_attachment': return <Download className="h-4 w-4 text-purple-600" />;
                          default: return <Mail className="h-4 w-4 text-green-600" />;
                        }
                      };
                      
                      const getActivityColor = (type: string) => {
                        switch (type) {
                          case 'opened_email': return 'bg-blue-50 border-blue-400';
                          case 'clicked_link': return 'bg-yellow-50 border-yellow-400';
                          case 'entered_credentials': return 'bg-red-50 border-red-400';
                          case 'downloaded_attachment': return 'bg-purple-50 border-purple-400';
                          default: return 'bg-green-50 border-green-400';
                        }
                      };
                      
                      return (
                        <div key={activity.id} className={`flex items-center space-x-3 p-3 rounded-lg border-l-4 ${getActivityColor(activity.type)}`}>
                          {getActivityIcon(activity.type)}
                          <div className="flex-1">
                            <p className="text-sm font-medium">
                              {activity.email} {activity.action}
                            </p>
                            <p className="text-xs text-gray-600">
                              {activity.department} • {new Date(activity.timestamp).toLocaleTimeString()}
                            </p>
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="departments">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2 text-green-600" />
                  Department Risk Analysis
                </CardTitle>
                <CardDescription>
                  Breakdown of vulnerability by department
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {departmentAnalysis.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      <TrendingUp className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                      <p className="text-lg font-medium">No department data available</p>
                      <p className="text-sm">Employee activity will generate department statistics</p>
                    </div>
                  ) : (
                    departmentAnalysis.map((dept, index) => (
                      <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-medium">{dept.dept}</h3>
                            <span className="text-sm text-gray-600">
                              {dept.vulnerable}/{dept.total} employees affected
                            </span>
                          </div>
                          <Progress value={dept.rate} className="h-2" />
                        </div>
                        <div className="ml-4 text-right">
                          <p className={`text-lg font-bold ${
                            dept.rate >= 30 ? 'text-red-600' : 
                            dept.rate >= 15 ? 'text-yellow-600' : 
                            'text-green-600'
                          }`}>
                            {dept.rate}%
                          </p>
                          <p className="text-xs text-gray-600">vulnerability rate</p>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default CampaignExecution;
