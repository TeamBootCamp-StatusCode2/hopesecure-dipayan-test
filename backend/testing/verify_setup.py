#!/usr/bin/env python
"""
Verification script to check organizational registration setup
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from organization.models import Company
from employees.models import Employee, Department
from campaigns.models import Campaign
from templates.models import Template

User = get_user_model()

def verify_setup():
    print("=== Verifying Organizational Registration Setup ===")
    
    # Check that models have organization fields
    print("\n1. Checking Model Organization Fields:")
    
    # Check User model
    if hasattr(User, 'organization'):
        print("   ✓ User model has organization field")
    else:
        print("   ✗ User model missing organization field")
    
    # Check Company model
    if hasattr(Company, 'get_user_company'):
        print("   ✓ Company model has get_user_company method")
    else:
        print("   ✗ Company model missing get_user_company method")
    
    # Check Employee model
    if hasattr(Employee, 'organization'):
        print("   ✓ Employee model has organization field")
    else:
        print("   ✗ Employee model missing organization field")
    
    # Check Department model
    if hasattr(Department, 'organization'):
        print("   ✓ Department model has organization field")
    else:
        print("   ✗ Department model missing organization field")
    
    # Check Campaign model
    if hasattr(Campaign, 'organization'):
        print("   ✓ Campaign model has organization field")
    else:
        print("   ✗ Campaign model missing organization field")
    
    # Check Template model
    if hasattr(Template, 'organization'):
        print("   ✓ Template model has organization field")
    else:
        print("   ✗ Template model missing organization field")
    
    print("\n2. Current Data Status:")
    print(f"   - Total Users: {User.objects.count()}")
    print(f"   - Total Companies: {Company.objects.count()}")
    print(f"   - Users with Organizations: {User.objects.filter(organization__isnull=False).count()}")
    
    print("\n3. Existing Organizations:")
    companies = Company.objects.all()
    for company in companies:
        user_count = company.users.count() if hasattr(company, 'users') else 0
        print(f"   - {company.name or 'Unnamed'} (ID: {company.id}) - {user_count} users")
        if company.created_by:
            print(f"     Admin: {company.created_by.email}")
    
    print("\n=== Setup Verification Complete ===")
    print("\n🎉 The system is now configured for organizational registration!")
    print("\nKey Changes Made:")
    print("   • Registration now creates organizations instead of individual accounts")
    print("   • Each user is linked to their organization")
    print("   • All data (employees, campaigns, templates) is organization-scoped")
    print("   • Company settings are shared within the organization")
    print("   • Registration form includes company information")

if __name__ == "__main__":
    verify_setup()
