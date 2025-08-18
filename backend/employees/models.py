from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Department(models.Model):
    """Organization departments"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Employee(models.Model):
    """Employee profiles for targeting in campaigns"""
    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    position = models.CharField(max_length=100)
    manager_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    # Security-related fields
    security_clearance_level = models.CharField(max_length=50, blank=True)
    has_admin_access = models.BooleanField(default=False)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='medium')
    last_security_training = models.DateField(blank=True, null=True)
    phishing_susceptibility_score = models.IntegerField(default=50)  # 0-100 scale
    
    # Campaign participation
    total_campaigns_received = models.IntegerField(default=0)
    total_campaigns_clicked = models.IntegerField(default=0)
    total_campaigns_submitted = models.IntegerField(default=0)
    last_campaign_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def click_rate(self):
        """Calculate employee's click rate on phishing campaigns"""
        if self.total_campaigns_received == 0:
            return 0
        return round((self.total_campaigns_clicked / self.total_campaigns_received) * 100, 2)
    
    @property
    def submission_rate(self):
        """Calculate employee's submission rate on phishing campaigns"""
        if self.total_campaigns_received == 0:
            return 0
        return round((self.total_campaigns_submitted / self.total_campaigns_received) * 100, 2)


class EmployeeGroup(models.Model):
    """Groups for organizing employees"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    employees = models.ManyToManyField(Employee, related_name='groups', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class TrainingRecord(models.Model):
    """Security training records for employees"""
    TRAINING_TYPE_CHOICES = [
        ('phishing_awareness', 'Phishing Awareness'),
        ('password_security', 'Password Security'),
        ('data_protection', 'Data Protection'),
        ('incident_response', 'Incident Response'),
        ('social_engineering', 'Social Engineering'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='training_records')
    training_type = models.CharField(max_length=50, choices=TRAINING_TYPE_CHOICES)
    training_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_date = models.DateTimeField()
    completion_date = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)  # 0-100
    duration_minutes = models.IntegerField(blank=True, null=True)
    trainer = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.training_name}"
