"""
Management command to populate the database with sample data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from templates.models import Template, TemplateTag
from employees.models import Department, Employee
from campaigns.models import Campaign, CampaignTarget
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        self.create_sample_users()
        
        # Create departments
        self.create_departments()
        
        # Create employees
        self.create_employees()
        
        # Create template tags
        self.create_template_tags()
        
        # Create templates
        self.create_templates()
        
        # Create campaigns
        self.create_campaigns()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_sample_users(self):
        """Create sample users with different roles"""
        users = [
            {
                'email': 'manager@cyberguard.com',
                'username': 'manager',
                'first_name': 'Security',
                'last_name': 'Manager',
                'role': 'manager',
                'department': 'IT Security'
            },
            {
                'email': 'analyst@cyberguard.com',
                'username': 'analyst',
                'first_name': 'Security',
                'last_name': 'Analyst',
                'role': 'analyst',
                'department': 'IT Security'
            }
        ]
        
        for user_data in users:
            if not User.objects.filter(email=user_data['email']).exists():
                user = User.objects.create_user(
                    password='password123',
                    **user_data
                )
                self.stdout.write(f'Created user: {user.email}')

    def create_departments(self):
        """Create sample departments"""
        departments = [
            {'name': 'IT Security', 'description': 'Information Technology Security Department'},
            {'name': 'Human Resources', 'description': 'Human Resources Department'},
            {'name': 'Finance', 'description': 'Finance and Accounting Department'},
            {'name': 'Marketing', 'description': 'Marketing and Communications Department'},
            {'name': 'Operations', 'description': 'Operations and Logistics Department'},
        ]
        
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(**dept_data)
            if created:
                self.stdout.write(f'Created department: {dept.name}')

    def create_employees(self):
        """Create sample employees"""
        departments = Department.objects.all()
        
        employees = [
            {
                'employee_id': 'EMP001',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@company.com',
                'position': 'Software Developer',
                'hire_date': datetime.now().date() - timedelta(days=365),
                'risk_level': 'medium'
            },
            {
                'employee_id': 'EMP002',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@company.com',
                'position': 'HR Manager',
                'hire_date': datetime.now().date() - timedelta(days=500),
                'risk_level': 'low'
            },
            {
                'employee_id': 'EMP003',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'email': 'mike.johnson@company.com',
                'position': 'Finance Analyst',
                'hire_date': datetime.now().date() - timedelta(days=200),
                'risk_level': 'high'
            }
        ]
        
        for i, emp_data in enumerate(employees):
            if not Employee.objects.filter(email=emp_data['email']).exists():
                emp_data['department'] = departments[i % len(departments)]
                employee = Employee.objects.create(**emp_data)
                self.stdout.write(f'Created employee: {employee.full_name}')

    def create_template_tags(self):
        """Create sample template tags"""
        tags = ['Login', 'Credentials', 'Corporate', 'Urgent', 'Banking', 'Social Media', 'Cloud']
        
        for tag_name in tags:
            tag, created = TemplateTag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

    def create_templates(self):
        """Create sample templates"""
        manager = User.objects.filter(role='manager').first()
        if not manager:
            return
        
        templates = [
            {
                'name': 'Company Login Page',
                'category': 'credential',
                'description': 'Mimics company login portal to capture credentials',
                'email_subject': 'Urgent: Account Verification Required',
                'sender_name': 'IT Security Team',
                'sender_email': 'security@company.com',
                'domain': 'company-login.secure.com',
                'difficulty': 'intermediate',
                'risk_level': 'intermediate',
                'html_content': '''<!DOCTYPE html>
<html>
<head><title>Company Login</title></head>
<body>
    <div style="max-width: 400px; margin: 50px auto; padding: 40px; border: 1px solid #ddd;">
        <h2>Company Portal</h2>
        <p style="color: red;">⚠️ Your account will be suspended in 24 hours if not verified.</p>
        <form>
            <div><label>Email:</label><input type="email" name="email" style="width: 100%; padding: 10px; margin: 5px 0;"></div>
            <div><label>Password:</label><input type="password" name="password" style="width: 100%; padding: 10px; margin: 5px 0;"></div>
            <button type="submit" style="width: 100%; padding: 12px; background: #007acc; color: white; border: none;">Verify Account</button>
        </form>
    </div>
</body>
</html>''',
                'status': 'active',
                'rating': 4.2,
                'created_by': manager
            },
            {
                'name': 'IT Security Alert',
                'category': 'link_click',
                'description': 'Security alert prompting immediate action',
                'email_subject': 'URGENT: Security Breach Detected',
                'sender_name': 'IT Security',
                'sender_email': 'alerts@company.com',
                'domain': 'security-alerts.company.com',
                'difficulty': 'high',
                'risk_level': 'high',
                'html_content': '''<!DOCTYPE html>
<html>
<head><title>Security Alert</title></head>
<body>
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial;">
        <div style="background: red; color: white; padding: 15px; text-align: center;">
            <h1>SECURITY BREACH DETECTED</h1>
        </div>
        <p>We have detected unauthorized access attempts on your account.</p>
        <p><strong>Action Required:</strong> Click the link below to secure your account immediately.</p>
        <a href="#" style="display: block; width: 200px; padding: 15px; background: red; color: white; text-decoration: none; text-align: center; margin: 20px auto;">SECURE ACCOUNT NOW</a>
        <p><small>This link will expire in 1 hour.</small></p>
    </div>
</body>
</html>''',
                'status': 'active',
                'rating': 3.8,
                'created_by': manager
            }
        ]
        
        for template_data in templates:
            if not Template.objects.filter(name=template_data['name']).exists():
                template = Template.objects.create(**template_data)
                
                # Add tags
                tag_names = ['Login', 'Credentials'] if 'Login' in template.name else ['Security', 'Alert']
                for tag_name in tag_names:
                    tag, _ = TemplateTag.objects.get_or_create(name=tag_name)
                    template.tags.add(tag)
                
                self.stdout.write(f'Created template: {template.name}')

    def create_campaigns(self):
        """Create sample campaigns"""
        manager = User.objects.filter(role='manager').first()
        templates = Template.objects.all()
        employees = Employee.objects.all()
        
        if not manager or not templates.exists() or not employees.exists():
            return
        
        campaigns = [
            {
                'name': 'Q4 Security Assessment',
                'description': 'Quarterly security awareness assessment',
                'campaign_type': 'credential',
                'status': 'active',
                'scheduled_start': datetime.now() - timedelta(days=5),
                'template': templates.first(),
                'created_by': manager
            },
            {
                'name': 'New Employee Training',
                'description': 'Security training for new hires',
                'campaign_type': 'link_click',
                'status': 'completed',
                'scheduled_start': datetime.now() - timedelta(days=15),
                'scheduled_end': datetime.now() - timedelta(days=10),
                'template': templates.last(),
                'created_by': manager
            }
        ]
        
        for camp_data in campaigns:
            if not Campaign.objects.filter(name=camp_data['name']).exists():
                campaign = Campaign.objects.create(**camp_data)
                
                # Add random targets
                target_employees = random.sample(list(employees), min(3, len(employees)))
                for employee in target_employees:
                    CampaignTarget.objects.create(
                        campaign=campaign,
                        email=employee.email,
                        first_name=employee.first_name,
                        last_name=employee.last_name,
                        department=employee.department.name,
                        status=random.choice(['sent', 'opened', 'clicked'])
                    )
                
                campaign.target_count = len(target_employees)
                campaign.emails_sent = len(target_employees)
                campaign.emails_opened = random.randint(0, len(target_employees))
                campaign.links_clicked = random.randint(0, campaign.emails_opened)
                campaign.credentials_submitted = random.randint(0, campaign.links_clicked)
                campaign.save()
                
                self.stdout.write(f'Created campaign: {campaign.name}')
