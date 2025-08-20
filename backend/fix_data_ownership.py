#!/usr/bin/env python
"""
Script to fix data ownership and ensure proper user isolation.
This script will update existing data to have proper created_by fields.
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from authentication.models import User
from templates.models import Template
from employees.models import Employee, Department
from campaigns.models import Campaign

def fix_data_ownership():
    """Fix existing data to have proper user ownership"""
    
    # Get all users
    users = User.objects.all()
    print(f"Found {users.count()} users")
    
    # For demonstration, we'll assign existing data to the first user
    # In production, you might want a more sophisticated approach
    if users.exists():
        default_user = users.first()
        print(f"Assigning orphaned data to user: {default_user.email}")
        
        # Fix templates without created_by
        orphaned_templates = Template.objects.filter(created_by__isnull=True)
        if orphaned_templates.exists():
            orphaned_templates.update(created_by=default_user)
            print(f"Fixed {orphaned_templates.count()} templates")
        
        # Fix employees without created_by
        orphaned_employees = Employee.objects.filter(created_by__isnull=True)
        if orphaned_employees.exists():
            orphaned_employees.update(created_by=default_user)
            print(f"Fixed {orphaned_employees.count()} employees")
        
        # Fix departments without created_by
        orphaned_departments = Department.objects.filter(created_by__isnull=True)
        if orphaned_departments.exists():
            orphaned_departments.update(created_by=default_user)
            print(f"Fixed {orphaned_departments.count()} departments")
        
        # Fix campaigns without created_by
        orphaned_campaigns = Campaign.objects.filter(created_by__isnull=True)
        if orphaned_campaigns.exists():
            orphaned_campaigns.update(created_by=default_user)
            print(f"Fixed {orphaned_campaigns.count()} campaigns")
        
        print("Data ownership fixed successfully!")
    else:
        print("No users found. Please create a user first.")

def clear_all_user_data():
    """Clear all user-created data (use with caution!)"""
    print("WARNING: This will delete ALL user data!")
    confirm = input("Are you sure? Type 'yes' to continue: ")
    
    if confirm.lower() == 'yes':
        Template.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()
        Campaign.objects.all().delete()
        print("All user data cleared!")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_all_user_data()
    else:
        fix_data_ownership()
