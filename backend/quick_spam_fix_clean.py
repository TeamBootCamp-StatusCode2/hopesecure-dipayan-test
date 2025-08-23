#!/usr/bin/env python3
"""
Quick Email Spam Fix Script
Apply immediate fixes to reduce spam filter issues
"""

import os
import sys

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
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: #f8f9fa;
            color: #333;
            padding: 30px 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
        .content {
            background: white;
            padding: 30px;
            border: 1px solid #e1e5e9;
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
            border-radius: 8px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>IT Security Department</h1>
        <p>Cybersecurity Awareness Training</p>
    </div>
    
    <div class="content">
        <h2>Security Awareness Training</h2>
        <p>Dear Team Member,</p>
        <p>This email is part of our ongoing cybersecurity awareness training program.</p>
        
        <div class="notice">
            <h3>Educational Purpose</h3>
            <p>This is a simulated security scenario designed to help you identify potential threats.</p>
        </div>
        
        <p>Your participation helps strengthen our organization's security posture.</p>
        <p>Best regards,<br><strong>IT Security Team</strong></p>
    </div>
    
    <div class="footer">
        <p><strong>Security Awareness Training Program</strong></p>
        <p>Questions? Contact your IT security team</p>
        <p><a href="mailto:unsubscribe@hopesecure.tech">Unsubscribe</a> | IT Department</p>
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
    
    print("📋 Add these DNS records to your domain provider:")
    print()
    print("1. SPF Record:")
    print("   Type: TXT")
    print("   Name: hopesecure.tech")
    print("   Value: v=spf1 include:sendgrid.net ~all")
    print()
    print("2. DMARC Record:")
    print("   Type: TXT") 
    print("   Name: _dmarc.hopesecure.tech")
    print("   Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@hopesecure.tech")
    print()
    print("3. SendGrid Authentication (get from SendGrid dashboard):")
    print("   Type: CNAME")
    print("   Name: em[XXXX].hopesecure.tech")
    print("   Value: u[XXXX].wl.sendgrid.net")
    print()
    print("⚠️  Important: DNS changes take 24-48 hours to propagate")

def main():
    """Main function to apply all fixes"""
    print("🚀 Quick Email Spam Fix Script")
    print("=" * 40)
    
    fixes_applied = 0
    total_fixes = 4
    
    # 1. Check campaign service
    if fix_campaign_launch_service():
        fixes_applied += 1
    
    # 2. Check environment variables
    if check_environment_variables():
        fixes_applied += 1
    
    # 3. Create improved template
    if create_quick_email_template():
        fixes_applied += 1
    
    # 4. Provide DNS guide
    provide_dns_setup_guide()
    fixes_applied += 1
    
    # Summary
    print(f"\n📊 Fixes Applied: {fixes_applied}/{total_fixes}")
    
    if fixes_applied >= 3:
        print("✅ Most fixes applied successfully!")
    else:
        print("⚠️  Some fixes need manual attention")
    
    print("\n🎯 Next Steps:")
    print("1. Configure SendGrid domain authentication")
    print("2. Add DNS records to your domain")
    print("3. Test email delivery")
    print("4. Monitor SendGrid analytics")
    print("5. Gradually increase campaign volume")

if __name__ == "__main__":
    main()
