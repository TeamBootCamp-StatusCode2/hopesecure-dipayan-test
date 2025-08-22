import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Mail, Shield, Globe, Settings, TestTube2, CheckCircle, AlertTriangle } from "lucide-react";

interface EmailConfiguration {
  mimic_domains: string[];
  spoofing_methods: string[];
  domain_examples: {
    homograph: string[];
    subdomain: string[];
    tld_variation: string[];
  };
}

interface DomainSettings {
  enableDomainSpoofing: boolean;
  targetDomain: string;
  spoofingMethod: 'homograph' | 'subdomain' | 'tld_variation';
  customDomain: string;
  senderName: string;
  senderEmail: string;
}

const EmailDomainConfiguration: React.FC = () => {
  const [emailConfig, setEmailConfig] = useState<EmailConfiguration | null>(null);
  const [domainSettings, setDomainSettings] = useState<DomainSettings>({
    enableDomainSpoofing: true,
    targetDomain: '',
    spoofingMethod: 'homograph',
    customDomain: '',
    senderName: 'IT Security Team',
    senderEmail: 'security@company.com'
  });
  const [generatedDomains, setGeneratedDomains] = useState<string[]>([]);
  const [testResult, setTestResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadEmailConfigurations();
  }, []);

  const loadEmailConfigurations = async () => {
    try {
      // This would be an API call in real implementation
      // const response = await fetch('/api/campaigns/email-configs/');
      // const data = await response.json();
      
      // Mock data for now
      const mockConfig: EmailConfiguration = {
        mimic_domains: [
          'gmaiI.com', 'gmai1.com', 'g-mail.com',
          'company-mail.com', 'corp-security.com',
          'bank-alert.com', 'secure-banking.net'
        ],
        spoofing_methods: ['homograph', 'subdomain', 'tld_variation'],
        domain_examples: {
          homograph: ['g00gle.com', 'microsft.com', 'arnazon.com'],
          subdomain: ['security.google-verify.com', 'login.microsoft-support.net'],
          tld_variation: ['gmail.net', 'outlook.org', 'facebook.co']
        }
      };
      
      setEmailConfig(mockConfig);
    } catch (error) {
      console.error('Failed to load email configurations:', error);
    }
  };

  const testDomainSpoofing = async () => {
    if (!domainSettings.targetDomain) return;
    
    setLoading(true);
    try {
      // This would be an API call in real implementation
      // const response = await fetch('/api/campaigns/test-spoofing/', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     target_domain: domainSettings.targetDomain,
      //     method: domainSettings.spoofingMethod
      //   })
      // });
      // const result = await response.json();
      
      // Mock domain generation logic
      const mockGeneration = generateMockDomains(domainSettings.targetDomain, domainSettings.spoofingMethod);
      
      setTestResult({
        target_domain: domainSettings.targetDomain,
        spoofing_method: domainSettings.spoofingMethod,
        generated_domains: mockGeneration
      });
      
      setGeneratedDomains(mockGeneration);
    } catch (error) {
      console.error('Failed to test domain spoofing:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateMockDomains = (domain: string, method: string): string[] => {
    const baseDomain = domain.split('.')[0];
    
    switch (method) {
      case 'homograph':
        return [
          domain.replace('o', '0'),
          domain.replace('i', '1'),
          domain.replace('l', 'I'),
          `${baseDomain.slice(0, -1)}${baseDomain.slice(-1) === 'e' ? '3' : 'e'}.com`
        ];
      case 'subdomain':
        return [
          `security.${baseDomain}-verify.com`,
          `login.${baseDomain}-support.net`,
          `notification.${baseDomain}-alert.org`
        ];
      case 'tld_variation':
        return [
          `${baseDomain}.net`,
          `${baseDomain}.org`,
          `${baseDomain}.co`,
          `${baseDomain}.info`
        ];
      default:
        return [];
    }
  };

  const saveDomainSettings = () => {
    // Save to localStorage or send to backend
    localStorage.setItem('email_domain_settings', JSON.stringify(domainSettings));
    
    // Show success message
    setTestResult({
      ...testResult,
      saved: true
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <Mail className="h-8 w-8 text-blue-600" />
        <div>
          <h2 className="text-3xl font-bold text-gray-800">Email Domain Configuration</h2>
          <p className="text-gray-600">Configure email spoofing and domain mimicking for phishing campaigns</p>
        </div>
      </div>

      <Tabs defaultValue="domain-spoofing" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="domain-spoofing" className="flex items-center gap-2">
            <Globe className="h-4 w-4" />
            Domain Spoofing
          </TabsTrigger>
          <TabsTrigger value="email-settings" className="flex items-center gap-2">
            <Settings className="h-4 w-4" />
            Email Settings
          </TabsTrigger>
          <TabsTrigger value="test-preview" className="flex items-center gap-2">
            <TestTube2 className="h-4 w-4" />
            Test & Preview
          </TabsTrigger>
        </TabsList>

        <TabsContent value="domain-spoofing">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Domain Spoofing Configuration
              </CardTitle>
              <CardDescription>
                Configure how emails will mimic legitimate domains to test employee awareness
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <Label className="text-sm font-medium">Enable Domain Spoofing</Label>
                  <p className="text-xs text-gray-500">Allow emails to mimic legitimate domains</p>
                </div>
                <Switch
                  checked={domainSettings.enableDomainSpoofing}
                  onCheckedChange={(checked) => 
                    setDomainSettings(prev => ({ ...prev, enableDomainSpoofing: checked }))
                  }
                />
              </div>

              {domainSettings.enableDomainSpoofing && (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="target-domain">Target Domain to Mimic</Label>
                      <Input
                        id="target-domain"
                        placeholder="e.g., google.com, microsoft.com"
                        value={domainSettings.targetDomain}
                        onChange={(e) => 
                          setDomainSettings(prev => ({ ...prev, targetDomain: e.target.value }))
                        }
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="spoofing-method">Spoofing Method</Label>
                      <Select
                        value={domainSettings.spoofingMethod}
                        onValueChange={(value: 'homograph' | 'subdomain' | 'tld_variation') =>
                          setDomainSettings(prev => ({ ...prev, spoofingMethod: value }))
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="homograph">Character Substitution (homograph)</SelectItem>
                          <SelectItem value="subdomain">Subdomain Spoofing</SelectItem>
                          <SelectItem value="tld_variation">TLD Variation</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="custom-domain">Custom Spoofed Domain (Optional)</Label>
                    <Input
                      id="custom-domain"
                      placeholder="Enter custom domain if not auto-generated"
                      value={domainSettings.customDomain}
                      onChange={(e) => 
                        setDomainSettings(prev => ({ ...prev, customDomain: e.target.value }))
                      }
                    />
                  </div>

                  <Button onClick={testDomainSpoofing} disabled={!domainSettings.targetDomain || loading}>
                    {loading ? 'Generating...' : 'Generate Spoofed Domains'}
                  </Button>

                  {generatedDomains.length > 0 && (
                    <div className="space-y-2">
                      <Label>Generated Spoofed Domains:</Label>
                      <div className="flex flex-wrap gap-2">
                        {generatedDomains.map((domain, index) => (
                          <Badge key={index} variant="outline" className="cursor-pointer hover:bg-gray-100">
                            {domain}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="email-settings">
          <Card>
            <CardHeader>
              <CardTitle>Email Sender Configuration</CardTitle>
              <CardDescription>
                Configure the sender information for phishing emails
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="sender-name">Sender Name</Label>
                  <Input
                    id="sender-name"
                    placeholder="e.g., IT Security Team"
                    value={domainSettings.senderName}
                    onChange={(e) => 
                      setDomainSettings(prev => ({ ...prev, senderName: e.target.value }))
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sender-email">Sender Email</Label>
                  <Input
                    id="sender-email"
                    placeholder="e.g., security@company.com"
                    value={domainSettings.senderEmail}
                    onChange={(e) => 
                      setDomainSettings(prev => ({ ...prev, senderEmail: e.target.value }))
                    }
                  />
                </div>
              </div>

              {emailConfig && (
                <div className="space-y-2">
                  <Label>Available Mimic Domains:</Label>
                  <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
                    {emailConfig.mimic_domains.map((domain, index) => (
                      <Badge 
                        key={index} 
                        variant="secondary" 
                        className="cursor-pointer hover:bg-blue-100"
                        onClick={() => setDomainSettings(prev => ({ 
                          ...prev, 
                          senderEmail: `${prev.senderEmail.split('@')[0]}@${domain}` 
                        }))}
                      >
                        {domain}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="test-preview">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TestTube2 className="h-5 w-5" />
                Test Configuration
              </CardTitle>
              <CardDescription>
                Preview how your spoofed emails will appear
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {testResult && (
                <Alert>
                  <CheckCircle className="h-4 w-4" />
                  <AlertDescription>
                    <div className="space-y-2">
                      <p><strong>Target Domain:</strong> {testResult.target_domain}</p>
                      <p><strong>Method:</strong> {testResult.spoofing_method}</p>
                      <p><strong>Generated Domains:</strong></p>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {testResult.generated_domains?.map((domain: string, index: number) => (
                          <Badge key={index} variant="outline">{domain}</Badge>
                        ))}
                      </div>
                    </div>
                  </AlertDescription>
                </Alert>
              )}

              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium mb-2">Email Preview:</h4>
                <div className="bg-white p-3 rounded border text-sm">
                  <p><strong>From:</strong> {domainSettings.senderName} &lt;{domainSettings.senderEmail}&gt;</p>
                  <p><strong>Subject:</strong> Security Alert: Action Required</p>
                  <p><strong>Domain Method:</strong> {domainSettings.spoofingMethod}</p>
                  {generatedDomains.length > 0 && (
                    <p><strong>Spoofed Domain:</strong> {generatedDomains[0]}</p>
                  )}
                </div>
              </div>

              <div className="flex gap-3">
                <Button onClick={saveDomainSettings} className="bg-green-600 hover:bg-green-700">
                  Save Configuration
                </Button>
                <Button variant="outline" onClick={testDomainSpoofing} disabled={loading}>
                  Test Again
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default EmailDomainConfiguration;
