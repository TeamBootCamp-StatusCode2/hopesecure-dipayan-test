from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailDomain(models.Model):
    """Email domains for phishing campaigns"""
    
    DOMAIN_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('failed', 'Verification Failed'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    DOMAIN_TYPE_CHOICES = [
        ('primary', 'Primary Domain'),
        ('spoofing', 'Spoofing Domain'),
        ('tracking', 'Tracking Domain'),
        ('redirect', 'Redirect Domain'),
    ]
    
    name = models.CharField(max_length=255, unique=True, help_text="Domain name (e.g., phishing-security.com)")
    domain_type = models.CharField(max_length=20, choices=DOMAIN_TYPE_CHOICES, default='spoofing')
    status = models.CharField(max_length=20, choices=DOMAIN_STATUS_CHOICES, default='pending')
    
    # DNS Configuration
    mx_records = models.JSONField(default=list, help_text="MX records for email routing")
    txt_records = models.JSONField(default=list, help_text="TXT records for verification")
    spf_record = models.TextField(blank=True, help_text="SPF record for email authentication")
    dkim_record = models.TextField(blank=True, help_text="DKIM record for email signing")
    dmarc_record = models.TextField(blank=True, help_text="DMARC record for email policy")
    
    # SSL/HTTPS Configuration
    ssl_enabled = models.BooleanField(default=False)
    ssl_certificate = models.TextField(blank=True)
    
    # Tracking and Analytics
    click_tracking_enabled = models.BooleanField(default=True)
    open_tracking_enabled = models.BooleanField(default=True)
    analytics_enabled = models.BooleanField(default=True)
    
    # Usage Statistics
    emails_sent = models.IntegerField(default=0)
    emails_opened = models.IntegerField(default=0)
    links_clicked = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_domains')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Configuration
    max_emails_per_day = models.IntegerField(default=1000)
    rate_limit_per_hour = models.IntegerField(default=100)
    
    class Meta:
        db_table = 'email_domains'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} ({self.domain_type})"
    
    @property
    def success_rate(self):
        """Calculate email success rate"""
        if self.emails_sent == 0:
            return 0
        return (self.emails_opened / self.emails_sent) * 100
    
    @property
    def click_rate(self):
        """Calculate click through rate"""
        if self.emails_opened == 0:
            return 0
        return (self.links_clicked / self.emails_opened) * 100


class DomainDNSRecord(models.Model):
    """DNS records for domain configuration"""
    
    RECORD_TYPE_CHOICES = [
        ('A', 'A Record'),
        ('AAAA', 'AAAA Record'),
        ('CNAME', 'CNAME Record'),
        ('MX', 'MX Record'),
        ('TXT', 'TXT Record'),
        ('SPF', 'SPF Record'),
        ('DKIM', 'DKIM Record'),
        ('DMARC', 'DMARC Record'),
    ]
    
    domain = models.ForeignKey(EmailDomain, on_delete=models.CASCADE, related_name='dns_records')
    record_type = models.CharField(max_length=10, choices=RECORD_TYPE_CHOICES)
    name = models.CharField(max_length=255, help_text="Record name/subdomain")
    value = models.TextField(help_text="Record value")
    ttl = models.IntegerField(default=3600, help_text="Time to Live in seconds")
    priority = models.IntegerField(null=True, blank=True, help_text="Priority for MX records")
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_attempts = models.IntegerField(default=0)
    last_verification = models.DateTimeField(null=True, blank=True)
    verification_error = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'domain_dns_records'
        unique_together = ['domain', 'record_type', 'name']
        
    def __str__(self):
        return f"{self.domain.name} - {self.record_type} - {self.name}"


class EmailTemplate(models.Model):
    """Email templates linked to domains"""
    
    name = models.CharField(max_length=200)
    domain = models.ForeignKey(EmailDomain, on_delete=models.CASCADE, related_name='templates')
    subject = models.CharField(max_length=500)
    html_content = models.TextField()
    plain_content = models.TextField(blank=True)
    
    # Sender Configuration
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    reply_to = models.EmailField(blank=True)
    
    # Template Settings
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=50, default='phishing')
    difficulty_level = models.CharField(max_length=20, default='intermediate')
    
    # Usage Statistics
    times_used = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'email_templates'
        
    def __str__(self):
        return f"{self.name} - {self.domain.name}"


class DomainVerificationToken(models.Model):
    """Tokens for domain verification"""
    
    domain = models.ForeignKey(EmailDomain, on_delete=models.CASCADE, related_name='verification_tokens')
    token = models.CharField(max_length=64, unique=True)
    verification_type = models.CharField(max_length=20, choices=[
        ('dns', 'DNS Verification'),
        ('file', 'File Upload Verification'),
        ('email', 'Email Verification'),
    ])
    
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'domain_verification_tokens'
