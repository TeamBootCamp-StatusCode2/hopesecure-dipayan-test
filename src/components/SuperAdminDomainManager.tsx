import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Globe, 
  Plus, 
  Check, 
  X, 
  RefreshCw, 
  Settings, 
  BarChart3, 
  Server,
  Mail,
  Shield,
  Users,
  Eye,
  Trash2,
  AlertTriangle,
  CheckCircle,
  Copy
} from 'lucide-react';

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

interface DomainSuggestion {
  domain: string;
  type: string;
  description: string;
}

const SuperAdminDomainManager: React.FC = () => {
  const [allDomains, setAllDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null);
  const [dnsRecords, setDnsRecords] = useState<DNSRecord[]>([]);
  const [suggestions, setSuggestions] = useState<DomainSuggestion[]>([]);
  const [newDomainName, setNewDomainName] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);

  // Copy to clipboard with success message and fallback
  const copyToClipboard = async (text: string, label: string) => {
    try {
      // Try modern clipboard API first
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        setMessage({type: 'success', text: `${label} copied to clipboard!`});
      } else {
        // Fallback for HTTP or older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
          document.execCommand('copy');
          setMessage({type: 'success', text: `${label} copied to clipboard!`});
        } catch (err) {
          // If all fails, show the text to user
          prompt('Copy this text:', text);
          setMessage({type: 'success', text: `${label} displayed for manual copy`});
        }
        
        document.body.removeChild(textArea);
      }
      setTimeout(() => setMessage(null), 2000);
    } catch (error) {
      // Final fallback - show in prompt
      prompt('Copy this text:', text);
      setMessage({type: 'success', text: `${label} displayed for manual copy`});
      setTimeout(() => setMessage(null), 2000);
    }
  };

  // Fetch all domains across all organizations
  const fetchAllDomains = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/domains/api/domains/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Domains data:', data); // Debug log
        setAllDomains(data.domains || []);
      }
    } catch (error) {
      console.error('Error fetching domains:', error);
    }
  };

  // Fetch domain suggestions
  const fetchSuggestions = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/domains/api/domain-suggestions/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
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
    if (!newDomainName.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/domains/api/domains/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: newDomainName.trim(),
          domain_type: 'spoofing',
          verification_method: 'dns'
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setMessage({ type: 'success', text: 'Domain added successfully! Please verify DNS records.' });
        setNewDomainName('');
        fetchAllDomains();
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
      const response = await fetch(`http://127.0.0.1:8000/api/campaigns/domains/api/domains/${domainId}/verify/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (data.success) {
        setMessage({ 
          type: data.verification_result.domain_verified ? 'success' : 'error', 
          text: data.verification_result.domain_verified ? 'Domain verified successfully!' : 'Domain verification failed'
        });
        fetchAllDomains();
        if (selectedDomain?.id === domainId) {
          fetchDNSRecords(domainId);
        }
      } else {
        setMessage({ type: 'error', text: data.message });
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
      const response = await fetch(`http://127.0.0.1:8000/api/campaigns/domains/api/domains/${domainId}/dns_records/`, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('DNS Records data:', data); // Debug log
        setDnsRecords(data.dns_records || []);
      }
    } catch (error) {
      console.error('Error fetching DNS records:', error);
    }
  };

  // Delete domain
  const deleteDomain = async (domainId: number) => {
    if (!confirm('Are you sure you want to delete this domain? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/campaigns/domains/api/domains/${domainId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        setMessage({ type: 'success', text: 'Domain deleted successfully' });
        fetchAllDomains();
        if (selectedDomain?.id === domainId) {
          setSelectedDomain(null);
          setDnsRecords([]);
        }
      } else {
        setMessage({ type: 'error', text: 'Failed to delete domain' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error deleting domain' });
    } finally {
      setLoading(false);
    }
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
    const verified = allDomains.filter(d => d.status === 'verified').length;
    const pending = allDomains.filter(d => d.status === 'pending').length;
    const failed = allDomains.filter(d => d.status === 'failed').length;
    const totalEmails = allDomains.reduce((sum, d) => sum + d.emails_sent, 0);
    
    return { verified, pending, failed, totalEmails };
  };

  useEffect(() => {
    fetchAllDomains();
    fetchSuggestions();
  }, []);

  useEffect(() => {
    if (selectedDomain) {
      fetchDNSRecords(selectedDomain.id);
    }
  }, [selectedDomain]);

  const stats = getDomainStats();

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Globe className="h-8 w-8" />
          Super Admin - Domain DNS Management
        </h1>
        <p className="text-gray-600 mt-2">
          Manage all email domains across the platform for phishing simulation campaigns
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
                <p className="text-sm text-gray-600">Total Domains</p>
                <p className="text-2xl font-bold">{allDomains.length}</p>
              </div>
              <Globe className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Verified</p>
                <p className="text-2xl font-bold text-green-600">{stats.verified}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Pending</p>
                <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
              </div>
              <AlertTriangle className="h-8 w-8 text-yellow-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Emails</p>
                <p className="text-2xl font-bold">{stats.totalEmails}</p>
              </div>
              <Mail className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Domain List */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>All Platform Domains</span>
                <Badge variant="secondary">{allDomains.length}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {/* Add Domain Form */}
              <div className="flex gap-2 mb-4">
                <Input
                  placeholder="example.com"
                  value={newDomainName}
                  onChange={(e) => setNewDomainName(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addDomain()}
                />
                <Button 
                  onClick={addDomain} 
                  disabled={loading || !newDomainName.trim()}
                  size="sm"
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>

              {/* Domain List */}
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {allDomains.map((domain) => (
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
                          {domain.emails_sent} emails • {domain.created_by || 'System'}
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
                {allDomains.length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    No domains found
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Domain Suggestions */}
          <Card className="mt-4">
            <CardHeader>
              <CardTitle>Suggested Domains</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {suggestions.map((suggestion, index) => (
                  <div key={index} className="p-2 border rounded hover:bg-gray-50">
                    <p className="font-medium text-sm">{suggestion.domain}</p>
                    <p className="text-xs text-gray-500">{suggestion.description}</p>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => setNewDomainName(suggestion.domain)}
                      className="mt-1"
                    >
                      Use This Domain
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Domain Details */}
        <div className="lg:col-span-2">
          {selectedDomain ? (
            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="dns">DNS Records</TabsTrigger>
                <TabsTrigger value="analytics">Analytics</TabsTrigger>
              </TabsList>

              <TabsContent value="overview">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Globe className="h-5 w-5" />
                        {selectedDomain.name}
                      </div>
                      <div className="flex gap-2">
                        <Button
                          onClick={() => verifyDomain(selectedDomain.id)}
                          disabled={loading}
                          variant={selectedDomain.status === 'verified' ? 'default' : 'outline'}
                          size="sm"
                        >
                          {loading ? (
                            <RefreshCw className="h-4 w-4 animate-spin" />
                          ) : selectedDomain.status === 'verified' ? (
                            <Check className="h-4 w-4" />
                          ) : (
                            'Verify Domain'
                          )}
                        </Button>
                        <Button
                          onClick={() => deleteDomain(selectedDomain.id)}
                          variant="destructive"
                          size="sm"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-sm font-medium text-gray-600">Status</label>
                        <Badge className={`${getStatusColor(selectedDomain.status)} block w-fit mt-1`}>
                          {selectedDomain.status}
                        </Badge>
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
                        <p className="mt-1">{selectedDomain.created_by || 'System'}</p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-600">Organization</label>
                        <p className="mt-1">{selectedDomain.organization || 'System Domain'}</p>
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
                                  record.record_type === 'TXT' ? 'bg-green-100 text-green-800 font-medium' :
                                  record.record_type === 'CNAME' ? 'bg-orange-100 text-orange-800 font-medium' :
                                  'bg-blue-100 text-blue-800 font-medium'
                                }
                              >
                                {record.record_type}
                              </Badge>
                              <h3 className="font-semibold text-gray-900">
                                {record.name === '@' ? 'Root Domain (@)' : record.name}
                              </h3>
                            </div>
                            <div className="flex items-center gap-2">
                              {record.is_verified ? (
                                <Badge className="bg-green-100 text-green-800 border-green-200">
                                  <Check className="h-3 w-3 mr-1" />
                                  Verified
                                </Badge>
                              ) : (
                                <Badge className="bg-red-100 text-red-800 border-red-200">
                                  <X className="h-3 w-3 mr-1" />
                                  Not Verified
                                </Badge>
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
                                  <code className="bg-white px-3 py-2 rounded border font-mono text-sm flex-1">
                                    {record.name}
                                  </code>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0"
                                    onClick={() => copyToClipboard(record.name, 'Name/Host')}
                                  >
                                    <Copy className="h-3 w-3" />
                                  </Button>
                                </div>
                              </div>
                              
                              <div>
                                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">Value/Points to</label>
                                <div className="flex items-center gap-2 mt-1">
                                  <code className="bg-white px-3 py-2 rounded border font-mono text-sm flex-1 break-all">
                                    {record.value.length > 40 ? record.value.substring(0, 40) + '...' : record.value}
                                  </code>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0"
                                    onClick={() => copyToClipboard(record.value, 'Value')}
                                  >
                                    <Copy className="h-3 w-3" />
                                  </Button>
                                </div>
                              </div>
                            </div>

                            {/* Additional Fields */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                              {record.record_type === 'MX' && record.priority && (
                                <div>
                                  <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">Priority</label>
                                  <div className="flex items-center gap-2 mt-1">
                                    <code className="bg-white px-3 py-2 rounded border font-mono text-sm">
                                      {record.priority}
                                    </code>
                                    <Button
                                      size="sm"
                                      variant="ghost"
                                      className="h-8 w-8 p-0"
                                      onClick={() => copyToClipboard(record.priority?.toString() || '', 'Priority')}
                                    >
                                      <Copy className="h-3 w-3" />
                                    </Button>
                                  </div>
                                </div>
                              )}
                              
                              <div>
                                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">TTL</label>
                                <div className="flex items-center gap-2 mt-1">
                                  <code className="bg-white px-3 py-2 rounded border font-mono text-sm">
                                    {record.ttl}
                                  </code>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0"
                                    onClick={() => copyToClipboard(record.ttl.toString(), 'TTL')}
                                  >
                                    <Copy className="h-3 w-3" />
                                  </Button>
                                </div>
                              </div>
                            </div>

                            {/* Copy All Button */}
                            <div className="mt-4 pt-3 border-t border-gray-200">
                              <Button
                                onClick={() => {
                                  const recordText = `Type: ${record.record_type}\nName: ${record.name}\nValue: ${record.value}${record.priority ? `\nPriority: ${record.priority}` : ''}\nTTL: ${record.ttl}`;
                                  copyToClipboard(recordText, 'All record details');
                                }}
                                variant="outline"
                                size="sm"
                                className="w-full"
                              >
                                <Copy className="h-4 w-4 mr-2" />
                                Copy All Record Details
                              </Button>
                            </div>
                          </div>

                          {/* Full Value Display */}
                          {record.value.length > 40 && (
                            <div className="mt-3 p-2 bg-blue-50 border border-blue-200 rounded">
                              <label className="text-xs font-semibold text-blue-800 uppercase tracking-wider">Full Value:</label>
                              <code className="block mt-1 text-xs text-blue-700 break-all font-mono">
                                {record.value}
                              </code>
                            </div>
                          )}
                          
                          {record.verification_error && (
                            <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded">
                              <p className="text-sm text-red-700 font-medium">Verification Error:</p>
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
              <CardContent className="flex items-center justify-center h-64">
                <div className="text-center">
                  <Globe className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <p className="text-gray-500">Select a domain to view details</p>
                  <p className="text-sm text-gray-400 mt-2">
                    Add new domains or manage existing ones from the list
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default SuperAdminDomainManager;
