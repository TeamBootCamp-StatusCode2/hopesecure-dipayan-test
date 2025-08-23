#!/usr/bin/env python3
"""
Simple SendGrid Email Test using Django
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')

# Setup Django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_django_email():
    """Test email sending using Django's send_mail"""
    print("🚀 Testing Django Email with SendGrid")
    print("=" * 40)
    
    try:
        # Send test email
        subject = 'HopeSecure Test Email - Django Integration'
        message = 'This is a test email from HopeSecure Django backend using SendGrid.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['bolbonakano@gmail.com']  # Replace with your email
        
        print(f"From: {from_email}")
        print(f"To: {recipient_list[0]}")
        print(f"Subject: {subject}")
        
        result = send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ Email sent successfully!")
            print("Check your inbox (and spam folder)")
        else:
            print("❌ Email sending failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_django_email()
