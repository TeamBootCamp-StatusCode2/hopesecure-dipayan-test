# SendGrid Setup Guide for HopeSecure

## 📧 SendGrid Configuration for Phishing Simulation

### Step 1: Create SendGrid Account
1. Go to [SendGrid.com](https://sendgrid.com)
2. Sign up for a free account (100 emails/day free)
3. Verify your email address

### Step 2: Generate API Key
1. Login to SendGrid dashboard
2. Go to **Settings** → **API Keys**
3. Click **Create API Key**
4. Choose **Full Access** (for testing) or **Restricted Access**
5. Copy the API key (you won't see it again!)

### Step 3: Domain Authentication (Recommended)
```bash
# For better email deliverability, authenticate your domain:
# 1. Go to Settings → Sender Authentication
# 2. Click "Authenticate Your Domain"
# 3. Add your domain (e.g., yourdomain.com)
# 4. Add DNS records as instructed
# 5. Verify the domain
```

### Step 4: Configure Environment Variables
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env file and add your SendGrid credentials:
SENDGRID_API_KEY=SG.your-api-key-here
DEFAULT_FROM_EMAIL=security@yourdomain.com
SENDGRID_WEBHOOK_URL=https://yourdomain.com/api/sendgrid/webhook/
```

### Step 5: Install Dependencies
```bash
# Navigate to backend directory
cd backend

# Install SendGrid and other dependencies
pip install -r requirements.txt
```

### Step 6: Test Configuration
```python
# Test SendGrid setup using Django shell
python manage.py shell

# Run this code:
from campaigns.sendgrid_service import verify_sendgrid_setup
result, message = verify_sendgrid_setup()
print(f"SendGrid Status: {result} - {message}")
```

### Step 7: Send Test Email
```bash
# Using the API endpoint:
curl -X POST http://localhost:8000/api/campaigns/send-test-email/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-auth-token" \
  -d '{"recipient_email": "test@example.com"}'
```

## 🔧 Advanced Configuration

### Domain Spoofing Setup
```python
# Configure phishing domains in email_config.py
DOMAIN_SPOOFING_METHODS = {
    'homograph': {
        'examples': {
            'google.com': ['g00gle.com', 'goog1e.com'],
            'microsoft.com': ['microsft.com', 'microsooft.com']
        }
    }
}
```

### Webhook Configuration (Optional)
```python
# For tracking email opens/clicks:
# 1. Go to SendGrid → Settings → Mail Settings
# 2. Enable "Event Webhook"
# 3. Set URL: https://yourdomain.com/api/sendgrid/webhook/
# 4. Select events: delivered, opened, clicked
```

## 📊 Email Tracking Features

### Available Tracking:
- ✅ **Email Delivery** - Track if email was delivered
- ✅ **Email Opens** - Track when recipient opens email
- ✅ **Link Clicks** - Track which links were clicked
- ✅ **Campaign Analytics** - Detailed statistics
- ✅ **Real-time Monitoring** - Live campaign updates

### Custom Headers for Spoofing:
```python
# Automatic header spoofing for phishing simulation:
headers = {
    'From': 'IT Security <security@g00gle-verify.com>',
    'Reply-To': 'security@g00gle-verify.com',
    'X-Originating-IP': '[192.168.1.100]',
    'X-Mailer': 'Microsoft Outlook 16.0'
}
```

## 🚨 Important Security Notes

### Legal Compliance:
- ⚠️ **Only use for authorized security testing**
- ⚠️ **Get written permission before testing**
- ⚠️ **Follow responsible disclosure practices**
- ⚠️ **Comply with local laws and regulations**

### Best Practices:
1. **Limit scope** - Only test within your organization
2. **Document everything** - Keep records of all tests
3. **Gradual testing** - Start with small groups
4. **Monitor carefully** - Watch for negative impacts
5. **Provide training** - Follow up with education

## 🔍 Troubleshooting

### Common Issues:

#### API Key Not Working:
```bash
# Check API key permissions
# Ensure it has "Mail Send" permissions
# Verify key is correctly set in .env file
```

#### Emails Not Sending:
```bash
# Check SendGrid quotas (free: 100/day)
# Verify sender email is authenticated
# Check Django logs for errors
```

#### Domain Authentication Failed:
```bash
# Verify DNS records are correctly added
# Wait 24-48 hours for DNS propagation
# Use SendGrid's domain verification tool
```

## 📈 Monitoring & Analytics

### Dashboard Metrics:
- **Total Campaigns**: Number of active campaigns
- **Emails Sent**: Total emails delivered
- **Open Rate**: Percentage of emails opened
- **Click Rate**: Percentage of links clicked
- **Success Rate**: Phishing simulation success

### Real-time Tracking:
```javascript
// Frontend real-time updates
const campaignStats = await fetch('/api/campaigns/1/live-stats/');
const data = await campaignStats.json();
console.log('Live stats:', data);
```

## 🎯 Campaign Execution Flow

1. **Create Campaign** → Select target employees
2. **Choose Template** → Configure phishing email
3. **Setup Domain** → Configure spoofed sender
4. **Launch Campaign** → Send emails with tracking
5. **Monitor Results** → Real-time analytics
6. **Generate Report** → Export results for training

## 📞 Support

If you encounter issues:
1. Check Django logs: `tail -f backend/logs/django.log`
2. Verify SendGrid status: Visit SendGrid Status Page
3. Test API key: Use SendGrid API testing tool
4. Review documentation: Check SendGrid Python docs
