import React, { useState, useEffect } from 'react';
import { Mail, ChevronDown, CheckCircle, Globe } from 'lucide-react';

interface EmailAccount {
  id: number;
  email_address: string;
  account_type: string;
  status: string;
  domain_name: string;
}

interface Domain {
  id: number;
  name: string;
  status: string;
}

interface SelectedEmailInfo {
  email: string;
  domain: string;
  accountId: number;
}

interface EmailSelectorProps {
  onEmailSelect?: (selectedEmail: SelectedEmailInfo | null) => void;
  selectedEmail?: SelectedEmailInfo | null;
}

const EmailSelector: React.FC<EmailSelectorProps> = ({ onEmailSelect, selectedEmail }) => {
  const [availableDomains, setAvailableDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<string>('');
  const [availableEmails, setAvailableEmails] = useState<EmailAccount[]>([]);
  const [localSelectedEmail, setLocalSelectedEmail] = useState<string>('');
  const [loading, setLoading] = useState(true);

  // Handle email selection and call parent callback
  const handleEmailSelection = (email: EmailAccount) => {
    setLocalSelectedEmail(email.email_address);
    if (onEmailSelect) {
      onEmailSelect({
        email: email.email_address,
        domain: email.domain_name,
        accountId: email.id
      });
    }
  };

  // Get current selected email (from props or local state)
  const currentSelectedEmail = selectedEmail?.email || localSelectedEmail;

  // Account type display mapping
  const accountTypeLabels = {
    'admin': '👤 Admin',
    'support': '🎧 Support', 
    'security': '🔒 Security',
    'noreply': '📧 No Reply',
    'custom': '⚙️ Custom'
  };

  useEffect(() => {
    loadAvailableDomains();
  }, []);

  useEffect(() => {
    if (selectedDomain) {
      loadEmailsForDomain(selectedDomain);
    } else {
      setAvailableEmails([]);
    }
  }, [selectedDomain]);

  const loadAvailableDomains = async () => {
    try {
      const authToken = localStorage.getItem('auth_token');
      console.log('Auth Token:', authToken ? 'Found' : 'Not found');
      
      const response = await fetch('http://localhost:8000/api/email/domains/available_domains/', {
        headers: {
          'Authorization': `Token ${authToken}`,
          'Content-Type': 'application/json'
        }
      });
      
      console.log('Domains API Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Domains loaded:', data);
        setAvailableDomains(data);
        
        // Auto-select first domain if available
        if (data.length > 0) {
          setSelectedDomain(data[0].id.toString());
        }
      } else {
        const errorText = await response.text();
        console.error('Domains API Error:', response.status, errorText);
        // Show error message in UI
        setAvailableDomains([]);
      }
    } catch (error) {
      console.error('Error loading domains:', error);
      // Fallback: Add manual domains for testing
      setAvailableDomains([
        { id: 2, name: 'hopesecure.tech', status: 'verified' },
        { id: 3, name: 'phishing-security.com', status: 'verified' }
      ]);
    }
    setLoading(false);
  };

  const loadEmailsForDomain = async (domainId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/email/accounts/?domain=${domainId}`, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        const emailAccounts = data.results || data;
        setAvailableEmails(emailAccounts);
        
        // Auto-select first email if available
        if (emailAccounts.length > 0) {
        const firstAccount = emailAccounts[0];
        setLocalSelectedEmail(firstAccount.email_address);
        // Auto-select first email if no email is already selected
        if (!selectedEmail && onEmailSelect) {
          onEmailSelect({
            email: firstAccount.email_address,
            domain: firstAccount.domain_name,
            accountId: firstAccount.id
          });
        }
      }
      }
    } catch (error) {
      console.error('Error loading emails:', error);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <div className="text-gray-600">Loading email options...</div>
      </div>
    );
  }

  if (availableDomains.length === 0) {
    return (
      <div className="text-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <Globe className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Domains Available</h3>
        <p className="text-gray-600 mb-4">
          Your organization hasn't set up any email domains yet.
        </p>
        <p className="text-sm text-gray-500">
          Contact your admin to set up domains and email accounts.
        </p>
        <div className="mt-4 text-xs text-gray-400">
          Debug: Check browser console for API errors
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-medium text-gray-900">📧 Select Sender Email</h3>
      
      {/* Domain Selector */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Domain
        </label>
        <div className="relative">
          <select
            value={selectedDomain}
            onChange={(e) => setSelectedDomain(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none"
          >
            <option value="">Choose a domain...</option>
            {availableDomains.map((domain) => (
              <option key={domain.id} value={domain.id}>
                🌐 {domain.name} ({domain.status})
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
        </div>
      </div>

      {/* Email Selector */}
      {selectedDomain && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Email Account
          </label>
          
          {availableEmails.length === 0 ? (
            <div className="text-center py-6 bg-yellow-50 rounded-lg border border-yellow-200">
              <Mail className="mx-auto h-8 w-8 text-yellow-500 mb-2" />
              <p className="text-yellow-700 font-medium">No Email Accounts Available</p>
              <p className="text-yellow-600 text-sm mt-1">
                Contact your admin to create email accounts for this domain.
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {availableEmails.map((email) => (
                <div
                  key={email.id}
                  onClick={() => handleEmailSelection(email)}
                  className={`p-4 border rounded-lg cursor-pointer transition-all ${
                    currentSelectedEmail === email.email_address
                      ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-lg ${
                        currentSelectedEmail === email.email_address ? 'bg-blue-100' : 'bg-gray-100'
                      }`}>
                        <Mail className={`h-5 w-5 ${
                          currentSelectedEmail === email.email_address ? 'text-blue-600' : 'text-gray-600'
                        }`} />
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">
                          {email.email_address}
                        </div>
                        <div className="text-sm text-gray-500">
                          {accountTypeLabels[email.account_type as keyof typeof accountTypeLabels] || email.account_type}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        email.status === 'active' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {email.status}
                      </span>
                      
                      {currentSelectedEmail === email.email_address && (
                        <CheckCircle className="h-5 w-5 text-blue-600" />
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Export for use in campaign creation
export const useSelectedEmail = () => {
  const [selectedEmail, setSelectedEmail] = useState<string>('');
  
  return {
    selectedEmail,
    setSelectedEmail,
    EmailSelectorComponent: EmailSelector
  };
};

export default EmailSelector;
