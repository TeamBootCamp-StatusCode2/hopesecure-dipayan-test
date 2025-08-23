#!/usr/bin/env python
"""
Test script to debug email system issues
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from campaigns.domain_models import EmailDomain
from email_accounts.models import EmailAccount
import requests

User = get_user_model()

def test_email_system():
    print("🔍 Testing Email System")
    print("=" * 50)
    
    # 1. Check if users exist
    print("\n1. 👥 Checking Users:")
    users = User.objects.all()
    if users:
        for user in users:
            print(f"   - {user.username} ({user.email}) - Active: {user.is_active}")
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            print(f"     Token: {token.key}")
    else:
        print("   ❌ No users found!")
        return
    
    # 2. Check domains
    print("\n2. 🌐 Checking Domains:")
    domains = EmailDomain.objects.all()
    if domains:
        for domain in domains:
            print(f"   - {domain.name} (Status: {domain.status}) - Created by: {domain.created_by.username}")
    else:
        print("   ❌ No domains found!")
    
    # 3. Check email accounts
    print("\n3. 📧 Checking Email Accounts:")
    accounts = EmailAccount.objects.all()
    if accounts:
        for account in accounts:
            print(f"   - {account.email_address} (Type: {account.account_type}) - Domain: {account.domain.name}")
    else:
        print("   ❌ No email accounts found!")
    
    # 4. Test API with authentication
    if users and domains:
        user = users.first()
        token = Token.objects.get(user=user)
        
        print(f"\n4. 🧪 Testing API with user: {user.username}")
        
        # Test GET accounts
        try:
            response = requests.get(
                'http://localhost:8000/api/email/accounts/',
                headers={'Authorization': f'Token {token.key}'}
            )
            print(f"   GET /api/email/accounts/ - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Found {len(data)} accounts")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
        
        # Test GET domains (corrected URL)
        try:
            response = requests.get(
                'http://localhost:8000/api/email/domains/available_domains/',
                headers={'Authorization': f'Token {token.key}'}
            )
            print(f"   GET /api/email/domains/available_domains/ - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Found {len(data)} available domains")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
        
        # Test creating an email account
        if domains:
            domain = domains.first()
            print(f"\n5. ➕ Testing Email Account Creation with domain: {domain.name}")
            
            try:
                response = requests.post(
                    'http://localhost:8000/api/email/accounts/',
                    headers={
                        'Authorization': f'Token {token.key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'username': 'test123',
                        'domain_id': domain.id,
                        'account_type': 'admin'
                    }
                )
                print(f"   POST /api/email/accounts/ - Status: {response.status_code}")
                if response.status_code in [200, 201]:
                    data = response.json()
                    print(f"   ✅ Account created: {data}")
                else:
                    print(f"   ❌ Error: {response.text}")
            except Exception as e:
                print(f"   ❌ Request failed: {e}")

if __name__ == "__main__":
    test_email_system()
