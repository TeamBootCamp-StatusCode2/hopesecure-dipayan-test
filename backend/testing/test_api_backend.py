"""
Simple script to test the API endpoints
Run this after starting the Django server
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_api():
    print("🧪 Testing HopeSecure Backend API")
    print("=" * 50)
    
    # Test user registration
    print("\n1. Testing User Registration...")
    register_data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpassword123',
        'password_confirm': 'testpassword123',
        'role': 'analyst',
        'department': 'IT'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=register_data)
        if response.status_code == 201:
            print("✅ Registration successful")
            token = response.json().get('token')
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test authentication headers
    headers = {'Authorization': f'Token {token}'}
    
    # Test templates endpoint
    print("\n2. Testing Templates Endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/templates/', headers=headers)
        if response.status_code == 200:
            templates = response.json()
            print(f"✅ Found {len(templates)} templates")
        else:
            print(f"❌ Templates request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Templates error: {e}")
    
    # Test campaigns endpoint
    print("\n3. Testing Campaigns Endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/campaigns/', headers=headers)
        if response.status_code == 200:
            campaigns = response.json()
            print(f"✅ Found {len(campaigns)} campaigns")
        else:
            print(f"❌ Campaigns request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Campaigns error: {e}")
    
    # Test employees endpoint
    print("\n4. Testing Employees Endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/employees/', headers=headers)
        if response.status_code == 200:
            employees = response.json()
            print(f"✅ Found {len(employees)} employees")
        else:
            print(f"❌ Employees request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Employees error: {e}")
    
    # Test dashboard stats
    print("\n5. Testing Dashboard Stats...")
    try:
        response = requests.get(f'{BASE_URL}/auth/dashboard/stats/', headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Dashboard stats retrieved")
            print(f"   - User role: {stats.get('role', 'N/A')}")
            print(f"   - Total campaigns: {stats.get('total_campaigns', 'N/A')}")
            print(f"   - Total templates: {stats.get('total_templates', 'N/A')}")
        else:
            print(f"❌ Dashboard stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard stats error: {e}")
    
    print("\n🎉 API testing completed!")
    print("💡 The backend is ready for frontend integration")

if __name__ == '__main__':
    test_api()
