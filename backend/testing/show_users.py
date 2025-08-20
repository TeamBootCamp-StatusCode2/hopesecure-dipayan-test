#!/usr/bin/env python
"""
Show all users in the database
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from authentication.models import User
from organization.models import Company

def show_users():
    print("=== User List ===")
    users = User.objects.all().order_by('created_at')
    
    if not users:
        print("No users found in the database.")
        return
    
    print(f"Total users: {users.count()}")
    print("-" * 80)
    
    for user in users:
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Username: {user.username}")
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"Role: {user.role}")
        print(f"Department: {user.department}")
        print(f"Phone: {user.phone_number}")
        print(f"Is Super Admin: {user.is_superuser}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Organization: {user.organization.name if user.organization else 'None'}")
        print(f"Email Verified: {user.is_email_verified}")
        print(f"Created: {user.created_at}")
        print(f"Last Login: {user.last_login}")
        print("-" * 80)

if __name__ == "__main__":
    show_users()
