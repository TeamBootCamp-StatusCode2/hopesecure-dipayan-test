#!/usr/bin/env python
"""
Debug activity logs API issue
"""

import os
import sys
import django

# Setup Django
os.environ['USE_POSTGRES'] = 'True'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from authentication.models import User, ActivityLog
from django.utils import timezone
from datetime import timedelta

def debug_activity_logs():
    """Debug activity logs issue"""
    
    print("🔍 Debugging activity logs...")
    
    # Get super admin user
    try:
        admin_user = User.objects.get(email='admin@test.com')
        print(f"✅ Admin user: {admin_user.email}")
        print(f"   Is superuser: {admin_user.is_superuser}")
        print(f"   Has organization attr: {hasattr(admin_user, 'organization')}")
        print(f"   Organization: {admin_user.organization}")
    except Exception as e:
        print(f"❌ Error getting admin user: {e}")
        return
    
    # Check activity logs
    try:
        logs_count = ActivityLog.objects.count()
        print(f"📊 Total activity logs: {logs_count}")
        
        # Try to get logs with time filter
        last_7d = timezone.now() - timedelta(days=7)
        recent_logs = ActivityLog.objects.filter(timestamp__gte=last_7d)
        print(f"📊 Logs in last 7 days: {recent_logs.count()}")
        
        # Show first few logs
        print("📝 Sample logs:")
        for i, log in enumerate(recent_logs[:3]):
            print(f"   {i+1}. {log.user} - {log.action_type} - {log.timestamp}")
    except Exception as e:
        print(f"❌ Error accessing activity logs: {e}")
    
    # Test the filter logic from views
    try:
        print("🧪 Testing filter logic...")
        logs_qs = ActivityLog.objects.all()
        
        if not admin_user.is_superuser:
            if hasattr(admin_user, 'organization') and admin_user.organization:
                logs_qs = logs_qs.filter(organization=admin_user.organization)
                print("   Filtered by organization")
            else:
                logs_qs = logs_qs.none()
                print("   No organization - returning empty queryset")
        else:
            print("   Super admin - showing all logs")
        
        print(f"   Filtered logs count: {logs_qs.count()}")
        
    except Exception as e:
        print(f"❌ Error in filter logic: {e}")

if __name__ == '__main__':
    debug_activity_logs()
