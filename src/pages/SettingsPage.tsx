import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import DashboardHeader from "@/components/DashboardHeader";
import { 
  Users, 
  Bell, 
  Download,
  Upload,
  Save
} from "lucide-react";
import { useState } from "react";

const SettingsPage = () => {
  const [organizationSettings, setOrganizationSettings] = useState({
    companyName: "TechCorp Inc.",
    domain: "techcorp.com",
    industry: "technology",
    employeeCount: "200-500",
    timezone: "UTC-5",
    language: "en",
    logo: null,
    address: "123 Business District, City",
    phone: "+1 (555) 123-4567",
    website: "https://techcorp.com",
    registrationNumber: "REG-2024-001",
    founded: "2020"
  });

  const [notificationSettings, setNotificationSettings] = useState({
    emailAlerts: true,
    campaignStarted: true,
    highRiskDetected: true,
    campaignCompleted: true,
    weeklyReports: true,
    monthlyReports: true,
    alertThreshold: 25
  });

  const handleSaveSettings = (section: string) => {
    // In real implementation, this would save to backend
    console.log(`Saving ${section} settings...`);
  };

  return (
    <>
      <DashboardHeader />
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Company Management</h1>
            <p className="text-gray-600 mt-1">Manage your organization settings and configuration</p>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline">
              <Upload className="h-4 w-4 mr-2" />
              Import Config
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Export Config
            </Button>
          </div>
        </div>

        <Tabs defaultValue="organization" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="organization">Company Details</TabsTrigger>
            <TabsTrigger value="notifications">Notifications</TabsTrigger>
          </TabsList>

          <TabsContent value="organization">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Users className="h-5 w-5 mr-2" />
                    Company Registration & Information
                  </CardTitle>
                  <CardDescription>Manage your company details and business information</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="company-name">Company Name</Label>
                      <Input 
                        id="company-name" 
                        value={organizationSettings.companyName}
                        onChange={(e) => setOrganizationSettings({...organizationSettings, companyName: e.target.value})}
                      />
                    </div>
                    <div>
                      <Label htmlFor="domain">Primary Domain</Label>
                      <Input 
                        id="domain" 
                        value={organizationSettings.domain}
                        onChange={(e) => setOrganizationSettings({...organizationSettings, domain: e.target.value})}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="industry">Industry</Label>
                      <Select value={organizationSettings.industry} onValueChange={(value) => setOrganizationSettings({...organizationSettings, industry: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="technology">Technology</SelectItem>
                          <SelectItem value="finance">Finance</SelectItem>
                          <SelectItem value="healthcare">Healthcare</SelectItem>
                          <SelectItem value="education">Education</SelectItem>
                          <SelectItem value="manufacturing">Manufacturing</SelectItem>
                          <SelectItem value="retail">Retail</SelectItem>
                          <SelectItem value="other">Other</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="employee-count">Employee Count</Label>
                      <Select value={organizationSettings.employeeCount} onValueChange={(value) => setOrganizationSettings({...organizationSettings, employeeCount: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="1-50">1-50</SelectItem>
                          <SelectItem value="51-200">51-200</SelectItem>
                          <SelectItem value="200-500">200-500</SelectItem>
                          <SelectItem value="500-1000">500-1000</SelectItem>
                          <SelectItem value="1000+">1000+</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="timezone">Timezone</Label>
                      <Select value={organizationSettings.timezone} onValueChange={(value) => setOrganizationSettings({...organizationSettings, timezone: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="UTC-12">UTC-12 (Baker Island)</SelectItem>
                          <SelectItem value="UTC-8">UTC-8 (Pacific)</SelectItem>
                          <SelectItem value="UTC-5">UTC-5 (Eastern)</SelectItem>
                          <SelectItem value="UTC+0">UTC+0 (London)</SelectItem>
                          <SelectItem value="UTC+1">UTC+1 (Berlin)</SelectItem>
                          <SelectItem value="UTC+8">UTC+8 (Singapore)</SelectItem>
                          <SelectItem value="UTC+9">UTC+9 (Tokyo)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="language">Default Language</Label>
                      <Select value={organizationSettings.language} onValueChange={(value) => setOrganizationSettings({...organizationSettings, language: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="en">English</SelectItem>
                          <SelectItem value="es">Spanish</SelectItem>
                          <SelectItem value="fr">French</SelectItem>
                          <SelectItem value="de">German</SelectItem>
                          <SelectItem value="zh">Chinese</SelectItem>
                          <SelectItem value="ja">Japanese</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="company-address">Company Address</Label>
                      <Input 
                        id="company-address" 
                        value={organizationSettings.address}
                        onChange={(e) => setOrganizationSettings({...organizationSettings, address: e.target.value})}
                      />
                    </div>
                    <div>
                      <Label htmlFor="company-phone">Phone Number</Label>
                      <Input 
                        id="company-phone" 
                        value={organizationSettings.phone}
                        onChange={(e) => setOrganizationSettings({...organizationSettings, phone: e.target.value})}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="company-website">Website URL</Label>
                      <Input 
                        id="company-website" 
                        value={organizationSettings.website}
                        onChange={(e) => setOrganizationSettings({...organizationSettings, website: e.target.value})}
                      />
                    </div>
                    <div>
                      <Label htmlFor="registration-number">Registration Number</Label>
                      <Input 
                        id="registration-number" 
                        value={organizationSettings.registrationNumber}
                        onChange={(e) => setOrganizationSettings({...organizationSettings, registrationNumber: e.target.value})}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="founded-year">Founded Year</Label>
                      <Input 
                        id="founded-year" 
                        value={organizationSettings.founded}
                        onChange={(e) => setOrganizationSettings({...organizationSettings, founded: e.target.value})}
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="company-logo">Company Logo</Label>
                    <div className="mt-2 flex items-center space-x-4">
                      <div className="h-16 w-16 bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                        <Users className="h-8 w-8 text-gray-400" />
                      </div>
                      <div>
                        <Button variant="outline">
                          <Upload className="h-4 w-4 mr-2" />
                          Upload Logo
                        </Button>
                        <p className="text-sm text-gray-600 mt-1">Recommended: 200x200px, PNG/JPG</p>
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-end">
                    <Button onClick={() => handleSaveSettings('organization')}>
                      <Save className="h-4 w-4 mr-2" />
                      Save Changes
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="notifications">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Bell className="h-5 w-5 mr-2" />
                    Notification Preferences
                  </CardTitle>
                  <CardDescription>Configure alerts and notification settings</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    <h3 className="font-semibold">Email Notifications</h3>
                    
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <Label>Campaign Started</Label>
                        <Switch 
                          checked={notificationSettings.campaignStarted} 
                          onCheckedChange={(checked) => setNotificationSettings({...notificationSettings, campaignStarted: checked})}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <Label>Campaign Completed</Label>
                        <Switch 
                          checked={notificationSettings.campaignCompleted} 
                          onCheckedChange={(checked) => setNotificationSettings({...notificationSettings, campaignCompleted: checked})}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <Label>High Risk Employee Detected</Label>
                        <Switch 
                          checked={notificationSettings.highRiskDetected} 
                          onCheckedChange={(checked) => setNotificationSettings({...notificationSettings, highRiskDetected: checked})}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <Label>Weekly Reports</Label>
                        <Switch 
                          checked={notificationSettings.weeklyReports} 
                          onCheckedChange={(checked) => setNotificationSettings({...notificationSettings, weeklyReports: checked})}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <Label>Monthly Reports</Label>
                        <Switch 
                          checked={notificationSettings.monthlyReports} 
                          onCheckedChange={(checked) => setNotificationSettings({...notificationSettings, monthlyReports: checked})}
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="alert-threshold">High Risk Alert Threshold (%)</Label>
                    <Input 
                      id="alert-threshold" 
                      type="number"
                      min="1"
                      max="100"
                      value={notificationSettings.alertThreshold}
                      onChange={(e) => setNotificationSettings({...notificationSettings, alertThreshold: parseInt(e.target.value)})}
                    />
                    <p className="text-sm text-gray-600 mt-1">Send alert when campaign success rate exceeds this threshold</p>
                  </div>

                  <div className="flex justify-end">
                    <Button onClick={() => handleSaveSettings('notifications')}>
                      <Save className="h-4 w-4 mr-2" />
                      Save Notification Settings
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
        </div>
      </div>
    </>
  );
};

export default SettingsPage;
