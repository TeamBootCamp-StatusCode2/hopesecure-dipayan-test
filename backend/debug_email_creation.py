#!/usr/bin/env python3
"""
Email Account Creation Debug Script
এই script দিয়ে email account creation issue debug করুন
"""

import os
import sys
import django
import requests
import json
from dotenv import load_dotenv

# Add backend to path
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
load_dotenv('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend/.env')
django.setup()

from django.contrib.auth import get_user_model
from campaigns.domain_models import EmailDomain
from email_accounts.models import EmailAccount

User = get_user_model()

def test_email_account_creation():
    """Test email account creation process"""
    print("🔍 Testing Email Account Creation")
    print("=" * 50)
    
    # 1. Check if user exists
    try:
        user = User.objects.first()
        if not user:
            print("❌ No users found in database")
            print("   Create a user first using: python manage.py createsuperuser")
            return False
        print(f"✅ User found: {user.username}")
    except Exception as e:
        print(f"❌ Error finding user: {e}")
        return False
    
    # 2. Check if domains exist
    try:
        domains = EmailDomain.objects.filter(created_by=user)
        if not domains.exists():
            print("❌ No domains found for user")
            print("   Add a domain first using the domain management interface")
            return False
        
        domain = domains.first()
        print(f"✅ Domain found: {domain.name}")
    except Exception as e:
        print(f"❌ Error finding domains: {e}")
        return False
    
    # 3. Try creating an email account directly
    try:
        # Check if account already exists
        test_username = "test"
        if EmailAccount.objects.filter(username=test_username, domain=domain).exists():
            print(f"⚠️  Email account {test_username}@{domain.name} already exists")
            account = EmailAccount.objects.get(username=test_username, domain=domain)
            print(f"✅ Existing account: {account.email_address}")
        else:
            account = EmailAccount.objects.create(
                username=test_username,
                domain=domain,
                account_type='admin',
                created_by=user
            )
            print(f"✅ Email account created: {account.email_address}")
    except Exception as e:
        print(f"❌ Error creating email account: {e}")
        return False
    
    # 4. Test API endpoint
    try:
        print("\n🌐 Testing API Endpoint...")
        
        # First create an auth token if needed
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        
        # Test API call
        api_url = "http://localhost:8000/api/email/accounts/"
        headers = {
            'Authorization': f'Token {token.key}',
            'Content-Type': 'application/json'
        }
        
        test_data = {
            'username': 'security',
            'domain_id': domain.id,
            'account_type': 'security'
        }
        
        response = requests.post(api_url, json=test_data, headers=headers)
        
        if response.status_code == 201:
            print("✅ API account creation successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API account creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False
    
    print("\n🎯 Email Account Creation: SUCCESS")
    return True

def check_frontend_config():
    """Check frontend configuration"""
    print("\n🎨 Frontend Configuration Check")
    print("=" * 50)
    
    # Check if frontend is making correct API calls
    print("📝 Frontend should call:")
    print("   URL: http://localhost:8000/api/email/accounts/")
    print("   Method: POST")
    print("   Headers: Authorization: Token <your-token>")
    print("   Body: {username, domain_id, account_type}")
    
    # Check common issues
    print("\n⚠️  Common Issues:")
    print("1. Wrong API URL (check port 8000)")
    print("2. Missing authentication token")
    print("3. Domain not created/verified")
    print("4. Username already exists")
    print("5. CORS issues")

def show_debug_steps():
    """Show debugging steps"""
    print("\n🔧 Debug Steps:")
    print("=" * 50)
    print("1. Check Django server logs:")
    print("   - Look for error messages when creating account")
    print("   - Check browser network tab for API response")
    print()
    print("2. Verify authentication:")
    print("   - Make sure user is logged in")
    print("   - Check auth token in localStorage")
    print()
    print("3. Check domain setup:")
    print("   - Domain must be created first")
    print("   - User must own the domain")
    print()
    print("4. Test with curl:")
    print("   curl -X POST http://localhost:8000/api/email/accounts/ \\")
    print("        -H 'Authorization: Token YOUR_TOKEN' \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"username\":\"test\",\"domain_id\":1,\"account_type\":\"admin\"}'")

if __name__ == "__main__":
    try:
        success = test_email_account_creation()
        check_frontend_config()
        
        if not success:
            show_debug_steps()
        else:
            print("\n🚀 Email Account System: WORKING CORRECTLY")
            
    except Exception as e:
        print(f"❌ Script error: {e}")
        show_debug_steps()
