"""
Simple test script to verify the global stats endpoint
"""
import requests
import json

def test_global_stats():
    print("🔍 Testing global stats endpoint...")
    
    try:
        response = requests.get('http://127.0.0.1:8000/api/campaigns/global-stats/')
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully fetched global statistics:")
            print(f"   📊 Detection Rate: {data.get('detection_rate')}%")
            print(f"   📧 Tests Conducted: {data.get('tests_conducted'):,}")
            print(f"   🏢 Enterprise Clients: {data.get('enterprise_clients')}")
            print(f"   📈 Total Campaigns: {data.get('total_campaigns')}")
            print(f"   🕒 Last Updated: {data.get('last_updated')}")
            
            # Calculate some insights
            if data.get('tests_conducted', 0) > 0:
                if data.get('tests_conducted') >= 1000:
                    formatted_tests = f"{data.get('tests_conducted')/1000:.1f}K+"
                else:
                    formatted_tests = str(data.get('tests_conducted'))
                print(f"   💡 Formatted Tests: {formatted_tests}")
            
        else:
            print(f"❌ Failed to fetch stats. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")

if __name__ == "__main__":
    test_global_stats()
