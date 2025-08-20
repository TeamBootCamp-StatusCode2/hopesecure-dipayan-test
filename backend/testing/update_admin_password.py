#!/usr/bin/env python
"""
Update admin password to admin123
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from authentication.models import User

try:
    user = User.objects.get(email='admin@test.com')
    user.set_password('admin123')
    user.save()
    print("✅ Password updated successfully for admin@test.com")
    print(f"✅ New credentials - Email: admin@test.com, Password: admin123")
except User.DoesNotExist:
    print("❌ User admin@test.com not found")
except Exception as e:
    print(f"❌ Error: {e}")
