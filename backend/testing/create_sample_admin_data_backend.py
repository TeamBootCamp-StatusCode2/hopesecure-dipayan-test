#!/usr/bin/env python
"""
Create sample activity logs and alerts for testing the admin dashboard
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from authentication.models import ActivityLog, SystemAlert
from organization.models import Company

User = get_user_model()

def create_sample_logs():
    """Create sample activity logs"""
    print("Creating sample activity logs...")
    
    # Get some users and organizations
    users = User.objects.all()[:5]
    organizations = Company.objects.all()
    
    if not users.exists():
        print("No users found. Please create users first.")
        return
    
    # Sample log entries
    sample_logs = [
        {
            'user': users[0],
            'organization': users[0].organization,
            'action_type': 'login',
            'description': f'User {users[0].email} logged in successfully',
            'severity': 'low',
            'ip_address': '192.168.1.100',
        },
        {
            'user': users[1],
            'organization': users[1].organization,
            'action_type': 'campaign_created',
            'description': f'User {users[1].email} created a new phishing campaign',
            'severity': 'medium',
            'ip_address': '192.168.1.101',
        },
        {
            'user': users[0],
            'organization': users[0].organization,
            'action_type': 'failed_login',
            'description': f'Failed login attempt for {users[0].email}',
            'severity': 'medium',
            'ip_address': '10.0.0.15',
        },
        {
            'user': None,
            'organization': organizations[0] if organizations else None,
            'action_type': 'phishing_attempt',
            'description': 'Suspicious phishing attempt detected from external source',
            'severity': 'high',
            'ip_address': '203.0.113.195',
        },
        {
            'user': users[2] if len(users) > 2 else users[0],
            'organization': users[2].organization if len(users) > 2 else users[0].organization,
            'action_type': 'security_alert',
            'description': 'Multiple failed login attempts detected',
            'severity': 'critical',
            'ip_address': '198.51.100.42',
        },
        {
            'user': users[1],
            'organization': users[1].organization,
            'action_type': 'password_changed',
            'description': f'User {users[1].email} changed their password',
            'severity': 'low',
            'ip_address': '192.168.1.105',
        },
        {
            'user': users[0],
            'organization': users[0].organization,
            'action_type': 'campaign_completed',
            'description': 'Phishing awareness campaign completed successfully',
            'severity': 'low',
            'ip_address': '192.168.1.100',
        },
        {
            'user': None,
            'organization': None,
            'action_type': 'system_error',
            'description': 'Database connection timeout detected',
            'severity': 'high',
            'ip_address': None,
        },
    ]
    
    # Create logs with varying timestamps
    now = timezone.now()
    for i, log_data in enumerate(sample_logs):
        # Spread logs over the last 7 days
        timestamp = now - timedelta(days=i % 7, hours=i * 2, minutes=i * 15)
        
        log = ActivityLog.objects.create(
            user=log_data['user'],
            organization=log_data['organization'],
            action_type=log_data['action_type'],
            description=log_data['description'],
            severity=log_data['severity'],
            ip_address=log_data['ip_address'],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            metadata={'sample': True, 'test_data': True}
        )
        log.timestamp = timestamp
        log.save()
    
    print(f"Created {len(sample_logs)} sample activity logs")


def create_sample_alerts():
    """Create sample system alerts"""
    print("Creating sample system alerts...")
    
    organizations = Company.objects.all()
    users = User.objects.filter(role__in=['admin', 'super_admin'])
    
    sample_alerts = [
        {
            'alert_type': 'security',
            'title': 'Multiple Failed Login Attempts',
            'description': 'More than 10 failed login attempts detected from IP 198.51.100.42 in the last hour',
            'severity': 'high',
            'organization': organizations[0] if organizations else None,
            'created_by': users[0] if users else None,
        },
        {
            'alert_type': 'system',
            'title': 'High Memory Usage',
            'description': 'System memory usage exceeded 85% threshold',
            'severity': 'medium',
            'organization': None,  # System-wide
            'created_by': None,  # Auto-generated
        },
        {
            'alert_type': 'user_activity',
            'title': 'Unusual Login Pattern',
            'description': 'User logged in from an unusual geographic location',
            'severity': 'medium',
            'organization': organizations[1] if len(organizations) > 1 else organizations[0] if organizations else None,
            'created_by': users[0] if users else None,
        },
        {
            'alert_type': 'data_breach',
            'title': 'Potential Data Breach Detected',
            'description': 'Unauthorized access attempt to sensitive data detected',
            'severity': 'critical',
            'organization': organizations[0] if organizations else None,
            'created_by': users[0] if users else None,
            'status': 'investigating',
        },
        {
            'alert_type': 'campaign',
            'title': 'Campaign Performance Issue',
            'description': 'Phishing campaign showing unusually low engagement rates',
            'severity': 'low',
            'organization': organizations[2] if len(organizations) > 2 else organizations[0] if organizations else None,
            'created_by': users[0] if users else None,
            'status': 'resolved',
        },
    ]
    
    now = timezone.now()
    for i, alert_data in enumerate(sample_alerts):
        # Create alerts with varying timestamps
        created_at = now - timedelta(days=i, hours=i * 3)
        
        alert = SystemAlert.objects.create(
            alert_type=alert_data['alert_type'],
            title=alert_data['title'],
            description=alert_data['description'],
            severity=alert_data['severity'],
            organization=alert_data['organization'],
            created_by=alert_data['created_by'],
            status=alert_data.get('status', 'active'),
        )
        alert.created_at = created_at
        alert.save()
        
        # Resolve some alerts
        if alert_data.get('status') == 'resolved':
            alert.resolved_at = created_at + timedelta(hours=6)
            alert.resolved_by = alert_data['created_by']
            alert.save()
    
    print(f"Created {len(sample_alerts)} sample system alerts")


def main():
    """Main function to create all sample data"""
    print("🔧 Creating sample data for admin dashboard...")
    
    try:
        create_sample_logs()
        create_sample_alerts()
        
        print("\n✅ Sample data created successfully!")
        print("\nSample data includes:")
        print("- Activity logs with various severity levels")
        print("- System alerts for different scenarios")
        print("- Failed login attempts and security events")
        print("- Campaign and user activity logs")
        print("\n🎯 You can now test the admin dashboard with realistic data!")
        
    except Exception as e:
        print(f"\n❌ Error creating sample data: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()
