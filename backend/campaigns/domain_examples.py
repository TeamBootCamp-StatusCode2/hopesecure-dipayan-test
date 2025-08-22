"""
SendGrid Multiple Domain Email Examples
বিভিন্ন domain extension দিয়ে phishing email পাঠানোর উদাহরণ
"""

# Example Domain Extensions for Phishing Campaigns:

PHISHING_DOMAIN_EXAMPLES = {
    # Corporate/Business Spoofing
    'microsoft-update.com': {
        'emails': [
            'security@microsoft-update.com',
            'notifications@microsoft-update.com', 
            'admin@microsoft-update.com',
            'support@microsoft-update.com'
        ],
        'use_case': 'Microsoft সাপোর্ট ও security update এর জাল email'
    },
    
    'google-security.net': {
        'emails': [
            'noreply@google-security.net',
            'alerts@google-security.net',
            'verification@google-security.net'
        ],
        'use_case': 'Google security alert এর জাল email'
    },
    
    # Banking/Financial Spoofing  
    'bank-verification.org': {
        'emails': [
            'security@bank-verification.org',
            'alerts@bank-verification.org',
            'fraud@bank-verification.org'
        ],
        'use_case': 'Banking security alert এর জাল email'
    },
    
    # Social Media Spoofing
    'facebook-security.info': {
        'emails': [
            'security@facebook-security.info',
            'notifications@facebook-security.info'
        ],
        'use_case': 'Facebook security notification এর জাল email'
    },
    
    # E-commerce Spoofing
    'amazon-delivery.co': {
        'emails': [
            'delivery@amazon-delivery.co',
            'orders@amazon-delivery.co',
            'tracking@amazon-delivery.co'
        ],
        'use_case': 'Amazon delivery notification এর জাল email'
    },
    
    # Government/Official Spoofing
    'gov-notice.org': {
        'emails': [
            'notifications@gov-notice.org',
            'alerts@gov-notice.org',
            'official@gov-notice.org'
        ],
        'use_case': 'Government notice এর জাল email'
    }
}

# SendGrid Configuration for Multiple Domains
SENDGRID_DOMAIN_CONFIG = {
    'api_key': 'your_sendgrid_api_key',
    'verified_domains': [
        'microsoft-update.com',
        'google-security.net', 
        'bank-verification.org',
        'facebook-security.info',
        'amazon-delivery.co',
        'gov-notice.org'
    ],
    'tracking_settings': {
        'click_tracking': True,
        'open_tracking': True,
        'subscription_tracking': False
    }
}

# Email Template Examples for Different Domains
EMAIL_TEMPLATES = {
    'microsoft_security': {
        'subject': '🔒 Microsoft Security Alert - Immediate Action Required',
        'from_email': 'security@microsoft-update.com',
        'from_name': 'Microsoft Security Team',
        'template': '''
        <html>
        <body style="font-family: Arial;">
            <div style="background: #0078d4; color: white; padding: 20px;">
                <h2>Microsoft Security Alert</h2>
            </div>
            <div style="padding: 20px;">
                <p>Dear {{recipient_name}},</p>
                <p>We detected unusual activity in your Microsoft account.</p>
                <p><strong>⚠️ Immediate action required to secure your account</strong></p>
                <a href="{{tracking_link}}" style="background: #0078d4; color: white; padding: 10px 20px; text-decoration: none;">
                    Verify Account Security
                </a>
                <p>If you did not request this, please contact support immediately.</p>
                <small>© Microsoft Corporation. All rights reserved.</small>
            </div>
        </body>
        </html>
        '''
    },
    
    'google_verification': {
        'subject': '🔐 Google Account Verification Required',
        'from_email': 'noreply@google-security.net', 
        'from_name': 'Google Security',
        'template': '''
        <html>
        <body style="font-family: Arial;">
            <div style="background: #4285f4; color: white; padding: 20px;">
                <h2>Google Account Security</h2>
            </div>
            <div style="padding: 20px;">
                <p>Hello {{recipient_name}},</p>
                <p>Your Google account requires immediate verification.</p>
                <p><strong>🚨 Account will be suspended in 24 hours</strong></p>
                <a href="{{tracking_link}}" style="background: #4285f4; color: white; padding: 10px 20px; text-decoration: none;">
                    Verify Now
                </a>
                <p>This is an automated message from Google Security.</p>
            </div>
        </body>
        </html>
        '''
    },
    
    'bank_fraud_alert': {
        'subject': '🏦 URGENT: Suspicious Activity Detected',
        'from_email': 'fraud@bank-verification.org',
        'from_name': 'Bank Security Department', 
        'template': '''
        <html>
        <body style="font-family: Arial;">
            <div style="background: #d32f2f; color: white; padding: 20px;">
                <h2>⚠️ FRAUD ALERT</h2>
            </div>
            <div style="padding: 20px;">
                <p>Dear {{recipient_name}},</p>
                <p>Suspicious transactions detected on your account:</p>
                <ul>
                    <li>$500.00 - Online Purchase</li>
                    <li>$1,200.00 - ATM Withdrawal</li>
                </ul>
                <p><strong>🔒 Verify these transactions immediately</strong></p>
                <a href="{{tracking_link}}" style="background: #d32f2f; color: white; padding: 10px 20px; text-decoration: none;">
                    Verify Transactions
                </a>
                <p>Call us at 1-800-BANK if you did not authorize these.</p>
            </div>
        </body>
        </html>
        '''
    }
}
