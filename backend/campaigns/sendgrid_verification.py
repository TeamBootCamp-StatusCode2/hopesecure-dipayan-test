"""
SendGrid Sender Verification Management
Automatically handle sender verification through API
"""

import os
import json
import django
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

class SendGridVerificationManager:
    def __init__(self):
        self.api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        self.sg = SendGridAPIClient(api_key=self.api_key)
    
    def create_verified_sender(self, email, name, reply_to=None):
        """
        Create a new verified sender
        """
        if not reply_to:
            reply_to = email
            
        data = {
            "nickname": name.lower().replace(" ", "_"),
            "from_email": email,
            "from_name": name,
            "reply_to": reply_to,
            "reply_to_name": name,
            "address": "HopeSecure Security Training",
            "address2": "Digital Security Division",
            "city": "Dhaka",
            "state": "Dhaka",
            "country": "Bangladesh",
            "zip": "1000"
        }
        
        try:
            response = self.sg.client.verified_senders.post(request_body=data)
            result = json.loads(response.body.decode('utf-8'))
            print(f"✅ Sender created: {email}")
            print(f"📧 Verification email sent to: {email}")
            print(f"🆔 Sender ID: {result.get('id')}")
            return result
        except Exception as e:
            print(f"❌ Error creating sender: {e}")
            if hasattr(e, 'body'):
                error_data = json.loads(e.body.decode('utf-8'))
                print(f"Error details: {error_data}")
            return None
    
    def resend_verification(self, sender_id):
        """
        Resend verification email for a specific sender
        """
        try:
            response = self.sg.client.verified_senders._(sender_id).resend.post()
            print(f"✅ Verification email resent for sender ID: {sender_id}")
            return True
        except Exception as e:
            print(f"❌ Error resending verification: {e}")
            return False
    
    def get_verified_senders(self):
        """
        Get all verified senders with their status
        """
        try:
            response = self.sg.client.verified_senders.get()
            data = json.loads(response.body.decode('utf-8'))
            
            print("📋 Current Verified Senders:")
            print("=" * 50)
            
            for sender in data.get('results', []):
                status = "✅ VERIFIED" if sender.get('verified') else "⏳ PENDING"
                print(f"Email: {sender.get('from_email')}")
                print(f"Name: {sender.get('from_name')}")
                print(f"Status: {status}")
                print(f"ID: {sender.get('id')}")
                print("-" * 30)
            
            return data.get('results', [])
        except Exception as e:
            print(f"❌ Error getting senders: {e}")
            return []
    
    def delete_sender(self, sender_id):
        """
        Delete a verified sender
        """
        try:
            response = self.sg.client.verified_senders._(sender_id).delete()
            print(f"✅ Sender deleted: {sender_id}")
            return True
        except Exception as e:
            print(f"❌ Error deleting sender: {e}")
            return False
    
    def setup_common_senders(self):
        """
        Setup commonly used sender emails for the project
        """
        common_senders = [
            {
                "email": "noreply@hopesecure.tech",
                "name": "HopeSecure Security",
                "reply_to": "support@hopesecure.tech"
            },
            {
                "email": "alerts@hopesecure.tech", 
                "name": "HopeSecure Alerts",
                "reply_to": "support@hopesecure.tech"
            },
            {
                "email": "training@hopesecure.tech",
                "name": "HopeSecure Training",
                "reply_to": "support@hopesecure.tech"
            }
        ]
        
        print("🚀 Setting up common sender emails...")
        for sender in common_senders:
            self.create_verified_sender(
                email=sender["email"],
                name=sender["name"],
                reply_to=sender["reply_to"]
            )
    
    def verify_domain_authentication(self):
        """
        Check domain authentication status
        """
        try:
            response = self.sg.client.whitelabel.domains.get()
            domains = json.loads(response.body.decode('utf-8'))
            
            print("🌐 Domain Authentication Status:")
            print("=" * 40)
            
            if not domains:
                print("❌ No domains configured")
                print("💡 Tip: Add domain authentication for better deliverability")
                return False
            
            for domain in domains:
                status = "✅ VERIFIED" if domain.get('valid') else "⏳ PENDING"
                print(f"Domain: {domain.get('domain')}")
                print(f"Status: {status}")
                print(f"Default: {domain.get('default')}")
                print("-" * 30)
            
            return True
        except Exception as e:
            print(f"❌ Error checking domains: {e}")
            return False

def main():
    """
    Main function to run verification management
    """
    print("🔐 SendGrid Verification Manager")
    print("=" * 40)
    
    manager = SendGridVerificationManager()
    
    # Show current status
    print("\n1️⃣ Current Verified Senders:")
    senders = manager.get_verified_senders()
    
    print("\n2️⃣ Domain Authentication:")
    manager.verify_domain_authentication()
    
    # Setup new senders if needed
    print("\n3️⃣ Available Actions:")
    print("- Add common sender emails")
    print("- Resend verification emails")
    print("- Check verification status")
    
    return manager

if __name__ == "__main__":
    main()
