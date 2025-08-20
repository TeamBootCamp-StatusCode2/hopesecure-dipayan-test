#!/usr/bin/env python
"""
Password Reset Script for migrated users
"""

import os
import sys
import django

# Setup Django
os.environ['USE_POSTGRES'] = 'True'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from authentication.models import User

def reset_user_passwords():
    """Reset passwords for all migrated users"""
    
    # User password mapping
    user_passwords = {
        'speed@lol.com': 'speed123',
        'pou@lol.com': 'pou123', 
        'pem@lol.com': 'pem123',
        'admin@test.com': 'admin123',
        'admin@hopesecure.com': 'admin123'
    }
    
    print("🔑 Resetting passwords for migrated users...")
    
    for email, password in user_passwords.items():
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            print(f"✅ Password reset for {email} -> {password}")
        except User.DoesNotExist:
            print(f"❌ User {email} not found")
        except Exception as e:
            print(f"❌ Error resetting password for {email}: {e}")
    
    print(f"\n🎉 Password reset completed!")
    print(f"📊 Total users: {User.objects.count()}")

if __name__ == '__main__':
    reset_user_passwords()
