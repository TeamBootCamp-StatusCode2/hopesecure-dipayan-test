import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { 
  ArrowLeft, 
  Mail, 
  Globe, 
  Target, 
  Eye, 
  Settings, 
  BarChart3,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Send
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const MultiDomainCampaign = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [availableDomains, setAvailableDomains] = useState([]);
  const [domainStats, setDomainStats] = useState([]);
  const [testResults, setTestResults] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    campaignName: "",
    targetEmails: [],
    domainType: "corporate",
    useRandomDomains: true,
    delaySeconds: 2,
    templateType: "microsoft_security"
  });

  // Email input state
  const [emailInput, setEmailInput] = useState("");

  // Available templates
  const emailTemplates = [
    {
      value: "microsoft_security",
      label: "Microsoft Security Alert",
      description: "Fake Microsoft security notification",
      riskLevel: "high"
    },
    {
      value: "google_verification", 
      label: "Google Account Verification",
      description: "Fake Google account verification",
      riskLevel: "medium"
    },
    {
      value: "bank_fraud_alert",
      label: "Bank Fraud Alert",
      description: "Fake banking security alert",
      riskLevel: "high"
    }
  ];

  // Domain types
  const domainTypes = [
    { value: "corporate", label: "Corporate (Microsoft, Google)", description: "Business email spoofing" },
    { value: "banking", label: "Banking & Finance", description: "Financial institutions" },
    { value: "social", label: "Social Media", description: "Facebook, Twitter, etc." },
    { value: "ecommerce", label: "E-commerce", description: "Amazon, Shopping sites" },
    { value: "government", label: "Government", description: "Official government notices" }
  ];

  useEffect(() => {
    loadAvailableDomains();
    loadDomainStatistics();
  }, []);

  const loadAvailableDomains = async () => {
    try {
      const response = await fetch('/api/campaigns/multi-domain/domains/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setAvailableDomains(data.verified_domains || []);
      }
    } catch (error) {
      console.error('Error loading domains:', error);
    }
  };

  const loadDomainStatistics = async () => {
    try {
      const response = await fetch('/api/campaigns/multi-domain/statistics/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setDomainStats(data.domain_statistics || []);
      }
    } catch (error) {
      console.error('Error loading domain stats:', error);
    }
  };

  const handleAddEmail = () => {
    const emails = emailInput.split(',').map(email => email.trim()).filter(email => email);
    const validEmails = emails.filter(email => email.includes('@'));
    
    setFormData(prev => ({
      ...prev,
      targetEmails: [...new Set([...prev.targetEmails, ...validEmails])]
    }));
    
    setEmailInput("");
  };

  const handleRemoveEmail = (emailToRemove) => {
    setFormData(prev => ({
      ...prev,
      targetEmails: prev.targetEmails.filter(email => email !== emailToRemove)
    }));
  };

  const handleTestEmail = async () => {
    if (!formData.targetEmails.length) {
      alert('Please add at least one target email');
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await fetch('/api/campaigns/multi-domain/test-email/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          test_email: formData.targetEmails[0],
          template_type: formData.templateType,
          sender_domain: availableDomains[0]?.name || null
        }),
      });

      const data = await response.json();
      setTestResults(data);
      
      if (data.success) {
        alert('Test email sent successfully!');
      } else {
        alert(`Test failed: ${data.error}`);
      }
    } catch (error) {
      console.error('Test email error:', error);
      alert('Error sending test email');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSendCampaign = async () => {
    if (!formData.campaignName || !formData.targetEmails.length) {
      alert('Please fill in campaign name and add target emails');
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await fetch('/api/campaigns/multi-domain/create/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          campaign_name: formData.campaignName,
          target_emails: formData.targetEmails,
          domain_type: formData.domainType,
          use_random_domains: formData.useRandomDomains,
          delay_seconds: formData.delaySeconds
        }),
      });

      const data = await response.json();
      
      if (data.success) {
        alert(`✅ Campaign sent successfully! Sent: ${data.results.sent}, Failed: ${data.results.failed}`);
        navigate('/dashboard');
      } else {
        alert(`Campaign failed: ${data.error}`);
      }
    } catch (error) {
      console.error('Campaign error:', error);
      alert('Error sending campaign');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-hero text-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          <div className="flex items-center gap-4 mb-6">
            <Button 
              variant="outline" 
              size="sm"
              className="border-white/30 text-white hover:bg-white/10"
              onClick={() => navigate('/dashboard')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </div>
          <div>
            <h1 className="text-3xl font-bold mb-2">🌐 Multi-Domain Phishing Campaign</h1>
            <p className="text-gray-300">বিভিন্ন domain extension দিয়ে advanced phishing simulation</p>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Campaign Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Campaign Basic Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-security-blue" />
                  Campaign Configuration
                </CardTitle>
                <CardDescription>Configure your multi-domain phishing campaign</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="campaign-name">Campaign Name</Label>
                  <Input 
                    id="campaign-name" 
                    placeholder="e.g., Multi-Domain Security Test 2025" 
                    className="mt-1"
                    value={formData.campaignName}
                    onChange={(e) => setFormData(prev => ({...prev, campaignName: e.target.value}))}
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <Label>Domain Type</Label>
                    <Select value={formData.domainType} onValueChange={(value) => setFormData(prev => ({...prev, domainType: value}))}>
                      <SelectTrigger className="mt-1">
                        <SelectValue placeholder="Select domain type" />
                      </SelectTrigger>
                      <SelectContent>
                        {domainTypes.map((type) => (
                          <SelectItem key={type.value} value={type.value}>
                            <div>
                              <div className="font-medium">{type.label}</div>
                              <div className="text-sm text-muted-foreground">{type.description}</div>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Email Template</Label>
                    <Select value={formData.templateType} onValueChange={(value) => setFormData(prev => ({...prev, templateType: value}))}>
                      <SelectTrigger className="mt-1">
                        <SelectValue placeholder="Select template" />
                      </SelectTrigger>
                      <SelectContent>
                        {emailTemplates.map((template) => (
                          <SelectItem key={template.value} value={template.value}>
                            <div>
                              <div className="font-medium">{template.label}</div>
                              <div className="text-sm text-muted-foreground">{template.description}</div>
                              <Badge variant={template.riskLevel === 'high' ? 'destructive' : 'secondary'} className="text-xs mt-1">
                                {template.riskLevel} risk
                              </Badge>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="random-domains"
                    checked={formData.useRandomDomains}
                    onCheckedChange={(checked) => setFormData(prev => ({...prev, useRandomDomains: Boolean(checked)}))}
                  />
                  <Label htmlFor="random-domains" className="text-sm font-medium">
                    Use random domains for each email (recommended)
                  </Label>
                </div>

                <div>
                  <Label htmlFor="delay">Email Delay (seconds)</Label>
                  <Input 
                    id="delay"
                    type="number"
                    min="1"
                    max="60"
                    className="mt-1"
                    value={formData.delaySeconds}
                    onChange={(e) => setFormData(prev => ({...prev, delaySeconds: parseInt(e.target.value)}))}
                  />
                  <p className="text-sm text-muted-foreground mt-1">
                    Delay between emails to avoid rate limiting
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Target Emails */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Mail className="h-5 w-5 text-security-blue" />
                  Target Emails
                </CardTitle>
                <CardDescription>Add email addresses for the campaign</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Input 
                    placeholder="Enter emails (comma separated)"
                    value={emailInput}
                    onChange={(e) => setEmailInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleAddEmail()}
                    className="flex-1"
                  />
                  <Button onClick={handleAddEmail}>Add</Button>
                </div>

                {formData.targetEmails.length > 0 && (
                  <div className="space-y-2">
                    <Label>Target Emails ({formData.targetEmails.length})</Label>
                    <div className="max-h-32 overflow-y-auto border rounded-md p-2 space-y-1">
                      {formData.targetEmails.map((email, index) => (
                        <div key={index} className="flex items-center justify-between bg-muted rounded px-2 py-1">
                          <span className="text-sm">{email}</span>
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => handleRemoveEmail(email)}
                            className="h-6 w-6 p-0"
                          >
                            ×
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <Button 
                onClick={handleTestEmail}
                variant="outline"
                disabled={isSubmitting || !formData.targetEmails.length}
                className="flex-1"
              >
                <Eye className="h-4 w-4 mr-2" />
                Send Test Email
              </Button>
              
              <Button 
                onClick={handleSendCampaign}
                disabled={isSubmitting || !formData.campaignName || !formData.targetEmails.length}
                className="flex-1 bg-security-blue hover:bg-security-blue/90"
              >
                <Send className="h-4 w-4 mr-2" />
                {isSubmitting ? 'Sending...' : 'Launch Campaign'}
              </Button>
            </div>
          </div>

          {/* Sidebar - Domain Info & Stats */}
          <div className="space-y-6">
            {/* Available Domains */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5 text-security-blue" />
                  Verified Domains
                </CardTitle>
                <CardDescription>Available domains for campaigns</CardDescription>
              </CardHeader>
              <CardContent>
                {availableDomains.length === 0 ? (
                  <div className="text-center py-6">
                    <AlertTriangle className="h-12 w-12 text-yellow-500 mx-auto mb-2" />
                    <p className="text-sm text-muted-foreground">No verified domains</p>
                    <Button variant="outline" size="sm" className="mt-2">
                      Add Domain
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {availableDomains.slice(0, 5).map((domain) => (
                      <div key={domain.id} className="flex items-center justify-between p-2 bg-muted rounded">
                        <div>
                          <div className="font-medium text-sm">{domain.name}</div>
                          <div className="text-xs text-muted-foreground">{domain.domain_type}</div>
                        </div>
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      </div>
                    ))}
                    {availableDomains.length > 5 && (
                      <p className="text-xs text-muted-foreground text-center">
                        +{availableDomains.length - 5} more domains
                      </p>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Domain Statistics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-security-blue" />
                  Domain Statistics
                </CardTitle>
              </CardHeader>
              <CardContent>
                {domainStats.length === 0 ? (
                  <p className="text-sm text-muted-foreground text-center py-4">
                    No statistics available
                  </p>
                ) : (
                  <div className="space-y-3">
                    {domainStats.slice(0, 3).map((stat, index) => (
                      <div key={index} className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span className="font-medium">{stat.domain}</span>
                          <span className="text-muted-foreground">{stat.emails_sent} sent</span>
                        </div>
                        <div className="text-xs text-muted-foreground">
                          Success: {stat.success_rate}% • Click: {stat.click_rate}%
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Test Results */}
            {testResults && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    {testResults.success ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-500" />
                    )}
                    Test Results
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div>Status: <Badge variant={testResults.success ? 'secondary' : 'destructive'}>{testResults.message}</Badge></div>
                    {testResults.email_details && (
                      <>
                        <div>Recipient: {testResults.email_details.recipient}</div>
                        <div>Sender: {testResults.email_details.sender}</div>
                        <div>Template: {testResults.email_details.template}</div>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MultiDomainCampaign;
