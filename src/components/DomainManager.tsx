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
  Shield
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

const DomainManager: React.FC = () => {
  const [domains, setDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null);
  const [dnsRecords, setDnsRecords] = useState<DNSRecord[]>([]);
  const [newDomainName, setNewDomainName] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);

  // Fetch user's domains
  const fetchDomains = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/campaigns/domains/api/domains/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setDomains(data.domains || []);
      }
    } catch (error) {
      console.error('Error fetching domains:', error);
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
        fetchDomains();
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
        setDnsRecords(data.dns_records || []);
      }
    } catch (error) {
      console.error('Error fetching DNS records:', error);
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

  useEffect(() => {
    fetchDomains();
  }, []);

  useEffect(() => {
    if (selectedDomain) {
      fetchDNSRecords(selectedDomain.id);
    }
  }, [selectedDomain]);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Globe className="h-8 w-8" />
          Domain Management
        </h1>
        <p className="text-gray-600 mt-2">
          Manage email domains for phishing simulation campaigns
        </p>
      </div>

      {message && (
        <Alert className={`mb-4 ${message.type === 'success' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
          <AlertDescription className={message.type === 'success' ? 'text-green-800' : 'text-red-800'}>
            {message.text}
          </AlertDescription>
        </Alert>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Domain List */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Your Domains</span>
                <Badge variant="secondary">{domains.length}</Badge>
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
              <div className="space-y-2">
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
                          {domain.emails_sent} emails sent
                        </p>
                      </div>
                      <Badge className={getStatusColor(domain.status)}>
                        {domain.status}
                      </Badge>
                    </div>
                  </div>
                ))}
                {domains.length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    No domains added yet
                  </p>
                )}
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
                      <Button
                        onClick={() => verifyDomain(selectedDomain.id)}
                        disabled={loading}
                        variant={selectedDomain.status === 'verified' ? 'default' : 'outline'}
                      >
                        {loading ? (
                          <RefreshCw className="h-4 w-4 animate-spin" />
                        ) : selectedDomain.status === 'verified' ? (
                          <Check className="h-4 w-4" />
                        ) : (
                          'Verify Domain'
                        )}
                      </Button>
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
                        <div key={record.id} className="border rounded-lg p-3">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <Badge variant="outline">{record.record_type}</Badge>
                              <div>
                                <p className="font-medium">{record.name}</p>
                                <p className="text-sm text-gray-500 truncate max-w-md">
                                  {record.value}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              {record.is_verified ? (
                                <Check className="h-4 w-4 text-green-600" />
                              ) : (
                                <X className="h-4 w-4 text-red-600" />
                              )}
                            </div>
                          </div>
                          {record.verification_error && (
                            <p className="text-sm text-red-600 mt-2">
                              {record.verification_error}
                            </p>
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
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default DomainManager;
