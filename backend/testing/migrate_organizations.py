#!/usr/bin/env python
"""
Migration script to link existing users to their organizations
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

def update_existing_data():
    print("=== Linking Users to Organizations ===")
    
    # Get all companies and users
    companies = Company.objects.all()
    users = User.objects.all()
    
    print(f"Found {companies.count()} companies and {users.count()} users")
    
    # Link users to their companies
    for user in users:
        if not user.organization:
            # Find company created by this user
            user_company = companies.filter(created_by=user).first()
            if user_company:
                user.organization = user_company
                user.save()
                print(f"Linked user {user.email} to company {user_company.name}")
    
    print("\n=== Linking Employees to Organizations ===")
    # Update employees to link to organizations
    employees = Employee.objects.all()
    for employee in employees:
        if not employee.organization and employee.created_by:
            if employee.created_by.organization:
                employee.organization = employee.created_by.organization
                employee.save()
                print(f"Linked employee {employee.email} to organization {employee.created_by.organization.name}")
    
    print("\n=== Linking Departments to Organizations ===")
    # Update departments to link to organizations
    departments = Department.objects.all()
    for department in departments:
        if not department.organization and department.created_by:
            if department.created_by.organization:
                department.organization = department.created_by.organization
                department.save()
                print(f"Linked department {department.name} to organization {department.created_by.organization.name}")
    
    print("\n=== Linking Campaigns to Organizations ===")
    # Update campaigns to link to organizations
    campaigns = Campaign.objects.all()
    for campaign in campaigns:
        if not campaign.organization and campaign.created_by:
            if campaign.created_by.organization:
                campaign.organization = campaign.created_by.organization
                campaign.save()
                print(f"Linked campaign {campaign.name} to organization {campaign.created_by.organization.name}")
    
    print("\n=== Linking Templates to Organizations ===")
    # Update templates to link to organizations
    templates = Template.objects.all()
    for template in templates:
        if not template.organization and template.created_by:
            if template.created_by.organization:
                template.organization = template.created_by.organization
                template.save()
                print(f"Linked template {template.name} to organization {template.created_by.organization.name}")
    
    print("\n=== Migration Complete ===")

if __name__ == "__main__":
    update_existing_data()
