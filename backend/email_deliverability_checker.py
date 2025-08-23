#!/usr/bin/env python3
"""
Email Deliverability Checker and Spam Filter Avoidance Guide
Check your email configuration and provide recommendations
"""

import os
import sys
import re
import json
from datetime import datetime

# Add Django setup
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')

try:
    import django
    django.setup()
    from django.conf import settings
except:
    print("Warning: Django not available, running basic checks only")

def check_sendgrid_reputation():
    """Check SendGrid account status and reputation"""
    print("🔍 Checking SendGrid Account Status...")
    print("=" * 50)
    
    try:
        import sendgrid
        api_key = os.getenv('SENDGRID_API_KEY') or settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        
        if not api_key:
            print("❌ SendGrid API key not found")
            return False
        
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        
        # Check reputation
        try:
            response = sg.reputation.get()
            if response.status_code == 200:
                rep_data = json.loads(response.body)
                print(f"✅ Account Reputation: {rep_data.get('reputation', 'Unknown')}")
            else:
                print(f"⚠️  Could not fetch reputation: {response.status_code}")
        except:
            print("⚠️  Reputation check not available")
        
        print("✅ SendGrid API connection successful")
        return True
        
    except Exception as e:
        print(f"❌ SendGrid connection failed: {e}")
        return False

def check_domain_authentication():
    """Check domain authentication status"""
    print("\n🔐 Checking Domain Authentication...")
    print("=" * 50)
    
    recommendations = []
    
    # Check if domain is configured
    sender_email = os.getenv('DEFAULT_FROM_EMAIL', 'hope@hopesecure.tech')
    domain = sender_email.split('@')[1] if '@' in sender_email else 'hopesecure.tech'
    
    print(f"📧 Sender Domain: {domain}")
    
    # Basic DNS checks (simplified)
    try:
        import subprocess
        
        # Check SPF record
        try:
            spf_result = subprocess.run(['dig', '+short', 'TXT', domain], 
                                      capture_output=True, text=True, timeout=10)
            if 'spf1' in spf_result.stdout.lower():
                print("✅ SPF record found")
            else:
                print("❌ SPF record not found")
                recommendations.append("Add SPF record: v=spf1 include:sendgrid.net ~all")
        except:
            print("⚠️  Could not check SPF record")
        
        # Check DKIM
        try:
            dkim_result = subprocess.run(['dig', '+short', 'TXT', f's1._domainkey.{domain}'], 
                                       capture_output=True, text=True, timeout=10)
            if 'dkim' in dkim_result.stdout.lower() or 'k=rsa' in dkim_result.stdout:
                print("✅ DKIM record found")
            else:
                print("❌ DKIM record not found")
                recommendations.append("Configure DKIM through SendGrid domain authentication")
        except:
            print("⚠️  Could not check DKIM record")
            
    except ImportError:
        print("⚠️  DNS checking tools not available")
        recommendations.extend([
            "Install dig tool for DNS checking: sudo apt-get install dnsutils",
            "Manually verify SPF/DKIM records"
        ])
    
    return recommendations

def analyze_email_content(subject, content):
    """Analyze email content for spam indicators"""
    print("\n📧 Analyzing Email Content...")
    print("=" * 50)
    
    issues = []
    recommendations = []
    score = 100
    
    # Spam word detection
    spam_phrases = [
        'FREE', 'URGENT', 'ACT NOW', 'LIMITED TIME', 'CLICK HERE NOW',
        'WINNER', 'CONGRATULATIONS', '$$$', '100% FREE', 'CALL NOW',
        'URGENT ACTION REQUIRED', 'VERIFY IMMEDIATELY', 'SUSPENDED',
        'ACCOUNT WILL BE CLOSED', 'CONFIRM IDENTITY', 'UPDATE PAYMENT'
    ]
    
    spam_count = sum(1 for phrase in spam_phrases if phrase in subject.upper() or phrase in content.upper())
    if spam_count > 0:
        issues.append(f"Found {spam_count} spam trigger words/phrases")
        score -= spam_count * 15
        recommendations.append("Replace spam trigger words with professional alternatives")
    
    # Subject line analysis
    if len(subject) > 50:
        issues.append("Subject line too long (>50 characters)")
        score -= 10
        recommendations.append("Keep subject line under 50 characters")
    
    if subject.count('!') > 2:
        issues.append("Too many exclamation marks in subject")
        score -= 5
        recommendations.append("Use professional tone in subject line")
    
    # Content analysis
    if len(content) < 100:
        issues.append("Email content too short")
        score -= 10
        recommendations.append("Add more substantial content (at least 100 characters)")
    
    if content.count('!') > 5:
        issues.append("Too many exclamation marks in content")
        score -= 10
        recommendations.append("Reduce exclamation marks for professional tone")
    
    # HTML structure check
    if '<html>' not in content.lower():
        issues.append("Missing proper HTML structure")
        score -= 5
        recommendations.append("Use proper HTML structure with DOCTYPE")
    
    if 'unsubscribe' not in content.lower():
        issues.append("Missing unsubscribe information")
        score -= 15
        recommendations.append("Add unsubscribe information for compliance")
    
    # Print results
    print(f"📊 Deliverability Score: {max(0, score)}/100")
    
    if issues:
        print("\n❌ Issues Found:")
        for issue in issues:
            print(f"   • {issue}")
    
    if recommendations:
        print("\n💡 Recommendations:")
        for rec in recommendations:
            print(f"   • {rec}")
    
    return max(0, score), issues, recommendations

