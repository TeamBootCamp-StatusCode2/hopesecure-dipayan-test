import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  Globe, 
  Plus, 
  Shield, 
  Check, 
  Copy, 
  Eye, 
  EyeOff, 
  Server, 
  Mail, 
  BarChart3, 
  Loader2,
  Trash2,
  CheckCircle,
  AlertCircle
} from "lucide-react";

interface Domain {
  id: number;
  name: string;
  type: string;
  status: string;
  emails_sent: number;
  success_rate: number;
  verified_at: string | null;
  created_at: string;
  created_by?: string;
  organization?: string;
}

interface DNSRecord {
  id: number;
  record_type: string;
  name: string;
  value: string;
  ttl: number;
  priority?: number;
  is_verified: boolean;
  verification_error?: string;
}

interface EmailAccount {
  id: number;
  username: string;
  email_address: string;
  account_type: string;
  status: string;
  emails_sent: number;
  created_at: string;
}

interface DomainSuggestion {
  domain: string;
  type: string;
  description: string;
}

interface Message {
  type: 'success' | 'error';
  text: string;
}

interface UserDomainManagerProps {
  organizationId?: string | null;
}

const UserDomainManager: React.FC<UserDomainManagerProps> = ({ organizationId }) => {
  console.log('UserDomainManager component mounted');
  
  const [domains, setDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null);
  const [dnsRecords, setDnsRecords] = useState<DNSRecord[]>([]);
  const [emailAccounts, setEmailAccounts] = useState<EmailAccount[]>([]);
  const [suggestions, setSuggestions] = useState<DomainSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<Message | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [newDomainName, setNewDomainName] = useState('');
  const [newDomainType, setNewDomainType] = useState('spoofing');
  const [newEmailUsername, setNewEmailUsername] = useState('');
  const [newEmailPassword, setNewEmailPassword] = useState('');
  const [newEmailType, setNewEmailType] = useState<'personal' | 'business' | 'campaign'>('campaign');
  const [activeTab, setActiveTab] = useState('overview');
  const [showValues, setShowValues] = useState<{ [key: number]: boolean }>({});

  // Fetch user domains (filtered by current user)
  const fetchDomains = async () => {
    console.log('=== FETCHING DOMAINS START ===');
    const token = localStorage.getItem('auth_token');
    console.log('Auth token exists:', !!token);
    console.log('Token (first 20 chars):', token?.substring(0, 20));
    console.log('Token length:', token?.length);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/domains/', {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      console.log('Response status:', response.status);
      console.log('Response statusText:', response.statusText);
      console.log('Response ok:', response.ok);
      
      if (response.ok) {
        const responseText = await response.text();
        console.log('Raw response text:', responseText);
        
        let data;
        try {
          data = JSON.parse(responseText);
        } catch (parseError) {
          console.error('JSON parse error:', parseError);
          return;
        }
        
        console.log('User Domains API Response:');
        console.log('- Full response:', JSON.stringify(data, null, 2));
        console.log('- Response.success:', data.success);
        console.log('- Response.domains:', data.domains);
        console.log('- Domains array type:', typeof data.domains);
        console.log('- Is domains an array:', Array.isArray(data.domains));
        console.log('- Array length:', data.domains ? data.domains.length : 'undefined');
        
        if (data.domains && Array.isArray(data.domains)) {
          console.log('- Individual domains:');
          data.domains.forEach((domain, index) => {
            console.log(`  Domain ${index}:`, JSON.stringify(domain, null, 2));
          });
        }
        
        console.log('- Setting domains to state...');
        setDomains(data.domains || []);
        
        // Check state after setting
        setTimeout(() => {
          console.log('- State check after 100ms: domains in state');
        }, 100);
        
      } else {
        const errorText = await response.text();
        console.error('Failed to fetch domains:', response.status, response.statusText);
        console.error('Error response:', errorText);
      }
    } catch (error) {
      console.error('Error fetching domains:', error);
      console.error('Error type:', typeof error);
      console.error('Error stack:', error instanceof Error ? error.stack : 'No stack');
    }
    console.log('=== FETCHING DOMAINS END ===');
  };

  // Fetch domain suggestions
  const fetchSuggestions = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/domains/suggestions/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setSuggestions(data.suggestions || []);
      }
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  // Add new domain
  const addDomain = async () => {
    if (!newDomainName.trim()) {
      setMessage({ type: 'error', text: 'Please enter a domain name' });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/domains/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: newDomainName,
          domain_type: newDomainType
        }),
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        setMessage({ type: 'success', text: 'Domain added successfully!' });
        setNewDomainName('');
        setShowAddForm(false);
        fetchDomains();
      } else {
        setMessage({ type: 'error', text: data.message || 'Failed to add domain' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error adding domain' });
    } finally {
      setLoading(false);
    }
  };

  // Verify domain
  const verifyDomain = async (domainId: number) => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/campaigns/domains/${domainId}/verify/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        setMessage({ type: 'success', text: 'Domain verification completed!' });
        fetchDomains();
        if (selectedDomain && selectedDomain.id === domainId) {
          fetchDNSRecords(domainId);
        }
      } else {
        setMessage({ type: 'error', text: data.message || 'Verification failed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error verifying domain' });
    } finally {
      setLoading(false);
    }
  };

  // Fetch DNS records for selected domain
  const fetchDNSRecords = async (domainId: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/campaigns/domains/${domainId}/dns_records/`, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('DNS Records data:', data);
        setDnsRecords(data.dns_records || []);
      }
    } catch (error) {
      console.error('Error fetching DNS records:', error);
    }
  };

  // Load email accounts for a domain
  const fetchEmailAccounts = async (domainId: string) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/email/accounts/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        // Filter accounts by domain if needed
        const domainAccounts = data.results ? 
          data.results.filter((account: any) => account.domain === parseInt(domainId)) : 
          data.filter((account: any) => account.domain === parseInt(domainId));
        
        setEmailAccounts(domainAccounts);
      } else {
        console.error('Failed to load email accounts:', response.status);
      }
    } catch (error) {
      console.error('Error loading email accounts:', error);
    }
  };

  // Create new email account
  const createEmailAccount = async () => {
    if (!selectedDomain || !newEmailUsername.trim()) {
      setMessage({ type: 'error', text: 'Please enter a username for the email account' });
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      console.log('Creating email account with:', {
        username: newEmailUsername,
        domain_id: selectedDomain.id,
        account_type: newEmailType,
        token: token ? 'Token present' : 'No token'
      });

      const response = await fetch('http://127.0.0.1:8000/api/email/accounts/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: newEmailUsername,
          domain_id: selectedDomain.id,
          account_type: newEmailType,
          auto_reply_enabled: false,
          auto_reply_message: ''
        }),
      });
      
      const data = await response.json();
      console.log('Email account creation response:', { status: response.status, data });
      
      if (response.ok) {
        setMessage({ type: 'success', text: `Email account ${newEmailUsername}@${selectedDomain.name} created successfully!` });
        setNewEmailUsername('');
        setNewEmailPassword('');
        setShowEmailForm(false);
        fetchEmailAccounts(selectedDomain.id.toString());
      } else {
        console.error('Email account creation failed:', data);
        setMessage({ type: 'error', text: data.message || data.error || JSON.stringify(data) });
      }
    } catch (error) {
      console.error('Email account creation error:', error);
      setMessage({ type: 'error', text: `Error creating email account: ${error.message}` });
    } finally {
      setLoading(false);
    }
  };

  // Delete email account
  const deleteEmailAccount = async (accountId: number) => {
    if (!confirm('Are you sure you want to delete this email account?')) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/email/accounts/${accountId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        setMessage({ type: 'success', text: 'Email account deleted successfully!' });
        if (selectedDomain) {
          fetchEmailAccounts(selectedDomain.id.toString());
        }
      } else {
        // Try to get error message if response has JSON content
        let errorMessage = 'Failed to delete email account';
        try {
          const data = await response.json();
          errorMessage = data.message || data.error || errorMessage;
        } catch {
          // Response body is empty or not JSON, use default message
        }
        setMessage({ type: 'error', text: errorMessage });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error deleting email account' });
    } finally {
      setLoading(false);
    }
  };

  // Delete domain
  const deleteDomain = async (domainId: number) => {
    if (!confirm('Are you sure you want to delete this domain? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/campaigns/domains/${domainId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        setMessage({ type: 'success', text: 'Domain deleted successfully!' });
        setSelectedDomain(null);
        setDnsRecords([]);
        fetchDomains();
      } else {
        setMessage({ type: 'error', text: data.message || 'Failed to delete domain' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error deleting domain' });
    } finally {
      setLoading(false);
    }
  };

  // Copy to clipboard
  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setMessage({ type: 'success', text: `${label} copied to clipboard!` });
    });
  };

  // Toggle value visibility
  const toggleValueVisibility = (recordId: number) => {
    setShowValues(prev => ({
      ...prev,
      [recordId]: !prev[recordId]
    }));
  };

  // Get status badge color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'verified': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // Get domain statistics
  const getDomainStats = () => {
    const verified = domains.filter(d => d.status === 'verified').length;
    const pending = domains.filter(d => d.status === 'pending').length;
    const failed = domains.filter(d => d.status === 'failed').length;
    const totalEmails = domains.reduce((sum, d) => sum + d.emails_sent, 0);
    
    return { verified, pending, failed, totalEmails };
  };

  useEffect(() => {
    console.log('UserDomainManager useEffect triggered - loading domains and suggestions');
    
    // Debug token
    const token = localStorage.getItem('auth_token');
    console.log('=== TOKEN DEBUG ===');
    console.log('Token exists:', !!token);
    console.log('Token length:', token?.length);
    console.log('Token (first 30 chars):', token?.substring(0, 30));
    console.log('Expected tokens:');
    console.log('  Superadmin: 7de217ae126053a2a87a58d7e3772ab5bccff824');
    console.log('  Shuvo: 2a2dc81b9f4387305167941eb034cf22034a6337');
    
    // Check if token is valid
    const validTokens = [
      '7de217ae126053a2a87a58d7e3772ab5bccff824', // superadmin
      '2a2dc81b9f4387305167941eb034cf22034a6337', // shuvo
      '8a9982d673c147c55bbd9dc3922eb75155b25c7e', // speed
      'c72f906194b7858120e6d5a7eb5bf13e13100aa8', // pou
    ];
    
    if (!validTokens.includes(token || '')) {
      console.log('⚠️ INVALID TOKEN! Please set a valid token in browser console:');
      console.log('localStorage.setItem("auth_token", "2a2dc81b9f4387305167941eb034cf22034a6337")');
    } else {
      console.log('✅ Valid token found');
    }
    
    fetchDomains();
    fetchSuggestions();
  }, []);

  useEffect(() => {
    console.log('Domains state changed:', domains);
  }, [domains]);

  useEffect(() => {
    if (selectedDomain) {
      fetchDNSRecords(selectedDomain.id);
      fetchEmailAccounts(selectedDomain.id.toString());
    }
  }, [selectedDomain]);

  const stats = getDomainStats();

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Globe className="h-8 w-8" />
          Organization Domain & Email Management
        </h1>
        <p className="text-gray-600 mt-2">
          Manage your organization's email domains and DNS settings for phishing simulation campaigns
        </p>
      </div>

      {message && (
        <Alert className={`mb-4 ${message.type === 'success' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
          <AlertDescription className={message.type === 'success' ? 'text-green-800' : 'text-red-800'}>
            {message.text}
          </AlertDescription>
        </Alert>
      )}

      {/* Statistics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-bold text-green-600">{stats.verified}</p>
                <p className="text-xs text-gray-500">Verified Domains</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
                <p className="text-xs text-gray-500">Pending Verification</p>
              </div>
              <AlertCircle className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-bold text-red-600">{stats.failed}</p>
                <p className="text-xs text-gray-500">Failed Domains</p>
              </div>
              <AlertCircle className="h-8 w-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-bold text-blue-600">{stats.totalEmails}</p>
                <p className="text-xs text-gray-500">Total Emails Sent</p>
              </div>
              <Mail className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Domain List */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5" />
                  Organization Domains ({domains.length})
                </CardTitle>
                <Button 
                  size="sm" 
                  onClick={() => setShowAddForm(!showAddForm)}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  <Plus className="h-4 w-4 mr-1" />
                  Add Domain
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {/* Add Domain Form */}
              {showAddForm && (
                <div className="mb-4 p-4 border rounded-lg bg-gray-50">
                  <div className="space-y-3">
                    <Input
                      placeholder="example.com"
                      value={newDomainName}
                      onChange={(e) => setNewDomainName(e.target.value)}
                      className="w-full"
                    />
                    <Select value={newDomainType} onValueChange={setNewDomainType}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="spoofing">Spoofing Domain</SelectItem>
                        <SelectItem value="phishing">Phishing Domain</SelectItem>
                        <SelectItem value="legitimate">Legitimate Domain</SelectItem>
                      </SelectContent>
                    </Select>
                    <div className="flex gap-2">
                      <Button 
                        onClick={addDomain} 
                        disabled={loading}
                        className="flex-1"
                      >
                        {loading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                        Add Domain
                      </Button>
                      <Button 
                        variant="outline" 
                        onClick={() => setShowAddForm(false)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                </div>
              )}

              {/* Domain List */}
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {domains.map((domain) => (
                  <div
                    key={domain.id}
                    className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                      selectedDomain?.id === domain.id ? 'border-blue-500 bg-blue-50' : 'hover:bg-gray-50'
                    }`}
                    onClick={() => setSelectedDomain(domain)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">{domain.name}</p>
                        <p className="text-sm text-gray-500">
                          {domain.emails_sent} emails • {domain.created_by || 'You'}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={getStatusColor(domain.status)}>
                          {domain.status}
                        </Badge>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteDomain(domain.id);
                          }}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
                {domains.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <Globe className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>No organization domains found</p>
                    <p className="text-sm">Add your organization's first domain to get started</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Domain Suggestions */}
          {suggestions.length > 0 && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle className="text-lg">💡 Suggested Domains</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {suggestions.slice(0, 3).map((suggestion, index) => (
                    <div key={index} className="p-3 border rounded-lg bg-gray-50">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium">{suggestion.domain}</p>
                          <p className="text-sm text-gray-500">{suggestion.description}</p>
                        </div>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => {
                            setNewDomainName(suggestion.domain);
                            setNewDomainType(suggestion.type);
                            setShowAddForm(true);
                          }}
                        >
                          Use
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Domain Details */}
        <div className="lg:col-span-2">
          {selectedDomain ? (
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="emails">Email Accounts</TabsTrigger>
                <TabsTrigger value="dns">DNS Records</TabsTrigger>
                <TabsTrigger value="analytics">Analytics</TabsTrigger>
              </TabsList>

              <TabsContent value="overview">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Globe className="h-5 w-5" />
                      Domain Overview
                    </CardTitle>
                    <div className="flex items-center gap-2">
                      <Badge className={getStatusColor(selectedDomain.status)}>
                        {selectedDomain.status}
                      </Badge>
                      <Button 
                        size="sm" 
                        onClick={() => verifyDomain(selectedDomain.id)}
                        disabled={loading}
                      >
                        {loading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                        Verify DNS
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="text-sm font-medium text-gray-600">Domain Name</label>
                        <p className="mt-1 text-lg font-semibold">{selectedDomain.name}</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Type</label>
                        <p className="mt-1">{selectedDomain.type}</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Emails Sent</label>
                        <p className="mt-1">{selectedDomain.emails_sent}</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Success Rate</label>
                        <p className="mt-1">{selectedDomain.success_rate}%</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Created By</label>
                        <p className="mt-1">{selectedDomain.created_by || 'Organization Member'}</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Organization</label>
                        <p className="mt-1">{selectedDomain.organization || 'Your Organization'}</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Created</label>
                        <p className="mt-1">{new Date(selectedDomain.created_at).toLocaleDateString()}</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Verified</label>
                        <p className="mt-1">
                          {selectedDomain.verified_at 
                            ? new Date(selectedDomain.verified_at).toLocaleDateString()
                            : 'Not verified'
                          }
                        </p>
                      </div>
                    </div>

                    {/* Quick Actions */}
                    <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <h3 className="font-medium text-blue-900 mb-3">Quick Actions for Phishing Campaigns</h3>
                      <div className="flex gap-3">
                        <Button 
                          size="sm"
                          onClick={() => setActiveTab('emails')}
                          className="bg-green-600 hover:bg-green-700"
                        >
                          <Mail className="h-4 w-4 mr-2" />
                          Create Email Account
                        </Button>
                        <Button 
                          size="sm"
                          variant="outline"
                          onClick={() => setActiveTab('dns')}
                        >
                          <Server className="h-4 w-4 mr-2" />
                          Manage DNS
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="emails">
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2">
                        <Mail className="h-5 w-5" />
                        Email Accounts
                      </CardTitle>
                      <Button 
                        size="sm" 
                        onClick={() => setShowEmailForm(!showEmailForm)}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <Plus className="h-4 w-4 mr-1" />
                        Create Email
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    {/* Create Email Form */}
                    {showEmailForm && (
                      <div className="mb-6 p-4 border rounded-lg bg-green-50">
                        <h3 className="font-medium mb-3">Create New Email Account</h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                          <div>
                            <label className="text-sm font-medium text-gray-600">Username</label>
                            <Input
                              placeholder="admin, support, security..."
                              value={newEmailUsername}
                              onChange={(e) => setNewEmailUsername(e.target.value)}
                              className="mt-1"
                            />
                          </div>
                          <div>
                            <label className="text-sm font-medium text-gray-600">Password</label>
                            <Input
                              type="password"
                              placeholder="Enter password for email account"
                              value={newEmailPassword}
                              onChange={(e) => setNewEmailPassword(e.target.value)}
                              className="mt-1"
                            />
                          </div>
                          <div>
                            <label className="text-sm font-medium text-gray-600">Type</label>
                            <Select 
                              value={newEmailType} 
                              onValueChange={(value) => setNewEmailType(value as 'personal' | 'business' | 'campaign')}
                            >
                              <SelectTrigger className="mt-1">
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="admin">Admin</SelectItem>
                                <SelectItem value="support">Support</SelectItem>
                                <SelectItem value="security">Security</SelectItem>
                                <SelectItem value="noreply">No Reply</SelectItem>
                                <SelectItem value="custom">Custom</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                          <div className="flex items-end">
                            <Button 
                              onClick={createEmailAccount} 
                              disabled={loading}
                              className="w-full"
                            >
                              {loading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                              Create
                            </Button>
                          </div>
                        </div>
                        <div className="mt-3 text-sm text-gray-600">
                          Email will be created as: <strong>{newEmailUsername || 'username'}@{selectedDomain.name}</strong>
                        </div>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => setShowEmailForm(false)}
                          className="mt-3"
                        >
                          Cancel
                        </Button>
                      </div>
                    )}

                    {/* Email Accounts List */}
                    <div className="space-y-3">
                      {emailAccounts.map((account) => (
                        <div key={account.id} className="border rounded-lg p-4 bg-white">
                          <div className="flex items-center justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-3">
                                <Mail className="h-5 w-5 text-blue-600" />
                                <div>
                                  <p className="font-medium text-lg">{account.email_address}</p>
                                  <div className="flex items-center gap-4 text-sm text-gray-500">
                                    <span>Type: {account.account_type}</span>
                                    <span>Status: {account.status}</span>
                                    <span>Emails sent: {account.emails_sent}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              <Badge className={
                                account.status === 'active' ? 'bg-green-100 text-green-800' :
                                account.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                                'bg-red-100 text-red-800'
                              }>
                                {account.status}
                              </Badge>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => {
                                  navigator.clipboard.writeText(account.email_address);
                                  setMessage({ type: 'success', text: 'Email address copied to clipboard!' });
                                }}
                              >
                                <Copy className="h-4 w-4 mr-1" />
                                Copy
                              </Button>
                              <Button
                                size="sm"
                                variant="ghost"
                                onClick={() => deleteEmailAccount(account.id)}
                                className="text-red-600 hover:text-red-800"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                          
                          {/* Usage Info */}
                          <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                              <div>
                                <span className="text-gray-600">Created:</span>
                                <p className="font-medium">{new Date(account.created_at).toLocaleDateString()}</p>
                              </div>
                              <div>
                                <span className="text-gray-600">Emails Sent:</span>
                                <p className="font-medium">{account.emails_sent}</p>
                              </div>
                              <div>
                                <span className="text-gray-600">Account Type:</span>
                                <p className="font-medium capitalize">{account.account_type}</p>
                              </div>
                              <div>
                                <span className="text-gray-600">Use in Campaign:</span>
                                <Button size="sm" className="mt-1">
                                  Use This Email
                                </Button>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                      
                      {emailAccounts.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                          <Mail className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                          <p>No email accounts found for this domain</p>
                          <p className="text-sm">Create your first email account to start sending campaigns</p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="dns">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Server className="h-5 w-5" />
                      DNS Records
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {dnsRecords.map((record) => (
                        <div key={record.id} className="border rounded-lg p-4 bg-white">
                          {/* Header with Type Badge and Status */}
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center gap-3">
                              <Badge 
                                variant="outline" 
                                className={
                                  record.record_type === 'MX' ? 'bg-purple-100 text-purple-800 font-medium' :
                                  record.record_type === 'TXT' ? 'bg-blue-100 text-blue-800 font-medium' :
                                  record.record_type === 'CNAME' ? 'bg-green-100 text-green-800 font-medium' :
                                  'bg-gray-100 text-gray-800 font-medium'
                                }
                              >
                                {record.record_type}
                              </Badge>
                              {record.priority && (
                                <Badge variant="outline" className="text-xs">
                                  Priority: {record.priority}
                                </Badge>
                              )}
                            </div>
                            
                            <div className="flex items-center gap-2">
                              {record.is_verified ? (
                                <div className="flex items-center gap-1 text-green-600">
                                  <Check className="h-4 w-4" />
                                  <span className="text-sm font-medium">Verified</span>
                                </div>
                              ) : (
                                <div className="flex items-center gap-1 text-red-600">
                                  <AlertCircle className="h-4 w-4" />
                                  <span className="text-sm font-medium">Not Verified</span>
                                </div>
                              )}
                            </div>
                          </div>
                          
                          {/* DNS Record Details */}
                          <div className="bg-gray-50 rounded-lg p-4">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                              <div>
                                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">Type</label>
                                <div className="flex items-center gap-2 mt-1">
                                  <code className="bg-white px-3 py-2 rounded border font-mono text-sm">
                                    {record.record_type}
                                  </code>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0"
                                    onClick={() => copyToClipboard(record.record_type, 'Record Type')}
                                  >
                                    <Copy className="h-3 w-3" />
                                  </Button>
                                </div>
                              </div>
                              
                              <div>
                                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">Name/Host</label>
                                <div className="flex items-center gap-2 mt-1">
                                  <code className="bg-white px-3 py-2 rounded border font-mono text-sm break-all">
                                    {record.name}
                                  </code>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0"
                                    onClick={() => copyToClipboard(record.name, 'Record Name')}
                                  >
                                    <Copy className="h-3 w-3" />
                                  </Button>
                                </div>
                              </div>
                              
                              <div>
                                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">Value</label>
                                <div className="flex items-center gap-2 mt-1">
                                  <code className="bg-white px-3 py-2 rounded border font-mono text-sm break-all flex-1">
                                    {showValues[record.id] ? record.value : '••••••••••••••••'}
                                  </code>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0"
                                    onClick={() => toggleValueVisibility(record.id)}
                                  >
                                    {showValues[record.id] ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0"
                                    onClick={() => copyToClipboard(record.value, 'Record Value')}
                                  >
                                    <Copy className="h-3 w-3" />
                                  </Button>
                                </div>
                              </div>
                            </div>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                              <div>
                                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">TTL</label>
                                <div className="flex items-center gap-2 mt-1">
                                  <code className="bg-white px-3 py-2 rounded border font-mono text-sm">
                                    {record.ttl}
                                  </code>
                                  <span className="text-xs text-gray-500">seconds</span>
                                </div>
                              </div>
                              
                              {record.priority && (
                                <div>
                                  <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">Priority</label>
                                  <div className="flex items-center gap-2 mt-1">
                                    <code className="bg-white px-3 py-2 rounded border font-mono text-sm">
                                      {record.priority}
                                    </code>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                          
                          {/* Verification Error */}
                          {record.verification_error && (
                            <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                              <p className="text-sm text-red-600 mt-1">{record.verification_error}</p>
                            </div>
                          )}
                        </div>
                      ))}
                      {dnsRecords.length === 0 && (
                        <p className="text-gray-500 text-center py-4">
                          No DNS records found
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="analytics">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Domain Analytics
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <Mail className="h-8 w-8 mx-auto mb-2 text-blue-600" />
                        <p className="text-2xl font-bold">{selectedDomain.emails_sent}</p>
                        <p className="text-sm text-gray-600">Emails Sent</p>
                      </div>
                      <div className="text-center">
                        <Shield className="h-8 w-8 mx-auto mb-2 text-green-600" />
                        <p className="text-2xl font-bold">{selectedDomain.success_rate}%</p>
                        <p className="text-sm text-gray-600">Success Rate</p>
                      </div>
                      <div className="text-center">
                        <Check className="h-8 w-8 mx-auto mb-2 text-purple-600" />
                        <p className="text-2xl font-bold">
                          {selectedDomain.status === 'verified' ? 'Yes' : 'No'}
                        </p>
                        <p className="text-sm text-gray-600">Verified</p>
                      </div>
                      <div className="text-center">
                        <Globe className="h-8 w-8 mx-auto mb-2 text-orange-600" />
                        <p className="text-2xl font-bold">{selectedDomain.type}</p>
                        <p className="text-sm text-gray-600">Domain Type</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          ) : (
            <Card>
              <CardContent className="text-center py-12">
                <Globe className="h-16 w-16 mx-auto mb-4 text-gray-300" />
                <h3 className="text-lg font-semibold text-gray-600 mb-2">No Domain Selected</h3>
                <p className="text-gray-500">Select a domain from the list to view its details and manage DNS records</p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserDomainManager;
