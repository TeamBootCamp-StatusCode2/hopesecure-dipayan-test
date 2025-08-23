import React, { useState, useEffect } from 'react';
import { Plus, Mail, Settings, Send, Users, Globe, Inbox } from 'lucide-react';

interface EmailAccount {
  id: number;
  email_address: string;
  account_type: string;
  status: string;
  emails_sent: number;
  emails_received: number;
  created_at: string;
  domain_name: string;
}

interface EmailDomain {
  id: number;
  name: string;
  status: string;
  emails_sent: number;
}

const EmailDashboard: React.FC = () => {
  const [emailAccounts, setEmailAccounts] = useState<EmailAccount[]>([]);
  const [availableDomains, setAvailableDomains] = useState<EmailDomain[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  
  // Create account form state
  const [createForm, setCreateForm] = useState({
    username: '',
    domain_id: '',
    account_type: 'admin'
  });

  const accountTypes = [
    { value: 'admin', label: '👤 Admin', desc: 'Administrative emails' },
    { value: 'support', label: '🎧 Support', desc: 'Customer support' },
    { value: 'security', label: '🔒 Security', desc: 'Security notifications' },
    { value: 'noreply', label: '📧 No Reply', desc: 'Automated emails' },
    { value: 'custom', label: '⚙️ Custom', desc: 'Custom purpose' }
  ];

  // Load data on component mount
  useEffect(() => {
    loadEmailAccounts();
    loadAvailableDomains();
  }, []);

  const loadEmailAccounts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/email/accounts/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setEmailAccounts(data.results || data);
      }
    } catch (error) {
      console.error('Error loading email accounts:', error);
    }
  };

  const loadAvailableDomains = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/email/domains/available_domains/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setAvailableDomains(data);
      }
    } catch (error) {
      console.error('Error loading domains:', error);
    }
    setLoading(false);
  };

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/email/accounts/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(createForm)
      });

      if (response.ok) {
        alert('✅ Email account created successfully!');
        setShowCreateForm(false);
        setCreateForm({ username: '', domain_id: '', account_type: 'admin' });
        loadEmailAccounts();
      } else {
        const error = await response.json();
        alert(`❌ Error: ${error.detail || 'Failed to create account'}`);
      }
    } catch (error) {
      alert(`❌ Error creating account: ${error}`);
    }
  };

  const sendTestEmail = async (accountId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/email/accounts/${accountId}/send_test_email/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });

      const result = await response.json();
      if (result.success) {
        alert(`✅ ${result.message}`);
        loadEmailAccounts(); // Refresh to update stats
      } else {
        alert(`❌ ${result.message}`);
      }
    } catch (error) {
      alert(`❌ Error sending test email: ${error}`);
    }
  };

  const quickSetupDomain = async (domainId: number) => {
    try {
      const response = await fetch('http://localhost:8000/api/email/domains/quick_setup/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          domain_id: domainId,
          account_types: ['admin', 'support', 'security']
        })
      });

      const result = await response.json();
      if (result.success) {
        alert(`✅ ${result.message}\n\nCreated accounts:\n${result.accounts.map((acc: any) => `• ${acc.email}`).join('\n')}`);
        loadEmailAccounts();
      } else {
        alert(`❌ ${result.message}`);
      }
    } catch (error) {
      alert(`❌ Error with quick setup: ${error}`);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading email management...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">📧 Email Management</h1>
          <p className="text-gray-600">Manage your domain email accounts</p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus size={20} />
          Create Email Account
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center gap-3">
            <Mail className="text-blue-500" size={24} />
            <div>
              <p className="text-sm text-gray-600">Total Accounts</p>
              <p className="text-xl font-bold">{emailAccounts.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center gap-3">
            <Globe className="text-green-500" size={24} />
            <div>
              <p className="text-sm text-gray-600">Active Domains</p>
              <p className="text-xl font-bold">{availableDomains.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center gap-3">
            <Send className="text-purple-500" size={24} />
            <div>
              <p className="text-sm text-gray-600">Emails Sent</p>
              <p className="text-xl font-bold">{emailAccounts.reduce((sum, acc) => sum + acc.emails_sent, 0)}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center gap-3">
            <Inbox className="text-orange-500" size={24} />
            <div>
              <p className="text-sm text-gray-600">Emails Received</p>
              <p className="text-xl font-bold">{emailAccounts.reduce((sum, acc) => sum + acc.emails_received, 0)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Available Domains for Quick Setup */}
      {availableDomains.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow border">
          <h2 className="text-lg font-semibold mb-4">🚀 Quick Domain Setup</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {availableDomains.map((domain) => (
              <div key={domain.id} className="border rounded-lg p-4 hover:shadow-md">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-medium text-gray-900">{domain.name}</h3>
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                    {domain.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  Emails sent: {domain.emails_sent}
                </p>
                <button
                  onClick={() => quickSetupDomain(domain.id)}
                  className="w-full bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 text-sm"
                >
                  Create Standard Accounts
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Email Accounts List */}
      <div className="bg-white rounded-lg shadow border">
        <div className="p-6 border-b">
          <h2 className="text-lg font-semibold">Email Accounts</h2>
        </div>
        
        {emailAccounts.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <Mail size={48} className="mx-auto mb-4 text-gray-300" />
            <p>No email accounts created yet</p>
            <p className="text-sm">Create your first email account to get started</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left p-4 font-medium">Email Address</th>
                  <th className="text-left p-4 font-medium">Type</th>
                  <th className="text-left p-4 font-medium">Status</th>
                  <th className="text-left p-4 font-medium">Stats</th>
                  <th className="text-left p-4 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {emailAccounts.map((account) => (
                  <tr key={account.id} className="border-t hover:bg-gray-50">
                    <td className="p-4">
                      <div>
                        <div className="font-medium">{account.email_address}</div>
                        <div className="text-sm text-gray-500">{account.domain_name}</div>
                      </div>
                    </td>
                    <td className="p-4">
                      <span className="inline-flex items-center gap-1 text-sm">
                        {accountTypes.find(t => t.value === account.account_type)?.label || account.account_type}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className={`px-2 py-1 rounded text-xs ${
                        account.status === 'active' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {account.status}
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="text-sm">
                        <div>📤 Sent: {account.emails_sent}</div>
                        <div>📥 Received: {account.emails_received}</div>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex gap-2">
                        <button
                          onClick={() => sendTestEmail(account.id)}
                          className="text-blue-600 hover:text-blue-700 text-sm"
                          title="Send test email"
                        >
                          🧪 Test
                        </button>
                        <button
                          className="text-green-600 hover:text-green-700 text-sm"
                          title="Open inbox"
                        >
                          📬 Inbox
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Create Account Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Create Email Account</h2>
            
            <form onSubmit={handleCreateAccount} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Username</label>
                <input
                  type="text"
                  value={createForm.username}
                  onChange={(e) => setCreateForm({...createForm, username: e.target.value})}
                  placeholder="admin, support, etc."
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Domain</label>
                <select
                  value={createForm.domain_id}
                  onChange={(e) => setCreateForm({...createForm, domain_id: e.target.value})}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                  required
                >
                  <option value="">Select domain...</option>
                  {availableDomains.map((domain) => (
                    <option key={domain.id} value={domain.id}>
                      {domain.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Account Type</label>
                <select
                  value={createForm.account_type}
                  onChange={(e) => setCreateForm({...createForm, account_type: e.target.value})}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                >
                  {accountTypes.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label} - {type.desc}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
                >
                  Create Account
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 rounded hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmailDashboard;
