from django.db import models
from django.contrib.auth import get_user_model
from templates.models import Template
from .domain_models import EmailDomain

User = get_user_model()


class Campaign(models.Model):
    """Phishing simulation campaigns"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    CAMPAIGN_TYPE_CHOICES = [
        ('credential', 'Credential Phishing'),
        ('data_input', 'Data Input Form'),
        ('link_click', 'Link Click Tracking'),
        ('attachment', 'Fake Attachment'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    campaign_type = models.CharField(max_length=50, choices=CAMPAIGN_TYPE_CHOICES)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='campaigns')
    domain = models.ForeignKey(EmailDomain, on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)  # Add domain field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    target_count = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
    emails_opened = models.IntegerField(default=0)
    links_clicked = models.IntegerField(default=0)
    credentials_submitted = models.IntegerField(default=0)
    data_submitted = models.IntegerField(default=0)
    attachments_downloaded = models.IntegerField(default=0)
    
    # Scheduling
    scheduled_start = models.DateTimeField(blank=True, null=True)
    scheduled_end = models.DateTimeField(blank=True, null=True)
    actual_start = models.DateTimeField(blank=True, null=True)
    actual_end = models.DateTimeField(blank=True, null=True)
    
    # Configuration
    send_reminder = models.BooleanField(default=False)
    reminder_delay_hours = models.IntegerField(default=24)
    track_clicks = models.BooleanField(default=True)
    track_downloads = models.BooleanField(default=True)
    capture_credentials = models.BooleanField(default=True)
    redirect_url = models.URLField(blank=True)
    
    # Metadata
    organization = models.ForeignKey('organization.Company', on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def success_rate(self):
        """Calculate campaign success rate"""
        if self.emails_sent == 0:
            return 0
        return round((self.credentials_submitted / self.emails_sent) * 100, 2)
    
    @property
    def open_rate(self):
        """Calculate email open rate"""
        if self.emails_sent == 0:
            return 0
        return round((self.emails_opened / self.emails_sent) * 100, 2)
    
    @property
    def click_rate(self):
        """Calculate click-through rate"""
        if self.emails_sent == 0:
            return 0
        return round((self.links_clicked / self.emails_sent) * 100, 2)


class CampaignTarget(models.Model):
    """Individual targets for a campaign"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Email Sent'),
        ('opened', 'Email Opened'),
        ('clicked', 'Link Clicked'),
        ('submitted', 'Data Submitted'),
        ('downloaded', 'Attachment Downloaded'),
        ('failed', 'Failed'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='targets')
    email = models.EmailField()
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Tracking
    email_sent_at = models.DateTimeField(blank=True, null=True)
    email_opened_at = models.DateTimeField(blank=True, null=True)
    link_clicked_at = models.DateTimeField(blank=True, null=True)
    data_submitted_at = models.DateTimeField(blank=True, null=True)
    attachment_downloaded_at = models.DateTimeField(blank=True, null=True)
    
    # User agent and IP tracking
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['campaign', 'email']
    
    def __str__(self):
        return f"{self.email} - {self.campaign.name}"


class CampaignEvent(models.Model):
    """Track individual events during campaigns"""
    EVENT_TYPE_CHOICES = [
        ('email_sent', 'Email Sent'),
        ('email_opened', 'Email Opened'),
        ('link_clicked', 'Link Clicked'),
        ('form_submitted', 'Form Submitted'),
        ('attachment_downloaded', 'Attachment Downloaded'),
        ('page_visited', 'Page Visited'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='events')
    target = models.ForeignKey(CampaignTarget, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    additional_data = models.JSONField(blank=True, null=True)  # Store form data, etc.
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.event_type} - {self.target.email} - {self.timestamp}"
