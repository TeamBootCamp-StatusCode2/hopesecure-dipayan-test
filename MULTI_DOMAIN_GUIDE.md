# Multi-Domain Phishing Campaign System
## SendGrid দিয়ে Multiple Domain Extensions ব্যবহারের সম্পূর্ণ গাইড

এই system দিয়ে আপনি বিভিন্ন domain extensions ব্যবহার করে professional phishing campaigns চালাতে পারবেন।

## 🌐 System Overview

### Multi-Domain Architecture:
```
┌─────────────────────────────────────────────────────────────┐
│                    HopeSecure Platform                      │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React)          Backend (Django)                │
│  └── MultiDomainCampaign   └── Multi-Domain Service        │
├─────────────────────────────────────────────────────────────┤
│                    SendGrid API                             │
├─────────────────────────────────────────────────────────────┤
│  Domain 1: microsoft-update.com                            │
│  Domain 2: google-security.net                             │
│  Domain 3: bank-verification.org                           │
│  Domain 4: facebook-security.info                          │
│  Domain 5: amazon-delivery.co                              │
└─────────────────────────────────────────────────────────────┘
```

## 📧 Email Domain Categories

### 1. Corporate Domains (Business Spoofing)
```
microsoft-update.com
├── security@microsoft-update.com
├── notifications@microsoft-update.com  
├── admin@microsoft-update.com
└── support@microsoft-update.com

google-security.net
├── noreply@google-security.net
├── alerts@google-security.net
└── verification@google-security.net
```

### 2. Banking/Financial Domains
```
bank-verification.org
├── security@bank-verification.org
├── alerts@bank-verification.org
└── fraud@bank-verification.org
```

### 3. Social Media Domains
```
facebook-security.info
├── security@facebook-security.info
└── notifications@facebook-security.info
```

### 4. E-commerce Domains
```
amazon-delivery.co
├── delivery@amazon-delivery.co
├── orders@amazon-delivery.co
└── tracking@amazon-delivery.co
```

## 🚀 How It Works

### 1. Domain Setup Process:
```python
# Add new domain
POST /api/campaigns/multi-domain/add-domain/
{
    "domain_name": "microsoft-update.com",
    "domain_type": "spoofing"
}

# System generates DNS instructions
Response:
{
    "dns_setup": {
        "TXT": "_sendgrid.microsoft-update.com",
        "CNAME": "mail.microsoft-update.com → sendgrid.net",
        "MX": "microsoft-update.com → mx.sendgrid.net"
    }
}
```

### 2. Email Generation Process:
```python
# Random email selection
def get_random_sender_email(domain_type='corporate'):
    suitable_domains = filter_domains_by_type(domain_type)
    selected_domain = random.choice(suitable_domains)
    prefix = random.choice(['security', 'notifications', 'alerts'])
    return f"{prefix}@{selected_domain}"

# Result: security@microsoft-update.com
```

### 3. Campaign Execution:
```python
# Multi-domain campaign
for recipient in target_emails:
    template = rotate_template()
    sender_email = get_random_sender_email()
    tracking_url = generate_tracking_url(recipient)
    
    send_email(
        from_email=sender_email,
        to_email=recipient,
        template=template,
        tracking_url=tracking_url
    )
```

## 📊 Frontend Implementation

### MultiDomainCampaign Component Features:
- ✅ Domain type selection (Corporate, Banking, Social, etc.)
- ✅ Template rotation (Microsoft, Google, Bank alerts)
- ✅ Random sender email generation
- ✅ Email delay configuration for rate limiting
- ✅ Real-time domain statistics
- ✅ Test email functionality

### Usage Example:
```typescript
// Launch multi-domain campaign
const campaignConfig = {
    campaign_name: "Q1 Security Assessment",
    target_emails: ["user1@company.com", "user2@company.com"],
    domain_type: "corporate",
    use_random_domains: true,
    delay_seconds: 2
};

fetch('/api/campaigns/multi-domain/create/', {
    method: 'POST',
    body: JSON.stringify(campaignConfig)
});
```

## 🎯 Email Templates

### Microsoft Security Alert:
```html
Subject: 🔒 Microsoft Security Alert - Immediate Action Required
From: security@microsoft-update.com

<div style="background: #0078d4; color: white; padding: 20px;">
    <h2>Microsoft Security Alert</h2>
</div>
<div style="padding: 20px;">
    <p>Dear {{recipient_name}},</p>
    <p>We detected unusual activity in your Microsoft account.</p>
    <a href="{{tracking_link}}" style="background: #0078d4; color: white; padding: 10px 20px;">
        Verify Account Security
    </a>
</div>
```

### Google Verification:
```html
Subject: 🔐 Google Account Verification Required
From: noreply@google-security.net

<div style="background: #4285f4; color: white; padding: 20px;">
    <h2>Google Account Security</h2>
</div>
<div style="padding: 20px;">
    <p>Hello {{recipient_name}},</p>
    <p>Your Google account requires immediate verification.</p>
    <a href="{{tracking_link}}" style="background: #4285f4; color: white; padding: 10px 20px;">
        Verify Now
    </a>
</div>
```

