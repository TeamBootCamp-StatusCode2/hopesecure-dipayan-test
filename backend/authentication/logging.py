"""
Activity Logging System for Admin Dashboard
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()


class ActivityLog(models.Model):
    """Track all important system activities for admin monitoring"""
    ACTION_TYPES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('campaign_created', 'Campaign Created'),
        ('campaign_started', 'Campaign Started'),
        ('campaign_completed', 'Campaign Completed'),
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('organization_created', 'Organization Created'),
        ('organization_updated', 'Organization Updated'),
        ('template_created', 'Template Created'),
        ('template_used', 'Template Used'),
        ('phishing_attempt', 'Phishing Attempt Detected'),
        ('security_alert', 'Security Alert'),
        ('admin_action', 'Admin Action'),
        ('system_error', 'System Error'),
        ('data_export', 'Data Export'),
        ('settings_changed', 'Settings Changed'),
        ('password_changed', 'Password Changed'),
        ('failed_login', 'Failed Login Attempt'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey('organization.Company', on_delete=models.CASCADE, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='low')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Additional data
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['action_type', 'timestamp']),
            models.Index(fields=['organization', 'timestamp']),
            models.Index(fields=['severity', 'timestamp']),
        ]
    
    def __str__(self):
        user_info = f"{self.user.email}" if self.user else "System"
        return f"{user_info} - {self.get_action_type_display()} ({self.timestamp})"


class SystemAlert(models.Model):
    """System-wide alerts for admin monitoring"""
    ALERT_TYPES = [
        ('security', 'Security Alert'),
        ('performance', 'Performance Alert'),
        ('system', 'System Alert'),
        ('user_activity', 'User Activity Alert'),
        ('campaign', 'Campaign Alert'),
        ('data_breach', 'Data Breach Alert'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('investigating', 'Investigating'),
        ('dismissed', 'Dismissed'),
    ]
    
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=ActivityLog.SEVERITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    organization = models.ForeignKey('organization.Company', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_alerts')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_severity_display()}"


def log_activity(user=None, organization=None, action_type='admin_action', 
                description='', severity='low', ip_address=None, 
                user_agent='', metadata=None):
    """Helper function to log activities"""
    if metadata is None:
        metadata = {}
    
    ActivityLog.objects.create(
        user=user,
        organization=organization,
        action_type=action_type,
        description=description,
        severity=severity,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata
    )


def create_system_alert(alert_type, title, description, severity='medium', 
                       organization=None, created_by=None):
    """Helper function to create system alerts"""
    SystemAlert.objects.create(
        alert_type=alert_type,
        title=title,
        description=description,
        severity=severity,
        organization=organization,
        created_by=created_by
    )