def provide_spam_filter_tips():
    """Provide comprehensive tips to avoid spam filters"""
    print("\n🛡️  Best Practices to Avoid Spam Filters")
    print("=" * 50)
    
    tips = [
        "✅ Use authenticated sender domains (SPF, DKIM, DMARC)",
        "✅ Maintain professional email formatting",
        "✅ Include unsubscribe links",
        "✅ Use proper text-to-image ratio (more text than images)",
        "✅ Avoid excessive capitalization and punctuation",
        "✅ Include sender's physical address",
        "✅ Maintain consistent sending patterns",
        "✅ Monitor bounce rates and engagement",
        "✅ Use reputable email service provider (SendGrid)",
        "✅ Warm up new domains gradually"
    ]
    
    for tip in tips:
        print(f"   {tip}")
    
    print("\n🚫 Words/Phrases to Avoid:")
    avoid_words = [
        "FREE", "URGENT", "ACT NOW", "LIMITED TIME", "CLICK HERE NOW",
        "WINNER", "CONGRATULATIONS", "100% FREE", "CALL NOW",
        "GUARANTEE", "RISK FREE", "NO OBLIGATION", "CASH BONUS"
    ]
    
    for word in avoid_words:
        print(f"   • {word}")

def check_sendgrid_settings():
    """Check SendGrid configuration for optimal deliverability"""
    print("\n⚙️  SendGrid Configuration Check")
    print("=" * 50)
    
    try:
        # Check basic settings
        api_key = os.getenv('SENDGRID_API_KEY')
        sender_email = os.getenv('DEFAULT_FROM_EMAIL', 'hope@hopesecure.tech')
        
        print(f"📧 Sender Email: {sender_email}")
        print(f"🔑 API Key: {'✅ Configured' if api_key else '❌ Missing'}")
        
        # SendGrid specific recommendations
        print("\n💡 SendGrid Optimization Tips:")
        print("   • Enable domain authentication in SendGrid dashboard")
        print("   • Configure custom return path")
        print("   • Set up dedicated IP (for high volume)")
        print("   • Monitor SendGrid analytics regularly")
        print("   • Use SendGrid's spam checker tool")
        print("   • Configure unsubscribe groups")
        
        return True
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False

def generate_improved_template():
    """Generate an improved email template"""
    print("\n📝 Improved Email Template")
    print("=" * 50)
    
    template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Notice</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .content { background: white; padding: 25px; border: 1px solid #ddd; border-radius: 8px; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
        .notice { background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="margin: 0; color: #1976d2;">IT Security Department</h2>
            <p style="margin: 5px 0 0 0;">Security Awareness Training</p>
        </div>
        <div class="content">
            <h3>Security Training Exercise</h3>
            <p>Dear Team Member,</p>
            <p>This message is part of our ongoing cybersecurity awareness training program.</p>
            <div class="notice">
                <p><strong>Educational Purpose</strong></p>
                <p>This is a simulated security scenario designed to help you identify potential threats.</p>
            </div>
            <p>Your participation helps strengthen our organization's security posture.</p>
        </div>
        <div class="footer">
            <p><strong>Security Awareness Training Program</strong></p>
            <p>Questions? Contact your IT security team</p>
            <p><a href="mailto:unsubscribe@company.com">Unsubscribe</a> | IT Department, Company Address</p>
        </div>
    </div>
</body>
</html>
    '''
    
    print("💡 Use this improved template structure for better deliverability:")
    print(template)

def main():
    """Main function to run all checks"""
    print("🚀 HopeSecure Email Deliverability Checker")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all checks
    sendgrid_ok = check_sendgrid_reputation()
    domain_recs = check_domain_authentication()
    check_sendgrid_settings()
    
    # Analyze sample content
    sample_subject = "Security Update - Account Verification Required"
    sample_content = """
    <p>Dear User, this is a security awareness training email.</p>
    <p>Please review the security guidelines.</p>
    """
    
    score, issues, recommendations = analyze_email_content(sample_subject, sample_content)
    
    # Provide general tips
    provide_spam_filter_tips()
    generate_improved_template()
    
    # Summary
    print("\n📋 Summary and Next Steps")
    print("=" * 50)
    
    if sendgrid_ok and score > 80:
        print("✅ Your email setup looks good!")
    else:
        print("⚠️  Some improvements needed:")
        
    if domain_recs:
        print("\n🔧 Domain Authentication Recommendations:")
        for rec in domain_recs:
            print(f"   • {rec}")
    
    print("\n🎯 Immediate Actions:")
    print("   1. Configure SPF/DKIM/DMARC records")
    print("   2. Use professional email templates")
    print("   3. Monitor SendGrid analytics")
    print("   4. Test emails before campaigns")
    print("   5. Gradually increase sending volume")

if __name__ == "__main__":
    main()
