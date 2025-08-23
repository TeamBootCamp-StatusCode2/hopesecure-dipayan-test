"""
Script to populate sample data for testing real-time global statistics
"""
import os
import sys
import django

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from campaigns.models import Campaign, CampaignTarget
from organization.models import Company
from employees.models import Employee
from django.utils import timezone
import random

User = get_user_model()

def create_sample_data():
    print("🔄 Creating sample data for real-time statistics...")
    
    # Create a default admin user first
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@hopesecure.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        print(f"  ✅ Created admin user: admin")
    
    # Create sample companies
    companies = []
    company_names = [
        "TechCorp Solutions", "DataSafe Industries", "SecureNet LLC", 
        "CyberGuard Systems", "InfoShield Corp", "DigitalFortress Inc",
        "SafeData Technologies", "ProtectPro Solutions", "SecureWave Ltd",
        "CyberDefense Group"
    ]
    
    for i, name in enumerate(company_names):
        company, created = Company.objects.get_or_create(
            name=name,
            defaults={
                'domain': f"{name.lower().replace(' ', '').replace(',', '')}.com",
                'industry': random.choice(['technology', 'finance', 'healthcare', 'manufacturing']),
                'employee_count': random.choice(['1-50', '51-200', '200-500', '500-1000', '1000+']),
                'created_by': admin_user,
            }
        )
        companies.append(company)
        if created:
            print(f"  ✅ Created company: {name}")
    
    # Create sample users and campaigns
    for i in range(20):
        # Create user
        username = f"testuser{i+1}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f"{username}@{random.choice(companies).domain}",
                'first_name': f"Test{i+1}",
                'last_name': "User",
            }
        )
        
        if created:
            print(f"  ✅ Created user: {username}")
        
        # Create campaigns for this user
        for j in range(random.randint(1, 5)):
            campaign_name = f"Campaign {j+1} - {random.choice(['Phishing Test', 'Security Awareness', 'Email Security', 'Social Engineering'])}"
            
            # Get or create a default template first
            from templates.models import Template
            template, _ = Template.objects.get_or_create(
                name="Default Test Template",
                defaults={
                    'category': 'credential',
                    'description': 'Default template for testing',
                    'email_subject': "Important Security Update Required",
                    'sender_name': "IT Security Team",
                    'sender_email': "security@company.com",
                    'html_content': "<p>Please click the link to update your security settings.</p>",
                    'domain': "secure-portal.com",
                    'difficulty': 'low',
                    'risk_level': 'low',
                    'created_by': user,
                }
            )
            
            campaign, created = Campaign.objects.get_or_create(
                name=campaign_name,
                created_by=user,
                defaults={
                    'description': f'Automated test campaign for {user.username}',
                    'campaign_type': random.choice(['credential', 'data_input', 'link_click', 'attachment']),
                    'template': template,
                    'status': random.choice(['completed', 'active', 'paused']),
                    'target_count': random.randint(10, 200),
                    'emails_sent': random.randint(10, 200),
                    'emails_opened': random.randint(5, 150),
                    'links_clicked': random.randint(1, 80),
                    'credentials_submitted': random.randint(0, 40),
                    'data_submitted': random.randint(0, 20),
                    'attachments_downloaded': random.randint(0, 30),
                    'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 90)),
                }
            )
            
            if created:
                print(f"    📧 Created campaign: {campaign_name} ({campaign.emails_sent} emails sent)")
    
    # Calculate and display statistics
    total_campaigns = Campaign.objects.count()
    total_emails = sum(Campaign.objects.values_list('emails_sent', flat=True))
    total_companies = Company.objects.count()
    total_users = User.objects.count()
    
    print(f"\n📊 Sample Data Summary:")
    print(f"  • Companies: {total_companies}")
    print(f"  • Users: {total_users}")
    print(f"  • Campaigns: {total_campaigns}")
    print(f"  • Total emails sent: {total_emails:,}")
    print(f"\n✅ Sample data creation complete!")

if __name__ == "__main__":
    create_sample_data()
