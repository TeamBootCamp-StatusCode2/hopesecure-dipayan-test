from django.db import models
from django.contrib.auth import get_user_model
from campaigns.models import Campaign
from employees.models import Employee, Department

User = get_user_model()


class Report(models.Model):
    """Base model for reports"""
    REPORT_TYPE_CHOICES = [
        ('campaign_summary', 'Campaign Summary'),
        ('employee_performance', 'Employee Performance'),
        ('department_analysis', 'Department Analysis'),
        ('security_metrics', 'Security Metrics'),
        ('trend_analysis', 'Trend Analysis'),
        ('custom', 'Custom Report'),
    ]
    
    STATUS_CHOICES = [
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generating')
    
    # Date range for the report
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    
    # Filters applied
    campaigns = models.ManyToManyField(Campaign, blank=True, related_name='reports')
    departments = models.ManyToManyField(Department, blank=True, related_name='reports')
    employees = models.ManyToManyField(Employee, blank=True, related_name='reports')
    
    # Report data (stored as JSON)
    data = models.JSONField(blank=True, null=True)
    
    # File storage
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class CampaignReport(models.Model):
    """Detailed reports for individual campaigns"""
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, related_name='detailed_report')
    
    # Summary statistics
    total_targets = models.IntegerField(default=0)
    emails_delivered = models.IntegerField(default=0)
    emails_opened = models.IntegerField(default=0)
    links_clicked = models.IntegerField(default=0)
    forms_submitted = models.IntegerField(default=0)
    attachments_downloaded = models.IntegerField(default=0)
    
    # Calculated rates
    delivery_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    open_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    click_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    submission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    download_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Time-based analysis
    average_time_to_click = models.DurationField(blank=True, null=True)
    average_time_to_submit = models.DurationField(blank=True, null=True)
    peak_activity_hour = models.IntegerField(blank=True, null=True)
    
    # Department breakdown
    department_stats = models.JSONField(blank=True, null=True)
    
    # Detailed timeline data
    timeline_data = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Report for {self.campaign.name}"


class SecurityMetrics(models.Model):
    """Organization-wide security metrics tracking"""
    
    # Overall statistics
    total_employees = models.IntegerField(default=0)
    total_campaigns = models.IntegerField(default=0)
    total_templates = models.IntegerField(default=0)
    
    # Risk metrics
    high_risk_employees = models.IntegerField(default=0)
    medium_risk_employees = models.IntegerField(default=0)
    low_risk_employees = models.IntegerField(default=0)
    
    # Performance metrics
    overall_click_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    overall_submission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    training_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Trend data (monthly aggregates)
    monthly_metrics = models.JSONField(blank=True, null=True)
    
    # Benchmark comparisons
    industry_average_click_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    industry_average_submission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Reporting period
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Security Metrics for {self.period_start.strftime('%Y-%m-%d')} to {self.period_end.strftime('%Y-%m-%d')}"


class DashboardWidget(models.Model):
    """Configuration for dashboard widgets"""
    WIDGET_TYPE_CHOICES = [
        ('campaign_stats', 'Campaign Statistics'),
        ('employee_risk', 'Employee Risk Distribution'),
        ('recent_activity', 'Recent Activity'),
        ('success_rates', 'Success Rates'),
        ('department_performance', 'Department Performance'),
        ('trend_chart', 'Trend Chart'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    width = models.IntegerField(default=1)
    height = models.IntegerField(default=1)
    configuration = models.JSONField(blank=True, null=True)  # Widget-specific settings
    is_visible = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position_y', 'position_x']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
