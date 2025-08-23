"""
Test Simple Domain API
Quick test to verify domain functionality
"""

import os
import sys
import django
import requests
import json

# Add Django project to path
sys.path.append('/home/shuvo/Desktop/PHISX/hopesecure-dipayan-test/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')

django.setup()

def test_domain_api():
    """
    Test the simple domain API endpoints
    """
    base_url = "http://127.0.0.1:8080/api/campaigns/domains"
    
    print("🧪 Testing Simple Domain API")
    print("=" * 50)
    
    # Test 1: Get domain suggestions
    print("\n📝 Test 1: Domain Suggestions")
    try:
        response = requests.get(f"{base_url}/api/domain-suggestions/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Got {len(data.get('suggestions', []))} suggestions")
            for suggestion in data.get('suggestions', [])[:3]:
                print(f"   - {suggestion['domain']} ({suggestion['type']})")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Validate domain
    print("\n🔍 Test 2: Domain Validation")
    try:
        test_data = {"domain_name": "test-secure.com"}
        response = requests.post(
            f"{base_url}/api/validate-domain/", 
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Validation result: {data}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: List domains
    print("\n📋 Test 3: List Domains")
    try:
        response = requests.get(f"{base_url}/api/domains/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data.get('domains', []))} domains")
            for domain in data.get('domains', []):
                print(f"   - {domain['name']} ({domain['status']})")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 4: Add domain
    print("\n➕ Test 4: Add Domain")
    try:
        test_domain = {
            "name": f"test-phishing-{int(__import__('time').time())}.com",
            "domain_type": "spoofing"
        }
        response = requests.post(
            f"{base_url}/api/domains/", 
            json=test_domain,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Domain added: {test_domain['name']}")
                domain_id = data.get('data', {}).get('domain_id')
                
                # Test DNS records
                if domain_id:
                    print(f"\n🔍 Test 5: DNS Records for Domain {domain_id}")
                    dns_response = requests.get(f"{base_url}/api/domains/{domain_id}/dns_records/")
                    if dns_response.status_code == 200:
                        dns_data = dns_response.json()
                        print(f"✅ Found {len(dns_data.get('dns_records', []))} DNS records")
                    else:
                        print(f"❌ DNS fetch failed: {dns_response.text}")
            else:
                print(f"❌ Failed to add domain: {data.get('message')}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Domain API Test Completed!")

if __name__ == "__main__":
    test_domain_api()
