import React, { useState, useEffect } from 'react';
import { ArrowLeft, Mail, Clock, Check, User, Trash2 } from 'lucide-react';

interface IncomingEmail {
  id: number;
  from_email: string;
  from_name: string;
  subject: string;
  text_content: string;
  html_content: string;
  received_at: string;
  is_read: boolean;
  is_spam: boolean;
}

interface SentEmail {
  id: number;
  to_emails: string[];
  cc_emails: string[];
  bcc_emails: string[];
  subject: string;
  text_content: string;
  html_content: string;
  sent_at: string;
  delivery_status: string;
}

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

interface EmailInboxProps {
  account: EmailAccount;
  onBack: () => void;
}

const EmailInbox: React.FC<EmailInboxProps> = ({ account, onBack }) => {
  const [inboxTab, setInboxTab] = useState<'inbox' | 'sent'>('inbox');
  const [inboxEmails, setInboxEmails] = useState<IncomingEmail[]>([]);
  const [sentEmails, setSentEmails] = useState<SentEmail[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<IncomingEmail | SentEmail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInboxEmails();
    loadSentEmails();
  }, [account.id]);

  const loadInboxEmails = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/email/accounts/${account.id}/inbox/`, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setInboxEmails(data);
      }
    } catch (error) {
      console.error('Error loading inbox emails:', error);
    }
  };

  const loadSentEmails = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/email/accounts/${account.id}/sent_emails/`, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setSentEmails(data);
      }
    } catch (error) {
      console.error('Error loading sent emails:', error);
    }
    setLoading(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
      return 'Today ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 2) {
      return 'Yesterday ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays <= 7) {
      return date.toLocaleDateString([], { weekday: 'short' }) + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString();
    }
  };

  const EmailList = ({ emails, type }: { emails: (IncomingEmail | SentEmail)[], type: 'inbox' | 'sent' }) => (
    <div className="space-y-2">
      {emails.length === 0 ? (
        <div className="text-center py-8">
          <Mail className="mx-auto h-12 w-12 text-gray-400" />
          <p className="text-gray-500 mt-2">No {type === 'inbox' ? 'received' : 'sent'} emails</p>
        </div>
      ) : (
        emails.map((email) => (
          <div
            key={email.id}
            onClick={() => setSelectedEmail(email)}
            className={`p-4 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors ${
              type === 'inbox' && 'is_read' in email && !email.is_read ? 'bg-blue-50 border-blue-200' : 'bg-white'
            }`}
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  {type === 'inbox' && 'is_read' in email && !email.is_read && (
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  )}
                  <h3 className={`font-medium truncate ${type === 'inbox' && 'is_read' in email && !email.is_read ? 'font-bold' : ''}`}>
                    {email.subject || '(No Subject)'}
                  </h3>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  {type === 'inbox' ? 
                    ('from_email' in email ? `From: ${email.from_name || email.from_email}` : '') :
                    ('to_emails' in email ? `To: ${email.to_emails.slice(0, 2).join(', ')}${email.to_emails.length > 2 ? '...' : ''}` : '')
                  }
                </p>
                <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                  {email.text_content ? email.text_content.substring(0, 100) + '...' : 'No content'}
                </p>
              </div>
              <div className="text-xs text-gray-500 ml-4">
                {formatDate(type === 'inbox' && 'received_at' in email ? email.received_at : 'sent_at' in email ? email.sent_at : '')}
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );

  const EmailView = ({ email }: { email: IncomingEmail | SentEmail }) => (
    <div className="bg-white border rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => setSelectedEmail(null)}
          className="flex items-center text-blue-600 hover:text-blue-700"
        >
          <ArrowLeft size={16} className="mr-1" />
          Back to list
        </button>
        <div className="flex items-center space-x-2">
          {inboxTab === 'inbox' && 'is_read' in email && !email.is_read && (
            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Unread</span>
          )}
          {inboxTab === 'sent' && 'delivery_status' in email && (
            <span className={`text-xs px-2 py-1 rounded ${
              email.delivery_status === 'sent' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {email.delivery_status}
            </span>
          )}
        </div>
      </div>

      <div className="border-b pb-4 mb-6">
        <h2 className="text-xl font-bold mb-2">{email.subject || '(No Subject)'}</h2>
        <div className="text-sm text-gray-600 space-y-1">
          {inboxTab === 'inbox' && 'from_email' in email && (
            <>
              <div><strong>From:</strong> {email.from_name || email.from_email} &lt;{email.from_email}&gt;</div>
              <div><strong>To:</strong> {account.email_address}</div>
              <div><strong>Date:</strong> {formatDate(email.received_at)}</div>
            </>
          )}
          {inboxTab === 'sent' && 'to_emails' in email && (
            <>
              <div><strong>From:</strong> {account.email_address}</div>
              <div><strong>To:</strong> {email.to_emails.join(', ')}</div>
              {email.cc_emails.length > 0 && <div><strong>CC:</strong> {email.cc_emails.join(', ')}</div>}
              {email.bcc_emails.length > 0 && <div><strong>BCC:</strong> {email.bcc_emails.join(', ')}</div>}
              <div><strong>Date:</strong> {formatDate(email.sent_at)}</div>
            </>
          )}
        </div>
      </div>

      <div className="prose max-w-none">
        {email.html_content ? (
          <div dangerouslySetInnerHTML={{ __html: email.html_content }} />
        ) : (
          <div className="whitespace-pre-wrap">{email.text_content || 'No content'}</div>
        )}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="bg-white">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b">
        <div className="flex items-center space-x-4">
          <button
            onClick={onBack}
            className="flex items-center text-gray-600 hover:text-gray-800"
          >
            <ArrowLeft size={20} className="mr-2" />
            Back to Dashboard
          </button>
          <div>
            <h1 className="text-2xl font-bold">📬 Email Inbox</h1>
            <p className="text-gray-600">{account.email_address}</p>
          </div>
        </div>
        <div className="text-sm text-gray-500">
          {inboxEmails.length} received • {sentEmails.length} sent
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b">
        <div className="flex space-x-8 px-6">
          <button
            onClick={() => setInboxTab('inbox')}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              inboxTab === 'inbox'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            📥 Inbox ({inboxEmails.length})
          </button>
          <button
            onClick={() => setInboxTab('sent')}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              inboxTab === 'sent'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            📤 Sent ({sentEmails.length})
          </button>
        </div>
      </div>

      {/* Email Content */}
      <div className="p-6">
        {selectedEmail ? (
          <EmailView email={selectedEmail} />
        ) : (
          <EmailList 
            emails={inboxTab === 'inbox' ? inboxEmails : sentEmails} 
            type={inboxTab} 
          />
        )}
      </div>
    </div>
  );
};

export default EmailInbox;
