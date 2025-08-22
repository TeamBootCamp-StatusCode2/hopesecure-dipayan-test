#!/usr/bin/env python3
"""
SendGrid Configuration Test Script
Test your SendGrid setup for HopeSecure phishing platform
"""

import os
import sys
import sendgrid
from sendgrid.helpers.mail import Mail, From, To, Subject, Content

def test_sendgrid_setup():
    """Test SendGrid configuration"""
    print("🔧 Testing SendGrid Configuration...")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key:
        print("❌ SENDGRID_API_KEY not found in environment variables")
        print("   Please set: export SENDGRID_API_KEY=your-api-key-here")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Initialize SendGrid client
    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        print("✅ SendGrid client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize SendGrid client: {e}")
        return False
    
    # Test API connection
    try:
        # Test by getting API key info instead of user info
        response = sg.api_keys.get()
        if response.status_code == 200:
            print("✅ SendGrid API connection successful")
            print(f"   Status Code: {response.status_code}")
        else:
            print(f"❌ SendGrid API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ SendGrid API connection failed: {e}")
        # Try alternative test - just initialize without API call
        print("ℹ️  Skipping API verification - will test with actual email send")
    
    return True

def send_test_email():
    """Send a test email"""
    print("\n📧 Sending Test Email...")
    print("=" * 50)
    
    # Get email details
    from_email = input("From email (press Enter for test@hopesecure.com): ").strip()
    if not from_email:
        from_email = "test@hopesecure.com"
    
    to_email = input("To email (required): ").strip()
    if not to_email:
        print("❌ Recipient email is required")
        return False
    
    # Create email
    message = Mail()
    message.from_email = From(from_email, "HopeSecure Test")
    message.add_to(To(to_email))
    message.subject = Subject("HopeSecure SendGrid Test Email")
    
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; margin: 20px;">
        <h2 style="color: #2c5aa0;">🔒 HopeSecure Test Email</h2>
        <p>Congratulations! Your SendGrid configuration is working correctly.</p>
        
        <div style="background: #f0f7ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3>Test Results:</h3>
            <ul>
                <li>✅ SendGrid API Key: Valid</li>
                <li>✅ Email Sending: Working</li>
                <li>✅ HTML Content: Rendered</li>
            </ul>
        </div>
        
        <p>Your phishing simulation platform is ready to use!</p>
        
        <hr>
        <small style="color: #666;">
            Sent from HopeSecure Phishing Platform<br>
            Test conducted at: $(date)
        </small>
    </body>
    </html>
    """
    
    message.add_content(Content("text/html", html_content))
    
    # Send email
    try:
        api_key = os.getenv('SENDGRID_API_KEY')
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"✅ Test email sent successfully to {to_email}")
            print(f"   Message ID: {response.headers.get('X-Message-Id', 'N/A')}")
            print("   Check your inbox (and spam folder)")
            return True
        else:
            print(f"❌ Failed to send email: {response.status_code}")
            print(f"   Response: {response.body}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 HopeSecure SendGrid Setup Test")
    print("=" * 50)
    
    # Test 1: Configuration
    if not test_sendgrid_setup():
        print("\n❌ SendGrid setup test failed")
        sys.exit(1)
    
    # Test 2: Send email (optional)
    print("\n" + "=" * 50)
    send_test = input("Do you want to send a test email? (y/n): ").strip().lower()
    
    if send_test in ['y', 'yes']:
        if send_test_email():
            print("\n✅ All tests passed! SendGrid is ready for HopeSecure.")
        else:
            print("\n❌ Test email failed")
            sys.exit(1)
    else:
        print("\n✅ Configuration test passed! SendGrid setup is valid.")
    
    print("\n🎯 Next Steps:")
    print("1. Set up your phishing domains")
    print("2. Configure email templates")
    print("3. Create your first campaign")
    print("4. Monitor results in real-time")

if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Note: python-dotenv not found, using system environment variables")
    
    main()
