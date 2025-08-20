from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):
    """Organization/Company information"""
    INDUSTRY_CHOICES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('government', 'Government'),
        ('other', 'Other'),
    ]
    
    EMPLOYEE_COUNT_CHOICES = [
        ('1-50', '1-50'),
        ('51-200', '51-200'),
        ('200-500', '200-500'),
        ('500-1000', '500-1000'),
        ('1000+', '1000+'),
    ]
    
    TIMEZONE_CHOICES = [
        ('UTC-12', 'UTC-12 (Baker Island)'),
        ('UTC-8', 'UTC-8 (Pacific)'),
        ('UTC-5', 'UTC-5 (Eastern)'),
        ('UTC+0', 'UTC+0 (London)'),
        ('UTC+1', 'UTC+1 (Berlin)'),
        ('UTC+8', 'UTC+8 (Singapore)'),
        ('UTC+9', 'UTC+9 (Tokyo)'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, blank=True)
    domain = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='technology')
    employee_count = models.CharField(max_length=20, choices=EMPLOYEE_COUNT_CHOICES, default='1-50')
    
    # Contact Information
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.CharField(max_length=200, blank=True)  # Changed from URLField to CharField
    
    # Registration Information
    registration_number = models.CharField(max_length=50, blank=True)
    founded_year = models.CharField(max_length=4, blank=True)
    
    # Settings
    timezone = models.CharField(max_length=20, choices=TIMEZONE_CHOICES, default='UTC+0')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name or f"Company {self.id}"
    
    @classmethod
    def get_user_company(cls, user):
        """Get the user's organization company or all companies for super admin"""
        try:
            # Super admin can access all companies
            if user.is_super_admin:
                return cls.objects.all()
            
            # Return the user's organization if they have one
            if user.organization:
                return user.organization
            
            # If user doesn't have an organization, this shouldn't happen in the new system
            # but we'll handle it gracefully by creating one
            company = cls.objects.create(
                name='',
                domain='',
                industry='technology',
                employee_count='1-50',
                address='',
                phone='',
                website='',
                registration_number='',
                founded_year='',
                timezone='UTC+0',
                language='en',
                created_by=user
            )
            
            # Link the user to this company
            user.organization = company
            user.save()
            
            return company
        except Exception as e:
            raise Exception(f"Failed to get user company: {str(e)}")
    
    @classmethod
    def get_all_companies(cls):
        """Get all companies in the system - for super admin use"""
        return cls.objects.all()
