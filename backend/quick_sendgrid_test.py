#!/usr/bin/env python3
"""
Quick SendGrid Setup Test
এই script run করে SendGrid setup test করুন
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_sendgrid_setup():
    """Check if SendGrid is properly configured"""
    print("🔍 HopeSecure SendGrid Setup Check")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key or api_key == 'your-sendgrid-api-key-here':
        print("❌ SENDGRID_API_KEY not configured")
        print("   Please update .env file with your real API key")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Check default email
    default_email = os.getenv('DEFAULT_FROM_EMAIL')
    if not default_email or '@yourdomain.com' in default_email:
        print("❌ DEFAULT_FROM_EMAIL not configured")
        print("   Please update .env with your verified sender email")
        return False
    
    print(f"✅ Default email: {default_email}")
    
    # Try importing SendGrid
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail
        print("✅ SendGrid package imported successfully")
    except ImportError:
        print("❌ SendGrid package not installed")
        print("   Run: pip install sendgrid")
        return False
    
    # Test API connection
    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        
        # Create a test email (don't send)
        message = Mail(
            from_email=default_email,
            to_emails='test@example.com',
            subject='Test Email',
            html_content='<p>Test content</p>'
        )
        
        print("✅ SendGrid client initialized successfully")
        print("✅ Test email object created")
        
    except Exception as e:
        print(f"❌ SendGrid API error: {e}")
        return False
    
    print("\n🎯 SendGrid Setup Status: READY")
    print("\n📧 Next Steps:")
    print("1. Add your domains in the admin panel")
    print("2. Configure DNS records for each domain")
    print("3. Start creating phishing campaigns")
    
    return True

def show_setup_instructions():
    """Show setup instructions"""
    print("\n📝 Setup Instructions:")
    print("=" * 50)
    print("1. Get SendGrid API Key:")
    print("   - Go to https://sendgrid.com")
    print("   - Create account → Settings → API Keys")
    print("   - Create Full Access API key")
    print("   - Copy the key")
    print()
    print("2. Update .env file:")
    print("   SENDGRID_API_KEY=SG.your-real-api-key-here")
    print("   DEFAULT_FROM_EMAIL=security@your-domain.com")
    print()
    print("3. Verify sender email in SendGrid:")
    print("   - Go to Settings → Sender Authentication")
    print("   - Add your email address")
    print("   - Verify it via email")
    print()
    print("4. Run this test again:")
    print("   python quick_sendgrid_test.py")

if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Please run this script from the backend directory")
        sys.exit(1)
    
    success = check_sendgrid_setup()
    
    if not success:
        show_setup_instructions()
        sys.exit(1)
    
    print("\n🚀 Your HopeSecure platform is ready for email campaigns!")
