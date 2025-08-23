import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Checkbox } from "@/components/ui/checkbox";
import { ArrowLeft, Upload, Users, Mail, Calendar, Target, Eye, Star, BarChart3, AlertTriangle, X } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { getActiveTemplates, getUserCreatedTemplates, Template } from "@/data/templates";
import { apiClient } from "@/lib/api";
import EmailSelector from "@/components/EmailSelector";
import SuccessDialog from "@/components/SuccessDialog";

const CreateCampaign = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [selectedTemplate, setSelectedTemplate] = useState<number | null>(null);
  const [campaignType, setCampaignType] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [userTemplates, setUserTemplates] = useState<Template[]>([]);
  const [showPreviewDialog, setShowPreviewDialog] = useState(false);
  const [previewTemplate, setPreviewTemplate] = useState<Template | null>(null);
  const [employees, setEmployees] = useState<any[]>([]);
  const [showEmployeeDialog, setShowEmployeeDialog] = useState(false);
  const [selectedEmployees, setSelectedEmployees] = useState<any[]>([]);
  const [selectedEmailAccount, setSelectedEmailAccount] = useState<{
    email: string;
    domain: string;
    accountId: number;
  } | null>(null);
  
  // Success dialog state
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);
  const [successResults, setSuccessResults] = useState<any>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    scheduleDate: "",
    targetEmails: [] as string[],
    useMultipleDomains: false, // Multi-domain option
    domainType: "corporate", // Domain type for multi-domain
    selectedDomain: "", // Selected specific domain
    customEmailPrefix: "noreply", // Custom email prefix
  });
  
  // Available domains from backend
  const [availableDomains, setAvailableDomains] = useState<any[]>([]);
  const [customEmailAddress, setCustomEmailAddress] = useState("");
  const [emailInput, setEmailInput] = useState(""); // For manual email input

  // Handle adding email manually
  const handleAddEmail = () => {
    const email = emailInput.trim();
    if (email && !formData.targetEmails.includes(email)) {
      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (emailRegex.test(email)) {
        setFormData(prev => ({
          ...prev,
          targetEmails: [...prev.targetEmails, email]
        }));
        setEmailInput('');
      } else {
        alert('Please enter a valid email address');
      }
    } else if (formData.targetEmails.includes(email)) {
      alert('Email already added');
    }
  };

  // Handle email input on Enter key
  const handleEmailKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddEmail();
    }
  };

  // Load available domains
  const loadAvailableDomains = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/campaigns/test-domains/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Domains loaded:', data);
        // Format domains for frontend
        const formattedDomains = data.domains.map((domain: any) => ({
          id: domain.id,
          name: domain.name,
          domain_type: domain.domain_type,
          status: domain.status,
          success_rate: 85, // Default value
          click_rate: 12, // Default value
          display_name: `${domain.name} (${domain.domain_type.charAt(0).toUpperCase() + domain.domain_type.slice(1)})`
        }));
        setAvailableDomains(formattedDomains);
      } else {
        console.error('Failed to load domains:', response.status);
      }
    } catch (error) {
      console.error('Error loading domains:', error);
    }
  };

  // Load user-created templates on component mount
  useEffect(() => {
    loadUserTemplates();
    loadEmployees();
    loadAvailableDomains(); // Load domains
    
    // Check if editing a draft campaign
    if (location.state?.editCampaign) {
      const campaign = location.state.editCampaign;
      setFormData({
        name: campaign.name || "",
        description: campaign.description || "",
        scheduleDate: campaign.scheduled_date || "",
        targetEmails: campaign.target_emails || [],
        useMultipleDomains: campaign.use_multiple_domains || false,
        domainType: campaign.domain_type || "corporate",
        selectedDomain: campaign.domain_id ? campaign.domain_id.toString() : "",
        customEmailPrefix: campaign.custom_email_prefix || "noreply",
      });
      setCampaignType(campaign.campaign_type || "");
      setSelectedTemplate(campaign.template_id || null);
    }
  }, [location.state]);

  // Load employees from Employee Management
  const loadEmployees = async () => {
    try {
      // First load from localStorage
      const savedEmployees = JSON.parse(localStorage.getItem('hopesecure_employees') || '[]');
      let localEmployees = Array.isArray(savedEmployees) ? savedEmployees : [];
      
      // Try to fetch from API
      try {
        const employeeData = await apiClient.getEmployees();
        const apiEmployees = Array.isArray(employeeData) ? employeeData : ((employeeData as any)?.results || []);
        
        if (apiEmployees.length > 0) {
          // Convert API employees to frontend format
          const convertedApiEmployees = apiEmployees.map(emp => ({
            id: emp.id,
            name: `${emp.first_name || ''} ${emp.last_name || ''}`.trim(),
            email: emp.email,
            department: emp.department_name || emp.department,
            position: emp.position || '',
            status: emp.is_active ? 'Active' : 'Inactive'
          }));
          
          // Merge employees
          const mergedEmployees = [...localEmployees];
          convertedApiEmployees.forEach(apiEmp => {
            if (!mergedEmployees.find(localEmp => localEmp.email === apiEmp.email)) {
              mergedEmployees.push(apiEmp);
            }
          });
          setEmployees(mergedEmployees);
        } else {
          setEmployees(localEmployees);
        }
      } catch (apiError) {
        console.warn('API fetch failed, using localStorage only:', apiError);
        setEmployees(localEmployees);
      }
    } catch (error) {
      console.error('Error loading employees:', error);
      setEmployees([]);
    }
  };

  const loadUserTemplates = async () => {
    try {
      // Try to load from API first
      const apiTemplates = await apiClient.getTemplates();
      // Convert API templates to local template format
      const convertedTemplates = apiTemplates.map(apiTemplate => ({
        id: apiTemplate.id,
        name: apiTemplate.name,
        category: apiTemplate.category,
        description: apiTemplate.description,
        usageCount: 0,
        successRate: '0%',
        lastUsed: 'Never',
        status: apiTemplate.status || 'Draft',
        riskLevel: apiTemplate.difficulty || 'intermediate',
        preview: apiTemplate.description,
        emailSubject: apiTemplate.email_subject || '',
        domain: apiTemplate.domain || 'custom.com',
        difficulty: apiTemplate.difficulty || 'Intermediate',
        rating: 0,
        tags: [],
        hasAttachments: apiTemplate.has_attachments || false,
        hasCSS: apiTemplate.has_css || false,
        isResponsive: apiTemplate.is_responsive || true,
        thumbnail: '/placeholder.svg',
        htmlContent: apiTemplate.html_content || '',
        cssStyles: apiTemplate.css_styles || '',
        senderName: apiTemplate.sender_name || '',
        senderEmail: apiTemplate.sender_email || '',
        landingPageUrl: apiTemplate.landing_page_url || '',
        priority: apiTemplate.priority || 'normal',
        trackingEnabled: apiTemplate.tracking_enabled || true
      }));
      setUserTemplates(convertedTemplates.filter(template => template.status !== 'system'));
    } catch (error) {
      console.warn('API failed, loading from localStorage:', error);
      
      // Fallback: Load from localStorage
      const storedTemplates = localStorage.getItem('hopesecure_user_templates');
      if (storedTemplates) {
        const parsed = JSON.parse(storedTemplates);
        setUserTemplates(parsed);
      } else {
        // If no stored templates, load pre-made templates as fallback
        const preMadeTemplates = getActiveTemplates();
        setUserTemplates(preMadeTemplates);
      }
    }
  };

  // Get templates - use user templates or fallback to pre-made templates
  const templates = userTemplates.length > 0 ? userTemplates : getActiveTemplates();

  const campaignTypes = [
    { value: "credential", label: "Credential Phishing", description: "Test if users enter login credentials" },
    { value: "data-input", label: "Data Input Form", description: "Test if users submit sensitive information" },
    { value: "link-click", label: "Link Click Tracking", description: "Track who clicks suspicious links" },
    { value: "attachment", label: "Fake Attachment", description: "Test if users download suspicious files" }
  ];

  // Handle form field changes
  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Handle template preview
  const handlePreviewTemplate = (template: Template) => {
    setPreviewTemplate(template);
    setShowPreviewDialog(true);
  };

  // Handle employee selection
  const handleSelectFromEmployees = () => {
    setShowEmployeeDialog(true);
  };

  const handleEmployeeToggle = (employee: any) => {
    setSelectedEmployees(prev => {
      const isSelected = prev.find(emp => emp.id === employee.id);
      if (isSelected) {
        return prev.filter(emp => emp.id !== employee.id);
      } else {
        return [...prev, employee];
      }
    });
  };

  const handleConfirmEmployeeSelection = () => {
    const newEmails = selectedEmployees.map(emp => emp.email);
    const existingEmails = formData.targetEmails;
    
    // Filter out emails that already exist
    const uniqueNewEmails = newEmails.filter(email => !existingEmails.includes(email));
    
    if (uniqueNewEmails.length === 0) {
      alert('All selected employees are already in the target list.');
      setShowEmployeeDialog(false);
      setSelectedEmployees([]);
      return;
    }
    
    setFormData(prev => ({
      ...prev,
      targetEmails: [...prev.targetEmails, ...uniqueNewEmails]
    }));
    
    setShowEmployeeDialog(false);
    setSelectedEmployees([]);
    
    if (uniqueNewEmails.length !== newEmails.length) {
      alert(`${uniqueNewEmails.length} new employees added. ${newEmails.length - uniqueNewEmails.length} were already in the list.`);
    }
  };

  // Handle removing an email
  const handleRemoveEmail = (emailToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      targetEmails: prev.targetEmails.filter(email => email !== emailToRemove)
    }));
  };

  // Handle form submission
  const handleSubmit = async (isDraft: boolean = false) => {
    // Basic validation
    if (!formData.name || !campaignType || !selectedTemplate) {
      alert('Please fill in all required fields (Name, Type, Template)');
      return;
    }

    if (formData.targetEmails.length === 0) {
      alert('Please add at least one target email address');
      return;
    }

    if (!selectedEmailAccount) {
      alert('Please select an email account to send from');
      return;
    }

    // Additional validation for multi-domain campaigns
    if (formData.useMultipleDomains && !formData.selectedDomain) {
      alert('Please select a domain for custom domain campaigns');
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Use selected email account or default verified email
      let senderEmail = selectedEmailAccount?.email || 'hope@hopesecure.tech';

      // Prepare campaign data for launch
      const campaignData = {
        name: formData.name,
        description: formData.description,
        campaign_type: Array.isArray(campaignType) ? campaignType[0] : campaignType,
        template_id: selectedTemplate,
        scheduled_date: formData.scheduleDate || null,
        target_emails: formData.targetEmails.filter(email => email.trim()),
        status: isDraft ? 'draft' : 'scheduled',
        created_at: new Date().toISOString(),
        // Custom domain specific fields
        use_custom_domain: false, // Force disable custom domain for now
        domain_id: null, // Force null domain
        sender_email: senderEmail,
        custom_email_prefix: formData.customEmailPrefix,
        is_multi_domain: false // Force disable multi-domain
      };

      console.log('Launching campaign with data:', campaignData);

      if (!isDraft) {
        // First validate campaign setup
        const validationResponse = await fetch('http://localhost:8000/api/campaigns/validate/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(campaignData)
        });

        if (validationResponse.ok) {
          const validationResult = await validationResponse.json();
          
          if (!validationResult.validation.ready_to_launch) {
            const issues = validationResult.validation.issues.join('\\n');
            alert(`Campaign validation failed:\\n${issues}`);
            setIsSubmitting(false);
            return;
          }
          
          // Show warnings if any
          if (validationResult.validation.warnings.length > 0) {
            const warnings = validationResult.validation.warnings.join('\\n');
            const proceed = confirm(`Campaign has warnings:\\n${warnings}\\n\\nDo you want to proceed?`);
            if (!proceed) {
              setIsSubmitting(false);
              return;
            }
          }
        }

        // Launch campaign
        console.log('🚀 About to launch campaign with payload:', JSON.stringify(campaignData, null, 2));
        
        const launchResponse = await fetch('http://localhost:8000/api/campaigns/launch/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(campaignData)
        });

        console.log('📨 Launch response status:', launchResponse.status);
        console.log('📨 Launch response headers:', Object.fromEntries(launchResponse.headers.entries()));

        if (launchResponse.ok) {
          const launchResult = await launchResponse.json();
          console.log('✅ Launch result:', launchResult);
          const results = launchResult.results;
          
          // Show modern success dialog
          setSuccessResults(results);
          setShowSuccessDialog(true);
        } else {
          const errorText = await launchResponse.text();
          console.error('❌ Launch failed response:', errorText);
          throw new Error(`Campaign launch failed: ${launchResponse.status} - ${errorText}`);
        }
      } else {
        // Save as draft (fallback to localStorage)
        const existingCampaigns = JSON.parse(localStorage.getItem('hopesecure_campaigns') || '[]');
        const newCampaign = {
          id: Date.now(),
          ...campaignData
        };
        existingCampaigns.push(newCampaign);
        localStorage.setItem('hopesecure_campaigns', JSON.stringify(existingCampaigns));
        alert(`✅ Campaign saved as draft successfully!`);
        navigate('/dashboard');
      }
      
    } catch (error) {
      console.error('Campaign error:', error);
      alert(`❌ Campaign failed: ${error.message || 'Unknown error occurred'}`);
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
            <h1 className="text-3xl font-bold mb-2">Create New Campaign</h1>
            <p className="text-gray-300">Set up a new cybersecurity awareness simulation</p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 lg:px-8 py-8">
        <form className="space-y-8" onSubmit={(e) => e.preventDefault()}>
          {/* Campaign Basic Info */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-security-blue" />
                Campaign Details
              </CardTitle>
              <CardDescription>Basic information about your security test</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="campaign-name">Campaign Name</Label>
                <Input 
                  id="campaign-name" 
                  placeholder="e.g., Q1 Security Assessment" 
                  className="mt-1"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                />
              </div>
              
              <div>
                <Label htmlFor="campaign-description">Description</Label>
                <Textarea 
                  id="campaign-description"
                  placeholder="Brief description of this campaign's objectives..."
                  className="mt-1"
                  rows={3}
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                />
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label>Campaign Type</Label>
                  <Select value={campaignType} onValueChange={setCampaignType}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select campaign type" />
                    </SelectTrigger>
                    <SelectContent>
                      {campaignTypes.map((type) => (
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
                  <Label htmlFor="schedule-date">Schedule Date</Label>
                  <Input 
                    id="schedule-date" 
                    type="datetime-local" 
                    className="mt-1"
                    value={formData.scheduleDate}
                    onChange={(e) => handleInputChange('scheduleDate', e.target.value)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Email Account Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mail className="h-5 w-5 text-security-blue" />
                Email Account Configuration
              </CardTitle>
              <CardDescription>Select which email account to use for sending this campaign</CardDescription>
            </CardHeader>
            <CardContent>
              <EmailSelector 
                onEmailSelect={setSelectedEmailAccount}
                selectedEmail={selectedEmailAccount}
              />
              
              {selectedEmailAccount && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded">
                  <p className="text-sm font-medium text-green-700">✅ Selected Sender:</p>
                  <p className="text-sm text-green-600 font-mono">
                    {selectedEmailAccount.email}
                  </p>
                  <p className="text-xs text-green-600 mt-1">
                    This email account will be used to send all campaign emails
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Template Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mail className="h-5 w-5 text-security-blue" />
                Email Template
              </CardTitle>
              <CardDescription>Choose or upload a template for your campaign</CardDescription>
            </CardHeader>
            <CardContent>
              {templates.length === 0 ? (
                <div className="text-center py-12">
                  <Mail className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">No Email Templates Available</h3>
                  <p className="text-gray-500 mb-6 max-w-md mx-auto">
                    You need to create email templates first in the Advanced Template Management section before you can create campaigns.
                  </p>
                  <Button 
                    onClick={() => navigate('/templates')}
                    className="bg-security-blue hover:bg-security-blue/90"
                  >
                    Create Templates
                  </Button>
                </div>
              ) : (
                <div className="grid md:grid-cols-2 gap-4 mb-6">
                  {templates.map((template) => (
                    <div 
                      key={template.id}
                      className={`border rounded-lg p-4 cursor-pointer transition-smooth hover:shadow-card ${
                        selectedTemplate === template.id 
                          ? 'border-security-blue bg-security-blue/5' 
                          : 'border-border'
                      }`}
                      onClick={() => setSelectedTemplate(template.id)}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-foreground">{template.name}</h3>
                        <div className="flex items-center space-x-2">
                          <Badge variant="secondary" className="text-xs">
                            {template.category}
                          </Badge>
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              handlePreviewTemplate(template);
                            }}
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      <p className="text-sm text-muted-foreground mb-2">{template.description}</p>
                      
                      <div className="flex items-center justify-between mb-2">
                        <Badge variant="outline" className={`text-xs ${
                          template.difficulty === 'Expert' ? 'border-red-200 text-red-700' :
                          template.difficulty === 'Intermediate' ? 'border-yellow-200 text-yellow-700' :
                          'border-green-200 text-green-700'
                        }`}>
                          {template.difficulty}
                        </Badge>
                      <div className="flex items-center space-x-3 text-xs text-muted-foreground">
                        <div className="flex items-center space-x-1">
                          <Star className="h-3 w-3 text-yellow-500 fill-current" />
                          <span>{template.rating}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <BarChart3 className="h-3 w-3" />
                          <span>{template.successRate}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-xs text-muted-foreground space-y-1">
                      <div><strong>Subject:</strong> {template.emailSubject}</div>
                      <div><strong>Domain:</strong> {template.domain}</div>
                      <div className="flex items-center space-x-1">
                        <strong>Tags:</strong>
                        {template.tags.slice(0, 2).map((tag) => (
                          <span key={tag} className="px-1.5 py-0.5 bg-gray-100 rounded text-xs">
                            {tag}
                          </span>
                        ))}
                        {template.tags.length > 2 && (
                          <span className="text-xs">+{template.tags.length - 2}</span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                </div>
              )}

              {templates.length > 0 && (
                <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                  <Upload className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                  <p className="text-sm text-muted-foreground mb-2">Or upload your own template</p>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => navigate('/templates')}
                  >
                    Upload Template
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Target Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5 text-security-blue" />
                Target Employees
              </CardTitle>
              <CardDescription>Select who will receive this campaign</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="border border-border rounded-lg p-4 text-center">
                  <Users className="h-8 w-8 text-security-blue mx-auto mb-2" />
                  <h3 className="font-medium mb-2">Select from Employees</h3>
                  <p className="text-sm text-muted-foreground mb-3">Choose from employee directory</p>
                  <Button variant="outline" size="sm" onClick={handleSelectFromEmployees}>
                    <Users className="h-4 w-4 mr-2" />
                    Select Employees
                  </Button>
                </div>

                <div className="border border-border rounded-lg p-4 text-center">
                  <Mail className="h-8 w-8 text-security-blue mx-auto mb-2" />
                  <h3 className="font-medium mb-2">Add Single Email</h3>
                  <p className="text-sm text-muted-foreground mb-3">Manually add individual emails</p>
                  <div className="flex space-x-1">
                    <input
                      type="email"
                      placeholder="user@company.com"
                      value={emailInput}
                      onChange={(e) => setEmailInput(e.target.value)}
                      onKeyPress={handleEmailKeyPress}
                      className="flex-1 px-2 py-1 text-xs border border-gray-300 rounded"
                    />
                    <Button variant="outline" size="sm" onClick={handleAddEmail}>
                      Add
                    </Button>
                  </div>
                </div>

                <div className="border border-border rounded-lg p-4 text-center">
                  <Upload className="h-8 w-8 text-security-blue mx-auto mb-2" />
                  <h3 className="font-medium mb-2">Upload CSV File</h3>
                  <p className="text-sm text-muted-foreground mb-3">Upload a CSV with employee emails</p>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => navigate('/employees')}
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    Upload CSV
                  </Button>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="email-list">Target Email Addresses</Label>
                  <span className="text-sm text-muted-foreground">
                    {formData.targetEmails.length} email{formData.targetEmails.length !== 1 ? 's' : ''} added
                  </span>
                </div>
                
                {/* Bulk Email Input */}
                <div className="mt-2 mb-3">
                  <details className="group">
                    <summary className="cursor-pointer text-sm text-blue-600 hover:text-blue-800">
                      📝 Add Multiple Emails (Bulk Input)
                    </summary>
                    <div className="mt-2 p-3 border border-blue-200 rounded-lg bg-blue-50">
                      <Label className="text-sm text-blue-700">Paste multiple emails (comma or line separated)</Label>
                      <textarea
                        placeholder="user1@company.com, user2@company.com&#10;user3@company.com"
                        className="w-full mt-1 p-2 text-sm border border-gray-300 rounded resize-none h-20"
                        onBlur={(e) => {
                          const emails = e.target.value
                            .split(/[,\n]/)
                            .map(email => email.trim())
                            .filter(email => email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
                            .filter(email => !formData.targetEmails.includes(email));
                          
                          if (emails.length > 0) {
                            setFormData(prev => ({
                              ...prev,
                              targetEmails: [...prev.targetEmails, ...emails]
                            }));
                            e.target.value = '';
                          }
                        }}
                      />
                      <p className="text-xs text-blue-600 mt-1">
                        Separate emails with commas or new lines. Invalid emails will be ignored.
                      </p>
                    </div>
                  </details>
                </div>
                
                {/* Email Pills Container */}
                <div className="border border-border rounded-lg p-3 min-h-[100px] mt-1 bg-background">
                  {formData.targetEmails.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {formData.targetEmails.map((email, index) => (
                        <div 
                          key={index}
                          className="inline-flex items-center bg-security-blue/10 text-security-blue border border-security-blue/20 rounded-full px-3 py-1 text-sm"
                        >
                          <span>{email}</span>
                          <button
                            type="button"
                            onClick={() => handleRemoveEmail(email)}
                            className="ml-2 hover:bg-security-blue/20 rounded-full p-0.5 transition-colors"
                            aria-label={`Remove ${email}`}
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-4">
                      <Mail className="h-8 w-8 text-gray-300 mx-auto mb-2" />
                      <p className="text-muted-foreground text-sm mb-2">
                        No email addresses added yet
                      </p>
                      <p className="text-xs text-gray-500">
                        Add emails manually, select from employees, or upload CSV
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-end">
            <Button 
              type="button"
              variant="outline" 
              onClick={() => handleSubmit(true)}
              className="order-2 sm:order-1"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Saving...' : 'Save as Draft'}
            </Button>
            <Button 
              type="button"
              variant="security" 
              size="lg"
              className="order-1 sm:order-2"
              onClick={() => handleSubmit(false)}
              disabled={isSubmitting || formData.targetEmails.length === 0}
            >
              {isSubmitting ? '🚀 Launching...' : `🚀 Launch Campaign (${formData.targetEmails.length} targets)`}
            </Button>
          </div>
        </form>
      </div>

      {/* Template Preview Dialog */}
      <Dialog open={showPreviewDialog} onOpenChange={setShowPreviewDialog}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center">
              <Eye className="h-5 w-5 mr-2" />
              Template Preview
            </DialogTitle>
            <DialogDescription>
              Preview how this template will appear to recipients
            </DialogDescription>
          </DialogHeader>
          
          {previewTemplate && (
            <div className="space-y-6">
              {/* Email Header */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                      <Mail className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold">From: {previewTemplate.domain}</p>
                      <p className="text-sm text-gray-600">To: employee@company.com</p>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-red-600 border-red-200">
                    SIMULATION
                  </Badge>
                </div>
                <h3 className="font-bold text-lg">{previewTemplate.emailSubject}</h3>
              </div>
              
              {/* Email Content */}
              <div className="border rounded-lg p-6 bg-white">
                {previewTemplate.htmlContent ? (
                  <div 
                    className="space-y-4"
                    dangerouslySetInnerHTML={{ 
                      __html: previewTemplate.htmlContent.substring(
                        previewTemplate.htmlContent.indexOf('<body>') + 6,
                        previewTemplate.htmlContent.indexOf('</body>')
                      ) || previewTemplate.description
                    }}
                  />
                ) : (
                  <div className="space-y-4">
                    <p>Dear Employee,</p>
                    <p>{previewTemplate.description}</p>
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <div className="flex items-center space-x-2">
                        <AlertTriangle className="h-5 w-5 text-red-600" />
                        <p className="font-semibold text-red-800">Action Required</p>
                      </div>
                      <p className="text-red-700 mt-2">Please take immediate action to secure your account.</p>
                    </div>
                    <div className="text-center py-4">
                      <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                        Click Here to Verify
                      </Button>
                    </div>
                    <p className="text-sm text-gray-600">
                      If you have any questions, please contact our support team.
                    </p>
                  </div>
                )}
              </div>
              
              {/* Template Stats */}
              <div className="grid grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="text-center">
                  <p className="text-gray-600">Difficulty</p>
                  <p className="font-semibold text-blue-600">{previewTemplate.difficulty}</p>
                </div>
                <div className="text-center">
                  <p className="text-gray-600">Rating</p>
                  <p className="font-semibold text-yellow-600">{previewTemplate.rating} ⭐</p>
                </div>
                <div className="text-center">
                  <p className="text-gray-600">Success Rate</p>
                  <p className="font-semibold text-green-600">{previewTemplate.successRate}</p>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Employee Selection Dialog */}
      <Dialog open={showEmployeeDialog} onOpenChange={setShowEmployeeDialog}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center">
              <Users className="h-5 w-5 mr-2" />
              Select Target Employees
            </DialogTitle>
            <DialogDescription>
              Choose employees from your directory to target in this campaign
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Summary */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-800">
                {selectedEmployees.length} employees selected from {employees.length} total employees
              </p>
            </div>

            {/* Employee List */}
            <div className="border rounded-lg">
              <div className="max-h-96 overflow-y-auto">
                {employees.length === 0 ? (
                  <div className="p-8 text-center text-gray-500">
                    <Users className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p className="text-lg font-medium mb-2">No Employees Found</p>
                    <p>Go to Employee Management to add employees first.</p>
                  </div>
                ) : (
                  <div className="space-y-2 p-4">
                    {employees.map((employee) => (
                      <div 
                        key={employee.id}
                        className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
                        onClick={() => handleEmployeeToggle(employee)}
                      >
                        <Checkbox 
                          checked={selectedEmployees.find(emp => emp.id === employee.id) ? true : false}
                          onCheckedChange={() => handleEmployeeToggle(employee)}
                        />
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="font-medium">{employee.name}</p>
                              <p className="text-sm text-gray-600">{employee.email}</p>
                            </div>
                            <div className="text-right">
                              <Badge variant="outline" className="text-xs">
                                {employee.department}
                              </Badge>
                              <p className="text-xs text-gray-500 mt-1">{employee.position}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-between">
              <div className="flex space-x-2">
                <Button 
                  variant="outline" 
                  onClick={() => setSelectedEmployees(employees)}
                  disabled={employees.length === 0}
                >
                  Select All
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => setSelectedEmployees([])}
                  disabled={selectedEmployees.length === 0}
                >
                  Clear All
                </Button>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline" onClick={() => setShowEmployeeDialog(false)}>
                  Cancel
                </Button>
                <Button 
                  onClick={handleConfirmEmployeeSelection}
                  disabled={selectedEmployees.length === 0}
                >
                  Add {selectedEmployees.length} Employees
                </Button>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Success Dialog */}
      <SuccessDialog 
        open={showSuccessDialog}
        onClose={() => {
          setShowSuccessDialog(false);
          navigate('/dashboard');
        }}
        results={successResults}
      />
    </div>
  );
};

export default CreateCampaign;