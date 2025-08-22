"""
Test Domain Management API
Test script to verify domain management functionality
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Add Django project to path
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')

django.setup()

from campaigns.domain_service import DomainDNSManager
from campaigns.domain_models import EmailDomain, DomainDNSRecord
from django.contrib.auth import get_user_model

User = get_user_model()

def test_domain_management():
    """
    Test domain management functionality
    """
    print("🧪 Testing Domain Management System")
    print("=" * 50)
    
    # Get or create test user
    try:
        user = User.objects.get(username='testadmin')
        print(f"✅ Using existing test user: {user.username}")
    except User.DoesNotExist:
        try:
            user = User.objects.create_user(
                username='testadmin',
                email='testadmin@test.com',
                password='testpass123'
            )
            print(f"✅ Created test user: {user.username}")
        except Exception as e:
            # Try to get any superuser
            user = User.objects.filter(is_superuser=True).first()
            if user:
                print(f"✅ Using existing superuser: {user.username}")
            else:
                print(f"❌ Failed to create test user: {str(e)}")
                return
    
    # Initialize domain manager
    dns_manager = DomainDNSManager()
    
    # Test 1: Add domain
    print("\n📝 Test 1: Adding Domain")
    domain_name = "test-security-alerts.com"
    success, result = dns_manager.add_domain(
        domain_name=domain_name,
        domain_type='spoofing',
        user=user
    )
    
    if success:
        print(f"✅ Domain added successfully: {domain_name}")
        print(f"   Domain ID: {result['domain_id']}")
        print(f"   Verification Token: {result['verification_token'][:20]}...")
        print(f"   DNS Records: {len(result['dns_records'])} records created")
        domain_id = result['domain_id']
    else:
        print(f"❌ Failed to add domain: {result}")
        return
    
    # Test 2: List domains
    print("\n📋 Test 2: Listing User Domains")
    domains = dns_manager.list_user_domains(user)
    print(f"✅ Found {len(domains)} domains for user {user.username}")
    for domain in domains:
        print(f"   - {domain['name']} ({domain['status']})")
    
    # Test 3: Get DNS records
    print("\n🔍 Test 3: Getting DNS Records")
    dns_records = dns_manager.get_required_dns_records(EmailDomain.objects.get(id=domain_id))
    print(f"✅ Found {len(dns_records)} DNS records:")
    for record in dns_records:
        print(f"   - {record['type']}: {record['name']} -> {record['value'][:50]}...")
    
    # Test 4: Domain verification (will fail for test domain)
    print("\n🔐 Test 4: Domain Verification")
    success, result = dns_manager.verify_domain_dns(domain_id)
    if success:
        verified = result['domain_verified']
        print(f"✅ Verification completed: {'✅ Verified' if verified else '❌ Failed'}")
        for record in result['records']:
            status = "✅" if record['verified'] else "❌"
            print(f"   {status} {record['record_type']}: {record['name']}")
    else:
        print(f"❌ Verification error: {result}")
    
    # Test 5: Domain analytics
    print("\n📊 Test 5: Domain Analytics")
    success, analytics = dns_manager.get_domain_analytics(domain_id)
    if success:
        print(f"✅ Analytics retrieved for {analytics['domain_name']}:")
        print(f"   Status: {analytics['status']}")
        print(f"   Emails Sent: {analytics['emails_sent']}")
        print(f"   Success Rate: {analytics['success_rate']}%")
        print(f"   Created: {analytics['created_at']}")
    else:
        print(f"❌ Analytics error: {analytics}")
    
    # Test 6: Update domain settings
    print("\n⚙️  Test 6: Update Domain Settings")
    settings_data = {
        'max_emails_per_day': 500,
        'rate_limit_per_hour': 50,
        'click_tracking_enabled': True,
        'open_tracking_enabled': True
    }
    success, message = dns_manager.update_domain_settings(domain_id, settings_data, user)
    if success:
        print(f"✅ Settings updated: {message}")
    else:
        print(f"❌ Settings update failed: {message}")
    
    # Test 7: Database verification
    print("\n🗄️  Test 7: Database Verification")
    try:
        domain = EmailDomain.objects.get(id=domain_id)
        dns_records = DomainDNSRecord.objects.filter(domain=domain)
        
        print(f"✅ Domain in database: {domain.name}")
        print(f"   Type: {domain.domain_type}")
        print(f"   Status: {domain.status}")
        print(f"   Max emails/day: {domain.max_emails_per_day}")
        print(f"   Rate limit/hour: {domain.rate_limit_per_hour}")
        print(f"   Click tracking: {domain.click_tracking_enabled}")
        print(f"   Open tracking: {domain.open_tracking_enabled}")
        
        print(f"✅ DNS Records in database: {dns_records.count()}")
        for record in dns_records:
            print(f"   - {record.record_type}: {record.name} -> {record.value[:50]}...")
            print(f"     TTL: {record.ttl}, Verified: {record.is_verified}")
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
    
    # Clean up test data
    print("\n🧹 Cleanup: Removing Test Data")
    success, message = dns_manager.delete_domain(domain_id, user)
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ Cleanup failed: {message}")
    
    print("\n" + "=" * 50)
    print("🎉 Domain Management Test Completed!")

def test_domain_suggestions():
    """
    Test domain suggestions
    """
    print("\n💡 Testing Domain Suggestions")
    from campaigns.domain_service import get_sendgrid_domain_suggestions
    
    suggestions = get_sendgrid_domain_suggestions()
    print(f"✅ Got {len(suggestions)} domain suggestions:")
    for suggestion in suggestions:
        print(f"   - {suggestion['domain']} ({suggestion['type']})")
        print(f"     {suggestion['description']}")

def test_domain_validation():
    """
    Test domain name validation
    """
    print("\n🔍 Testing Domain Validation")
    from campaigns.domain_service import validate_domain_name
    
    test_domains = [
        "valid-domain.com",
        "test123.org",
        "sub.domain.net",
        "invalid domain.com",  # Invalid: space
        "toolong" + "a" * 60 + ".com",  # Invalid: too long
        "valid.co.uk",
        "-invalid.com",  # Invalid: starts with hyphen
        "valid-test.info"
    ]
    
    for domain in test_domains:
        is_valid = validate_domain_name(domain)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"   {status}: {domain}")

if __name__ == "__main__":
    try:
        test_domain_management()
        test_domain_suggestions()
        test_domain_validation()
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
