#!/usr/bin/env python3
"""
Multi-Domain Campaign Test Script
SendGrid দিয়ে multiple domain extensions test করার জন্য
"""

import os
import sys
import django
import json
from datetime import datetime

# Django setup
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

def test_multi_domain_system():
    """
    Multi-domain system এর সব features test করে
    """
    print("🚀 Starting Multi-Domain Campaign System Test...")
    print("=" * 60)
    
    try:
        # Import after Django setup
        from campaigns.multi_domain_service import MultiDomainPhishingService
        from campaigns.domain_models import EmailDomain
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # Test 1: Service Initialization
        print("\n1. 🔧 Testing Service Initialization...")
        service = MultiDomainPhishingService()
        print("   ✅ MultiDomainPhishingService initialized successfully")
        
        # Test 2: Domain Loading
        print("\n2. 📋 Testing Domain Loading...")
        service.load_verified_domains()
        print(f"   ✅ Loaded {len(service.available_domains)} verified domains")
        for domain in service.available_domains[:3]:
            print(f"      - {domain}")
        
        # Test 3: Random Email Generation
        print("\n3. 📧 Testing Random Email Generation...")
        domain_types = ['corporate', 'banking', 'social', 'ecommerce']
        for domain_type in domain_types:
            random_email = service.get_random_sender_email(domain_type)
            print(f"   {domain_type.capitalize()}: {random_email}")
        
        # Test 4: Email Template Creation
        print("\n4. 📝 Testing Email Template Creation...")
        from campaigns.domain_examples import EMAIL_TEMPLATES
        
        test_recipient = "test@example.com"
        test_tracking_url = "https://track.example.com/click/test123"
        
        for template_name in EMAIL_TEMPLATES.keys():
            email_data = service.create_personalized_email(
                template_name, test_recipient, test_tracking_url
            )
            if email_data:
                print(f"   ✅ {template_name}: {email_data['subject'][:50]}...")
            else:
                print(f"   ❌ Failed to create template: {template_name}")
        
        # Test 5: Domain Statistics
        print("\n5. 📊 Testing Domain Statistics...")
        stats = service.get_domain_statistics()
        print(f"   ✅ Retrieved statistics for {len(stats)} domains")
        for stat in stats[:3]:
            print(f"      - {stat['domain']}: {stat['emails_sent']} emails sent")
        
        # Test 6: Tracking URL Generation
        print("\n6. 🔗 Testing Tracking URL Generation...")
        tracking_url = service.generate_tracking_url("test@example.com", "test_campaign_001")
        print(f"   ✅ Generated tracking URL: {tracking_url}")
        
        # Test 7: Database Domain Check
        print("\n7. 🗄️  Testing Database Domain Management...")
        total_domains = EmailDomain.objects.count()
        verified_domains = EmailDomain.objects.filter(status='verified').count()
        print(f"   ✅ Total domains in database: {total_domains}")
        print(f"   ✅ Verified domains: {verified_domains}")
        
        # Test 8: Email Configuration Test
        print("\n8. ⚙️  Testing Email Configuration...")
        from django.conf import settings
        
        if hasattr(settings, 'PHISHING_EMAIL_SETTINGS'):
            sendgrid_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
            if sendgrid_key:
                print(f"   ✅ SendGrid API Key configured (starts with: {sendgrid_key[:10]}...)")
            else:
                print("   ⚠️  SendGrid API Key not found in settings")
        else:
            print("   ⚠️  PHISHING_EMAIL_SETTINGS not configured")
        
        # Test 9: Sample Campaign Configuration
        print("\n9. 🎯 Testing Campaign Configuration...")
        sample_config = {
            'campaign_id': 'test_multi_domain_' + datetime.now().strftime('%Y%m%d_%H%M%S'),
            'use_random_domains': True,
            'delay_seconds': 2,
            'domain_type': 'corporate'
        }
        print(f"   ✅ Sample campaign config: {json.dumps(sample_config, indent=4)}")
        
        print("\n" + "=" * 60)
        print("🎉 All Tests Completed Successfully!")
        print("\n📋 System Ready For:")
        print("   ✅ Multi-domain phishing campaigns")
        print("   ✅ Template-based email generation")
        print("   ✅ Domain rotation and management")
        print("   ✅ Click tracking and analytics")
        print("   ✅ SendGrid integration")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_domain_examples():
    """
    Domain examples এবং templates test করে
    """
    print("\n" + "=" * 60)
    print("🌐 Testing Domain Examples and Templates")
    print("=" * 60)
    
    try:
        from campaigns.domain_examples import PHISHING_DOMAIN_EXAMPLES, EMAIL_TEMPLATES
        
        print("\n📧 Available Domain Examples:")
        for domain, config in PHISHING_DOMAIN_EXAMPLES.items():
            print(f"\n🔸 {domain} ({config['use_case']})")
            for email in config['emails'][:2]:  # Show first 2 emails
                print(f"   - {email}")
        
        print(f"\n📝 Available Email Templates: {len(EMAIL_TEMPLATES)}")
        for template_name, template in EMAIL_TEMPLATES.items():
            print(f"\n🔸 {template_name}")
            print(f"   Subject: {template['subject']}")
            print(f"   From: {template['from_name']} <{template['from_email']}>")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain examples test failed: {str(e)}")
        return False

def create_sample_domains():
    """
    Sample domains create করে testing এর জন্য
    """
    print("\n" + "=" * 60)
    print("🏗️  Creating Sample Domains for Testing")
    print("=" * 60)
    
    try:
        from campaigns.domain_models import EmailDomain
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # Get or create a test user
        test_user, created = User.objects.get_or_create(
            username='test_admin',
            defaults={
                'email': 'test@example.com',
                'is_staff': True
            }
        )
        
        # Sample domains to create
        sample_domains = [
            {
                'name': 'microsoft-update.com',
                'domain_type': 'spoofing',
                'status': 'verified'
            },
            {
                'name': 'google-security.net',
                'domain_type': 'spoofing', 
                'status': 'verified'
            },
            {
                'name': 'bank-verification.org',
                'domain_type': 'spoofing',
                'status': 'verified'
            },
            {
                'name': 'amazon-delivery.co',
                'domain_type': 'spoofing',
                'status': 'verified'
            }
        ]
        
        created_count = 0
        for domain_data in sample_domains:
            domain, created = EmailDomain.objects.get_or_create(
                name=domain_data['name'],
                defaults={
                    'domain_type': domain_data['domain_type'],
                    'status': domain_data['status'],
                    'created_by': test_user,
                    'emails_sent': 0,
                    'emails_opened': 0,
                    'links_clicked': 0
                }
            )
            
            if created:
                created_count += 1
                print(f"   ✅ Created: {domain.name}")
            else:
                print(f"   ℹ️  Already exists: {domain.name}")
        
        print(f"\n🎉 Sample domains setup complete! Created {created_count} new domains.")
        return True
        
    except Exception as e:
        print(f"❌ Sample domain creation failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🌐 HopeSecure Multi-Domain Campaign System Test")
    print("=" * 60)
    
    # Run all tests
    tests_passed = 0
    total_tests = 3
    
    if create_sample_domains():
        tests_passed += 1
    
    if test_domain_examples():
        tests_passed += 1
    
    if test_multi_domain_system():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All systems are GO! Ready for multi-domain campaigns!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("=" * 60)
