from django.core.management.base import BaseCommand
from campaigns.models import Campaign
from templates.models import Template
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample campaigns'

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

        # Get templates
        templates = Template.objects.all()
        if not templates.exists():
            self.stdout.write('No templates found. Please create templates first.')
            return

        sample_campaigns = [
            {
                'name': 'Q1 Security Assessment 2025',
                'description': 'Quarterly security awareness test for all employees',
                'campaign_type': 'credential',
                'template': templates.first(),
                'status': 'completed',
                'target_count': 150,
                'emails_sent': 150,
                'emails_opened': 98,
                'links_clicked': 45,
                'credentials_submitted': 12,
                'scheduled_start': datetime.now() - timedelta(days=30),
                'actual_start': datetime.now() - timedelta(days=30),
                'actual_end': datetime.now() - timedelta(days=25),
                'created_by': user
            },
            {
                'name': 'IT Security Alert Test',
                'description': 'Testing response to security alerts',
                'campaign_type': 'link_click',
                'template': templates.first(),
                'status': 'active',
                'target_count': 75,
                'emails_sent': 75,
                'emails_opened': 62,
                'links_clicked': 28,
                'scheduled_start': datetime.now() - timedelta(days=5),
                'actual_start': datetime.now() - timedelta(days=5),
                'created_by': user
            },
            {
                'name': 'HR Benefits Enrollment Test',
                'description': 'Testing data input form phishing',
                'campaign_type': 'data_input',
                'template': templates.first(),
                'status': 'scheduled',
                'target_count': 100,
                'scheduled_start': datetime.now() + timedelta(days=7),
                'created_by': user
            }
        ]

        created_count = 0
        for campaign_data in sample_campaigns:
            campaign, created = Campaign.objects.get_or_create(
                name=campaign_data['name'],
                defaults=campaign_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created campaign: {campaign.name}')
            else:
                self.stdout.write(f'Campaign already exists: {campaign.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new campaigns')
        )
