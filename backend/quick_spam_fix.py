#!/usr/bin/env python3
"""
Quick Email Spam Fix Script
Apply immediate fixes to reduce spam filter issues
"""

import os
import sys
import re

def fix_campaign_launch_service():
    """Apply spam-prevention fixes to campaign launch service"""
    file_path = '/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend/campaigns/campaign_launch_service.py'
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if anti-spam service is already integrated
        if 'AntiSpamEmailService' in content:
            print("✅ Anti-spam service already integrated in campaign_launch_service.py")
            return True
        
        print("❌ Anti-spam service not found in campaign_launch_service.py")
        print("💡 Please manually integrate the anti-spam service or re-run the integration")
        return False
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔍 Checking Environment Variables...")
    
    required_vars = [
        'SENDGRID_API_KEY',
        'DEFAULT_FROM_EMAIL'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        
        print("\n💡 Add these to your .env file:")
        print("SENDGRID_API_KEY=your_sendgrid_api_key_here")
        print("DEFAULT_FROM_EMAIL=hope@hopesecure.tech")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def create_quick_email_template():
    """Create an improved email template file"""
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Training</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }
        .content {
            background: white;
            padding: 30px;
            border: 1px solid #e1e5e9;
            border-top: none;
        }
        .notice {
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            border-radius: 0 0 8px 8px;
            border: 1px solid #e1e5e9;
            border-top: none;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin: 10px 0;
        }
        .security-badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin: 0; font-size: 24px;">🛡️ IT Security Department</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">Cybersecurity Awareness Training</p>
        <span class="security-badge">TRAINING EXERCISE</span>
    </div>
    
    <div class="content">
        <h2 style="color: #495057; margin-top: 0;">Security Awareness Training</h2>
        
        <p>Dear Team Member,</p>
        
        <p>This email is part of our ongoing cybersecurity awareness training program designed to help you identify and respond to potential security threats.</p>
        
        <div class="notice">
            <h3 style="margin-top: 0; color: #007bff;">📚 Educational Purpose</h3>
            <p style="margin-bottom: 0;">This is a simulated security scenario. Your participation helps strengthen our organization's overall security posture and protects sensitive information.</p>
        </div>
        
        <p>Key learning objectives:</p>
        <ul>
            <li>Recognize suspicious email patterns</li>
            <li>Verify sender authenticity</li>
            <li>Report potential security threats</li>
            <li>Follow proper security protocols</li>
        </ul>
        
        <p>For additional cybersecurity resources and training materials, please visit our internal security portal or contact the IT security team.</p>
        
        <p style="margin-top: 30px;">Best regards,<br>
        <strong>IT Security Team</strong></p>
    </div>
    
    <div class="footer">
        <p><strong>🎯 Security Awareness Training Program</strong></p>
        <p>This email was sent as part of your organization's cybersecurity education initiative.</p>
        <p>Questions about this training? Contact your IT security team at <a href="mailto:security@company.com">security@company.com</a></p>
        <p style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">
            <a href="mailto:unsubscribe@hopesecure.tech?subject=Training%20Unsubscribe">Unsubscribe from training emails</a> | 
            <a href="#">Privacy Policy</a> | 
            IT Department, Your Company Address
        </p>
        <p style="font-size: 10px; color: #adb5bd; margin-top: 10px;">
            © 2025 HopeSecure Security Training Platform. All rights reserved.
        </p>
    </div>
</body>
</html>'''
    
    template_path = '/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend/templates/improved_email_template.html'
    
    try:
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        with open(template_path, 'w') as f:
            f.write(template_content)
        print(f"✅ Created improved email template: {template_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create template: {e}")
        return False

def provide_dns_setup_guide():
    """Provide DNS setup instructions"""
    print("\n🌐 DNS Setup Guide for hopesecure.tech")
    print("=" * 50)
    
    dns_records = [
        {
            'type': 'TXT',
            'name': 'hopesecure.tech',
            'value': 'v=spf1 include:sendgrid.net ~all',
            'purpose': 'SPF Record for email authentication'
        },
        {
            'type': 'TXT',
            'name': '_dmarc.hopesecure.tech',
            'value': 'v=DMARC1; p=quarantine; rua=mailto:dmarc@hopesecure.tech',
            'purpose': 'DMARC policy for email security'
        },
        {
            'type': 'CNAME',
            'name': 'em[XXXX].hopesecure.tech',
            'value': 'u[XXXX].wl.sendgrid.net',
            'purpose': 'SendGrid domain authentication (get from SendGrid dashboard)'
        }
    ]
    
    print("📋 Add these DNS records to your domain provider:")
    print()
    
    for i, record in enumerate(dns_records, 1):
        print(f"{i}. {record['type']} Record:")
        print(f"   Name: {record['name']}")
        print(f"   Value: {record['value']}")
        print(f"   Purpose: {record['purpose']}")
        print()
    
    print("⚠️  Important Notes:")
    print("   • DNS changes can take 24-48 hours to propagate")
    print("   • Get exact CNAME values from SendGrid dashboard")
    print("   • Verify records using: dig TXT hopesecure.tech")

def create_test_email_script():
    """Create a script to test email deliverability"""
    script_content = '''#!/usr/bin/env python3
"""
Quick Email Test Script
Send a test email to check spam filter status
"""

import os
import sys

# Add Django setup
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')

try:
    import django
    django.setup()
    from campaigns.anti_spam_service import AntiSpamEmailService
    
    def send_test_email(recipient_email):
        """Send a test email using anti-spam service"""
        print(f"📧 Sending test email to: {recipient_email}")
        
        service = AntiSpamEmailService()
        
        result = service.send_campaign_email(
            recipient_email=recipient_email,
            subject="Security Training - Email Deliverability Test",
            html_content="""
            <h2>Email Deliverability Test</h2>
            <p>This is a test email to check spam filter avoidance.</p>
            <p>If you receive this in your inbox, the configuration is working!</p>
            """,
            sender_name="IT Security Test",
            campaign_id="test_001"
        )
        
        if result['success']:
            print("✅ Test email sent successfully!")
            print(f"Status Code: {result['status_code']}")
        else:
            print("❌ Test email failed!")
            print(f"Error: {result['message']}")
        
        return result
    
    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Usage: python3 test_email.py recipient@example.com")
            sys.exit(1)
        
        recipient = sys.argv[1]
        send_test_email(recipient)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure Django and anti_spam_service are properly configured")
except Exception as e:
    print(f"❌ Error: {e}")
'''
    
    script_path = '/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend/test_email.py'
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        print(f"✅ Created email test script: {script_path}")
        print(f"💡 Usage: python3 test_email.py your_email@example.com")
        return True
    except Exception as e:
        print(f"❌ Failed to create test script: {e}")
        return False)

if __name__ == "__main__":
    main()
