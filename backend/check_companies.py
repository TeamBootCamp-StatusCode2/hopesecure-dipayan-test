#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from organization.models import Company

User = get_user_model()

print("=== Current Company Data ===")
companies = Company.objects.all()
print(f"Total companies: {companies.count()}")

for company in companies:
    print(f"Company ID: {company.id}")
    print(f"Company Name: {company.name}")
    print(f"Created by: {company.created_by.email if company.created_by else 'None'}")
    print(f"Domain: {company.domain}")
    print("---")

print("\n=== Testing User Company Access ===")
users = User.objects.all()
for user in users:
    print(f"User: {user.email}")
    try:
        user_company = Company.get_user_company(user)
        print(f"  Company ID: {user_company.id}")
        print(f"  Company Name: {user_company.name}")
        print(f"  Company Domain: {user_company.domain}")
    except Exception as e:
        print(f"  Error: {e}")
    print("---")
