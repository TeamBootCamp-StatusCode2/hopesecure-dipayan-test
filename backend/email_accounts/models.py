"""
Email Accounts Models
Manages custom email accounts for domains
"""
from django.db import models
from django.contrib.auth import get_user_model
from campaigns.domain_models import EmailDomain

User = get_user_model()

class EmailAccount(models.Model):
    """
    Custom email accounts for domains (e.g., admin@hopesecure.tech)
    """
    ACCOUNT_TYPES = [
        ('admin', 'Admin'),
        ('support', 'Support'),
        ('security', 'Security'),
        ('noreply', 'No Reply'),
        ('custom', 'Custom'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    # Basic Info
    username = models.CharField(max_length=100)  # 'admin', 'support', etc.
    domain = models.ForeignKey(EmailDomain, on_delete=models.CASCADE, related_name='email_accounts')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='custom')
    
    # Full email address (computed)
    @property
    def email_address(self):
        return f"{self.username}@{self.domain.name}"
    
    # Account Management
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Usage Stats
    emails_sent = models.IntegerField(default=0)
    emails_received = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Configuration
    auto_reply_enabled = models.BooleanField(default=False)
    auto_reply_message = models.TextField(blank=True)
    forward_to_email = models.EmailField(blank=True, null=True)
    
    class Meta:
        unique_together = ['username', 'domain']
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email_address


class EmailAlias(models.Model):
    """
    Email aliases (e.g., info@domain.com -> admin@domain.com)
    """
    alias_name = models.CharField(max_length=100)  # 'info', 'contact', etc.
    domain = models.ForeignKey(EmailDomain, on_delete=models.CASCADE)
    target_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def alias_email(self):
        return f"{self.alias_name}@{self.domain.name}"
    
    class Meta:
        unique_together = ['alias_name', 'domain']
    
    def __str__(self):
        return f"{self.alias_email} -> {self.target_account.email_address}"


class IncomingEmail(models.Model):
    """
    Store incoming emails for webmail interface
    """
    # Email Headers
    account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name='received_emails')
    from_email = models.EmailField()
    from_name = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=500)
    
    # Content
    text_content = models.TextField(blank=True)
    html_content = models.TextField(blank=True)
    
    # Metadata
    received_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    message_id = models.CharField(max_length=500, unique=True)
    
    # Attachments info (for future)
    has_attachments = models.BooleanField(default=False)
    attachment_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-received_at']
    
    def __str__(self):
        return f"{self.subject} from {self.from_email}"


class SentEmail(models.Model):
    """
    Store sent emails for webmail interface
    """
    account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name='sent_emails')
    to_emails = models.JSONField()  # List of recipient emails
    cc_emails = models.JSONField(default=list, blank=True)
    bcc_emails = models.JSONField(default=list, blank=True)
    
    subject = models.CharField(max_length=500)
    text_content = models.TextField(blank=True)
    html_content = models.TextField(blank=True)
    
    sent_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=50, default='sent')
    sendgrid_message_id = models.CharField(max_length=200, blank=True)
    
    # Campaign relation (optional)
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.subject} to {', '.join(self.to_emails[:3])}"
