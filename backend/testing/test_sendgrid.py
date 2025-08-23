#!/usr/bin/env python3
import os
import django
import sys

# Add the backend directory to Python path
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

# Test SendGrid
from django.conf import settings
from campaigns.sendgrid_service import SendGridService

print("🔍 Testing SendGrid Configuration...")
print(f"SENDGRID_API_KEY configured: {'Yes' if settings.PHISHING_CONFIG['SENDGRID_API_KEY'] else 'No'}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Test SendGrid service
try:
    service = SendGridService()
    print("✅ SendGrid service initialized successfully")
    
    # Test with a simple email send
    result = service.send_phishing_email_sendgrid(
        recipient_email="test@example.com",
        subject="Test Email",
        html_content="<h1>Test</h1>",
        sender_email=settings.DEFAULT_FROM_EMAIL,
        use_spoofing=False
    )
    print(f"Test email result: {result}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
