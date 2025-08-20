from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Template(models.Model):
    """Phishing email and landing page templates"""
    CATEGORY_CHOICES = [
        ('credential', 'Credential Phishing'),
        ('data_input', 'Data Input Form'),
        ('link_click', 'Link Click Tracking'),
        ('attachment', 'Fake Attachment'),
        ('social_engineering', 'Social Engineering'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('intermediate', 'Intermediate'),
        ('high', 'High'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    email_subject = models.CharField(max_length=200)
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    html_content = models.TextField()
    css_styles = models.TextField(blank=True)
    landing_page_url = models.URLField(blank=True)
    domain = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    has_attachments = models.BooleanField(default=False)
    has_css = models.BooleanField(default=False)
    is_responsive = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='template_thumbnails/', blank=True, null=True)
    usage_count = models.IntegerField(default=0)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    tracking_enabled = models.BooleanField(default=True)
    priority = models.CharField(max_length=20, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_templates', null=True, blank=True)  # Made nullable for testing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class TemplateTag(models.Model):
    """Tags for categorizing templates"""
    name = models.CharField(max_length=50, unique=True)
    templates = models.ManyToManyField(Template, related_name='tags', blank=True)
    
    def __str__(self):
        return self.name


class TemplateAttachment(models.Model):
    """File attachments for phishing templates"""
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='template_attachments/')
    filename = models.CharField(max_length=200)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    is_malicious_simulation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.filename} - {self.template.name}"