### Bank Fraud Alert:
```html
Subject: 🏦 URGENT: Suspicious Activity Detected
From: fraud@bank-verification.org

<div style="background: #d32f2f; color: white; padding: 20px;">
    <h2>⚠️ FRAUD ALERT</h2>
</div>
<div style="padding: 20px;">
    <p>Dear {{recipient_name}},</p>
    <p>Suspicious transactions detected:</p>
    <ul>
        <li>$500.00 - Online Purchase</li>
        <li>$1,200.00 - ATM Withdrawal</li>
    </ul>
    <a href="{{tracking_link}}" style="background: #d32f2f; color: white; padding: 10px 20px;">
        Verify Transactions
    </a>
</div>
```

## 🔧 SendGrid Configuration

### 1. API Key Setup:
```python
# settings.py
PHISHING_EMAIL_SETTINGS = {
    'SENDGRID_API_KEY': 'your_sendgrid_api_key',
    'DEFAULT_FROM_EMAIL': 'security@your-domain.com',
    'TRACKING_DOMAIN': 'https://your-tracking-domain.com'
}
```

### 2. Domain Verification:
```bash
# DNS Records to add for each domain:
TXT Record: _sendgrid.your-domain.com → "verification_code"
CNAME Record: mail.your-domain.com → sendgrid.net
MX Record: your-domain.com → 10 mx.sendgrid.net
```

### 3. Email Authentication:
```python
# SPF Record
"v=spf1 include:sendgrid.net ~all"

# DKIM Record (Generated by SendGrid)
"k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC..."

# DMARC Record
"v=DMARC1; p=quarantine; rua=mailto:dmarc@your-domain.com"
```

## 📈 Campaign Analytics

### Domain Statistics:
```json
{
    "domain_statistics": [
        {
            "domain": "microsoft-update.com",
            "emails_sent": 150,
            "success_rate": 85.5,
            "click_rate": 23.2,
            "last_used": "2025-01-15T10:30:00Z"
        },
        {
            "domain": "google-security.net", 
            "emails_sent": 98,
            "success_rate": 92.1,
            "click_rate": 31.8,
            "last_used": "2025-01-14T15:45:00Z"
        }
    ]
}
```

### Campaign Results:
```json
{
    "results": {
        "sent": 245,
        "failed": 5,
        "emails_sent": [
            {
                "recipient": "user@company.com",
                "sender": "security@microsoft-update.com",
                "template": "microsoft_security",
                "tracking_url": "https://track.domain.com/click/abc123"
            }
        ]
    }
}
```

## 🛡️ Security Features

### 1. Rate Limiting:
- Configurable delay between emails (1-60 seconds)
- SendGrid API rate limit compliance
- Domain rotation to avoid spam detection

### 2. Tracking & Monitoring:
- Click tracking with unique URLs
- Open rate monitoring
- Real-time campaign statistics
- Domain performance analytics

### 3. Email Spoofing Protection:
- Custom headers for authenticity
- SPF/DKIM/DMARC compliance
- Professional email formatting
- Realistic sender names

## 🚦 Best Practices

### 1. Domain Management:
- Use realistic domain names
- Verify all domains before campaigns
- Rotate domains for different campaign types
- Monitor domain reputation

### 2. Email Content:
- Personalize emails with recipient names
- Use professional templates
- Include realistic company branding
- Test emails before mass sending

### 3. Campaign Strategy:
- Stagger email sending with delays
- Use different templates for variety
- Monitor click rates and adjust
- Follow up with security training

## 🔍 Troubleshooting

### Common Issues:

1. **Domain Not Verified:**
   ```bash
   # Check DNS records
   dig TXT _sendgrid.your-domain.com
   dig MX your-domain.com
   ```

2. **SendGrid API Errors:**
   ```python
   # Check API key validity
   response = sendgrid_client.send(message)
   if response.status_code != 202:
       print(f"Error: {response.body}")
   ```

3. **Email Delivery Issues:**
   - Check SPF/DKIM/DMARC records
   - Verify domain authentication
   - Monitor SendGrid delivery statistics

## 🎉 Summary

এই Multi-Domain Phishing System দিয়ে আপনি:

✅ **Multiple domain extensions** ব্যবহার করতে পারবেন  
✅ **Realistic phishing emails** তৈরি করতে পারবেন  
✅ **Professional templates** ব্যবহার করতে পারবেন  
✅ **Advanced tracking** ও analytics পাবেন  
✅ **SendGrid integration** এর মাধ্যমে reliable delivery পাবেন  
✅ **Rate limiting** ও security features পাবেন  

**Perfect for cybersecurity awareness training এবং penetration testing!**
