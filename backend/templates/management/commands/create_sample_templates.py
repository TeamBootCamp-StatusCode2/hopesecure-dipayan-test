from django.core.management.base import BaseCommand
from templates.models import Template
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample templates'

    def handle(self, *args, **options):
        # Get first user or create admin user
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                username='admin',
                email='admin@hopesecure.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('Created admin user')

        sample_templates = [
            {
                'name': 'Company Login Page',
                'category': 'credential',
                'description': 'Mimics company login portal to capture credentials',
                'email_subject': 'Urgent: Account Verification Required',
                'sender_name': 'IT Security Team',
                'sender_email': 'security@company.com',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <title>Account Verification</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; }
        .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Account Verification Required</h2>
        <p>We have detected suspicious activity on your account.</p>
        <p>Please verify your account immediately:</p>
        <a href="#" class="btn">Verify Account</a>
    </div>
</body>
</html>
                ''',
                'domain': 'company-login.secure.com',
                'difficulty': 'intermediate',
                'risk_level': 'intermediate',
                'status': 'active',
                'usage_count': 15,
                'success_rate': 32.00,
                'rating': 4.2,
                'tracking_enabled': True,
                'priority': 'high',
                'created_by': user
            },
            {
                'name': 'IT Security Alert',
                'category': 'link_click',
                'description': 'Security alert prompting immediate action',
                'email_subject': 'Security Alert: Suspicious Activity Detected',
                'sender_name': 'Security Team',
                'sender_email': 'alerts@company.com',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <title>Security Alert</title>
</head>
<body>
    <h2>SECURITY ALERT</h2>
    <p>Suspicious login attempt detected from unknown location.</p>
    <p><strong>Action Required:</strong> Secure your account immediately.</p>
    <a href="#" style="background: #dc3545; color: white; padding: 10px 20px; text-decoration: none;">SECURE ACCOUNT</a>
</body>
</html>
                ''',
                'domain': 'security-alerts.company.com',
                'difficulty': 'beginner',
                'risk_level': 'low',
                'status': 'active',
                'usage_count': 23,
                'success_rate': 45.00,
                'rating': 3.8,
                'tracking_enabled': True,
                'priority': 'urgent',
                'created_by': user
            },
            {
                'name': 'Office 365 Update',
                'category': 'attachment',
                'description': 'Fake Microsoft Office update with malicious attachment',
                'email_subject': 'Important: Office 365 Security Update Required',
                'sender_name': 'Microsoft Office Team',
                'sender_email': 'updates@microsoft-office.com',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <title>Office 365 Update</title>
</head>
<body>
    <h2>Critical Security Update Available</h2>
    <p>A critical security update is available for your Office 365 installation.</p>
    <p>Please download and install the update immediately to maintain security.</p>
    <a href="#" style="background: #0078d4; color: white; padding: 10px 20px; text-decoration: none;">Download Update</a>
</body>
</html>
                ''',
                'domain': 'updates.microsoft-office.com',
                'difficulty': 'advanced',
                'risk_level': 'high',
                'status': 'draft',
                'usage_count': 8,
                'success_rate': 67.00,
                'rating': 4.9,
                'tracking_enabled': True,
                'priority': 'high',
                'created_by': user
            },
            {
                'name': 'HR Benefits Enrollment',
                'category': 'data_input',
                'description': 'Annual benefits enrollment requiring personal information',
                'email_subject': 'Urgent: Complete Your Benefits Enrollment',
                'sender_name': 'HR Benefits Team',
                'sender_email': 'benefits@company.com',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <title>Benefits Enrollment</title>
</head>
<body>
    <h2>Annual Benefits Enrollment</h2>
    <p>Complete your annual benefits enrollment by the deadline.</p>
    <p>Provide your personal information to continue enrollment:</p>
    <form>
        <input type="text" placeholder="Full Name" required><br><br>
        <input type="email" placeholder="Email Address" required><br><br>
        <input type="text" placeholder="Social Security Number" required><br><br>
        <button type="submit">Submit Enrollment</button>
    </form>
</body>
</html>
                ''',
                'domain': 'hr-benefits.company.com',
                'difficulty': 'intermediate',
                'risk_level': 'intermediate',
                'status': 'active',
                'usage_count': 12,
                'success_rate': 56.00,
                'rating': 4.1,
                'tracking_enabled': True,
                'priority': 'high',
                'created_by': user
            }
        ]

        created_count = 0
        for template_data in sample_templates:
            template, created = Template.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created template: {template.name}')
            else:
                self.stdout.write(f'Template already exists: {template.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new templates')
        )
