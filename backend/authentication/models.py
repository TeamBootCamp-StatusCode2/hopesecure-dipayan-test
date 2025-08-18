from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model for the cybersecurity platform"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Security Manager'),
        ('analyst', 'Security Analyst'),
        ('employee', 'Employee'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    """Extended profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    security_score = models.IntegerField(default=0)  # Based on phishing test performance
    training_completed = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Profile for {self.user.full_name}"
