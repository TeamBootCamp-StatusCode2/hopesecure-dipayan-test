#!/usr/bin/env python3

import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000/api/campaigns/domains"
    
    print("🧪 Testing Domain API")
    print("=" * 50)
    
    # Test 1: Domain suggestions
    print("\n📝 Test 1: Domain Suggestions")
    try:
        response = requests.get(f"{base_url}/api/domain-suggestions/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('success')}")
            print(f"✅ Got {len(data.get('suggestions', []))} suggestions")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: List domains
    print("\n📋 Test 2: List Domains")
    try:
        response = requests.get(f"{base_url}/api/domains/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('success')}")
            print(f"✅ Found {len(data.get('domains', []))} domains")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Add domain
    print("\n➕ Test 3: Add Domain")
    try:
        test_domain = {
            "name": "test-secure-email.com",
            "domain_type": "spoofing"
        }
        response = requests.post(
            f"{base_url}/api/domains/",
            json=test_domain,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get('success'):
            print("✅ Domain added successfully!")
        else:
            print(f"❌ Failed: {data.get('message')}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_api()
