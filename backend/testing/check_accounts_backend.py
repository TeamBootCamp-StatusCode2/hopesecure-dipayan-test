#!/usr/bin/env python
"""
Check current accounts and organizations in the system
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from organization.models import Company

User = get_user_model()

def check_accounts():
    print("=== Current System Status ===")
    
    # Get all users
    users = User.objects.all().order_by('created_at')
    print(f"\n📊 Total User Accounts: {users.count()}")
    
    if users.exists():
        print("\n👤 User Details:")
        for i, user in enumerate(users, 1):
            org_name = user.organization.name if user.organization else "No Organization"
            print(f"   {i}. {user.email}")
            print(f"      Name: {user.first_name} {user.last_name}")
            print(f"      Role: {user.role}")
            print(f"      Organization: {org_name}")
            print(f"      Created: {user.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    # Get all organizations/companies
    companies = Company.objects.all().order_by('created_at')
    print(f"🏢 Total Organizations: {companies.count()}")
    
    if companies.exists():
        print("\n🏢 Organization Details:")
        for i, company in enumerate(companies, 1):
            user_count = company.users.count()
            admin_email = company.created_by.email if company.created_by else "Unknown"
            print(f"   {i}. {company.name or 'Unnamed Organization'}")
            print(f"      Domain: {company.domain or 'Not set'}")
            print(f"      Industry: {company.get_industry_display()}")
            print(f"      Employee Count: {company.get_employee_count_display()}")
            print(f"      Admin: {admin_email}")
            print(f"      Users in Org: {user_count}")
            print(f"      Created: {company.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    # Summary
    print("=== Summary ===")
    users_with_org = User.objects.filter(organization__isnull=False).count()
    users_without_org = User.objects.filter(organization__isnull=True).count()
    
    print(f"✅ Users with Organizations: {users_with_org}")
    print(f"❌ Users without Organizations: {users_without_org}")
    print(f"🏢 Active Organizations: {companies.count()}")
    
    if users_without_org > 0:
        print(f"\n⚠️  Warning: {users_without_org} users are not linked to any organization!")

if __name__ == "__main__":
    check_accounts()
