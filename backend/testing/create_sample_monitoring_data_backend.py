#!/usr/bin/env python
"""
Create sample activity logs and alerts for testing
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ['USE_POSTGRES'] = 'True'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from authentication.models import User, ActivityLog, SystemAlert
from django.utils import timezone

def create_sample_logs():
    """Create sample activity logs"""
    
    print("📝 Creating sample activity logs...")
    
    # Get users
    users = User.objects.all()
    if not users.exists():
        print("❌ No users found. Please create users first.")
        return
    
    # Sample activities
    activities = [
        ('login', 'User successfully logged in', 'low'),
        ('logout', 'User logged out', 'low'),
        ('failed_login', 'Failed login attempt detected', 'medium'),
        ('campaign_created', 'New phishing campaign created', 'medium'),
        ('campaign_started', 'Phishing campaign started', 'high'),
        ('user_created', 'New user account created', 'medium'),
        ('settings_changed', 'System settings modified', 'high'),
        ('phishing_attempt', 'Suspicious phishing attempt detected', 'critical'),
        ('security_alert', 'Security breach attempt', 'critical'),
        ('admin_action', 'Administrative action performed', 'medium'),
    ]
    
    # Create logs for the last 30 days
    for i in range(50):
        user = random.choice(users)
        activity_type, description, severity = random.choice(activities)
        
        # Random timestamp in last 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        timestamp = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
        
        ActivityLog.objects.create(
            user=user,
            organization=user.organization,
            action_type=activity_type,
            description=f"{description} by {user.full_name}",
            severity=severity,
            ip_address=f"192.168.1.{random.randint(1, 254)}",
            user_agent="Mozilla/5.0 (Test User Agent)",
            metadata={
                'source': 'test_data',
                'action_id': f"action_{i}",
                'additional_info': f"Sample log entry {i}"
            },
            timestamp=timestamp
        )
    
    print(f"✅ Created {ActivityLog.objects.count()} activity logs")

def create_sample_alerts():
    """Create sample system alerts"""
    
    print("🚨 Creating sample system alerts...")
    
    # Sample alerts
    alerts_data = [
        ('security', 'Suspicious Login Activity', 'Multiple failed login attempts detected from IP 192.168.1.100', 'high', 'active'),
        ('security', 'Potential Phishing Attack', 'Unusual email activity detected in organization', 'critical', 'active'),
        ('performance', 'High CPU Usage', 'Server CPU usage above 80% for extended period', 'medium', 'resolved'),
        ('system', 'Database Connection Issue', 'Temporary database connectivity problems detected', 'high', 'resolved'),
        ('user_activity', 'Unusual User Behavior', 'User accessing resources outside normal hours', 'medium', 'active'),
        ('security', 'Malware Detection', 'Potential malware detected in uploaded file', 'critical', 'active'),
        ('performance', 'Slow Response Time', 'API response times above normal thresholds', 'low', 'monitoring'),
        ('system', 'Backup Failure', 'Scheduled backup process failed', 'high', 'active'),
    ]
    
    # Get a super admin user for created_by field
    super_admin = User.objects.filter(is_superuser=True).first()
    
    for i, (alert_type, title, description, severity, status) in enumerate(alerts_data):
        # Random timestamp in last 7 days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        created_at = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
        
        resolved_at = None
        resolved_by = None
        if status == 'resolved':
            resolved_at = created_at + timedelta(hours=random.randint(1, 48))
            resolved_by = super_admin
        
        SystemAlert.objects.create(
            alert_type=alert_type,
            title=title,
            description=description,
            severity=severity,
            status=status,
            organization=None,  # System-wide alerts
            created_by=super_admin,
            resolved_at=resolved_at,
            resolved_by=resolved_by,
            created_at=created_at
        )
    
    print(f"✅ Created {SystemAlert.objects.count()} system alerts")

if __name__ == '__main__':
    print("🔄 Creating sample data for admin monitoring...")
    create_sample_logs()
    create_sample_alerts()
    print("🎉 Sample data creation completed!")
