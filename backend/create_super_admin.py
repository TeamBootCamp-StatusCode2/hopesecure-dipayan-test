#!/usr/bin/env python
"""
Create super admin user: admin@test.com with password 'admin'
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from authentication.models import UserProfile

User = get_user_model()

def create_super_admin():
    print("=== Creating Super Admin ===")
    
    email = "admin@test.com"
    password = "admin"
    
    # Check if super admin already exists
    if User.objects.filter(email=email).exists():
        print(f"❌ Super admin with email {email} already exists!")
        user = User.objects.get(email=email)
        # Update to super admin role if not already
        if user.role != 'super_admin':
            user.role = 'super_admin'
            user.save()
            print(f"✅ Updated existing user {email} to super_admin role")
        else:
            print(f"✅ User {email} is already a super admin")
        return user
    
    try:
        # Create super admin user
        user = User.objects.create_user(
            email=email,
            username="superadmin",
            password=password,
            first_name="Super",
            last_name="Admin",
            role="super_admin",
            department="System Administration",
            phone_number="",
            is_staff=True,  # Django admin access
            is_superuser=True  # Django superuser
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        print(f"✅ Super admin created successfully!")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Role: {user.role}")
        print(f"   Django Admin Access: {user.is_staff}")
        print(f"   Django Superuser: {user.is_superuser}")
        
        return user
        
    except Exception as e:
        print(f"❌ Failed to create super admin: {str(e)}")
        return None

def test_super_admin_access():
    print("\n=== Testing Super Admin Access ===")
    
    try:
        admin_user = User.objects.get(email="admin@test.com")
        
        print(f"Super Admin Properties:")
        print(f"   is_super_admin: {admin_user.is_super_admin}")
        print(f"   is_org_admin: {admin_user.is_org_admin}")
        print(f"   is_staff: {admin_user.is_staff}")
        print(f"   is_superuser: {admin_user.is_superuser}")
        print(f"   organization: {admin_user.organization}")
        
        # Test access to all organizations
        from organization.models import Company
        companies = Company.get_all_companies()
        print(f"   Can access {companies.count()} organizations")
        
        print("✅ Super admin access verified!")
        
    except Exception as e:
        print(f"❌ Failed to test super admin access: {str(e)}")

if __name__ == "__main__":
    user = create_super_admin()
    if user:
        test_super_admin_access()
        
        print("\n=== Super Admin Access Summary ===")
        print("🔐 Login Credentials:")
        print("   Email: admin@test.com")
        print("   Password: admin")
        print("\n🔧 Super Admin Capabilities:")
        print("   • View all organizations and their data")
        print("   • Access system-wide statistics")
        print("   • Manage all users across organizations")
        print("   • View all campaigns, templates, employees")
        print("   • Django admin panel access")
        print("   • System monitoring and management")
        print("\n🌐 API Endpoints:")
        print("   • GET /api/organization/admin/organizations/ - All organizations")
        print("   • GET /api/organization/admin/stats/ - System statistics")
        print("   • GET /api/organization/company/ - Enhanced view for super admin")
