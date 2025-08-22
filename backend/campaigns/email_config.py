# Email Configuration for Phishing Simulation

"""
Email Domain Mimicking Configuration
এই ফাইলে phishing campaign এর জন্য email configuration রয়েছে
"""

EMAIL_CONFIGURATIONS = {
    # Gmail Mimicking
    'gmail_mimic': {
        'smtp_host': 'smtp.gmail.com',
        'smtp_port': 587,
        'use_tls': True,
        'mimic_domains': [
            'gmaiI.com',  # Capital I instead of l
            'gmai1.com',  # Number 1 instead of l
            'g-mail.com',
            'googlemail.net'
        ],
        'display_names': [
            'Gmail Security Team',
            'Google Account Security',
            'Gmail Support'
        ]
    },
    
    # Corporate Email Mimicking
    'corporate_mimic': {
        'smtp_host': 'localhost',  # Your SMTP server
        'smtp_port': 587,
        'use_tls': True,
        'mimic_domains': [
            'company-mail.com',
            'corp-security.com',
            'hr-notifications.com',
            'it-support.net'
        ],
        'display_names': [
            'IT Security Team',
            'HR Department',
            'System Administrator',
            'Security Alert'
        ]
    },
    
    # Banking/Finance Mimicking
    'banking_mimic': {
        'smtp_host': 'localhost',
        'smtp_port': 587,
        'use_tls': True,
        'mimic_domains': [
            'bank-alert.com',
            'secure-banking.net',
            'account-verification.com'
        ],
        'display_names': [
            'Bank Security',
            'Account Verification',
            'Fraud Prevention Team'
        ]
    }
}

# Domain Spoofing Techniques
DOMAIN_SPOOFING_METHODS = {
    'homograph': {
        'description': 'Similar looking characters',
        'examples': {
            'google.com': ['g00gle.com', 'goog1e.com', 'googIe.com'],
            'microsoft.com': ['microsft.com', 'microsooft.com'],
            'amazon.com': ['amazom.com', 'arnazon.com']
        }
    },
    
    'subdomain': {
        'description': 'Legitimate looking subdomains',
        'examples': {
            'google.com': ['security.google-verify.com', 'gmail.google-support.net'],
            'microsoft.com': ['login.microsoft-security.com'],
            'facebook.com': ['security.facebook-alert.com']
        }
    },
    
    'tld_variation': {
        'description': 'Different top level domains',
        'examples': {
            'gmail.com': ['gmail.net', 'gmail.org', 'gmail.co'],
            'outlook.com': ['outlook.net', 'outlook.org']
        }
    }
}
