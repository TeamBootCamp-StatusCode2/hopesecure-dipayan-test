"""
Multi-Domain SendGrid Email Service
বিভিন্ন domain extension দিয়ে phishing email পাঠানোর জন্য
"""

import sendgrid
from sendgrid.helpers.mail import Mail, From, To, Subject, Content
import random
import time
import logging
from django.conf import settings
from .domain_examples import PHISHING_DOMAIN_EXAMPLES, EMAIL_TEMPLATES

logger = logging.getLogger(__name__)

class MultiDomainPhishingService:
    """
    Multiple domain extensions দিয়ে phishing emails পাঠানোর service
    """
    
    def __init__(self):
        self.sendgrid_client = None
        self.setup_sendgrid()
        self.available_domains = []
        self.load_verified_domains()
    
    def setup_sendgrid(self):
        """SendGrid client setup"""
        api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        if api_key:
            self.sendgrid_client = sendgrid.SendGridAPIClient(api_key=api_key)
            logger.info("SendGrid client initialized successfully")
        else:
            logger.error("SendGrid API key not found!")
    
    def load_verified_domains(self):
        """Load verified domains from database"""
        from .domain_models import EmailDomain
        
        verified_domains = EmailDomain.objects.filter(status='verified')
        self.available_domains = [domain.name for domain in verified_domains]
        
        logger.info(f"Loaded {len(self.available_domains)} verified domains")
    
    def get_random_sender_email(self, domain_type='corporate'):
        """
        Random sender email address generate করে domain type অনুযায়ী
        """
        if not self.available_domains:
            return 'test@example.com'
        
        # Select domain based on type
        domain_mapping = {
            'corporate': ['microsoft-update.com', 'google-security.net'],
            'banking': ['bank-verification.org'],
            'social': ['facebook-security.info'],
            'ecommerce': ['amazon-delivery.co'],
            'government': ['gov-notice.org']
        }
        
        suitable_domains = []
        for domain in self.available_domains:
            if any(d in domain for d in domain_mapping.get(domain_type, [])):
                suitable_domains.append(domain)
        
        if not suitable_domains:
            suitable_domains = self.available_domains
        
        selected_domain = random.choice(suitable_domains)
        
        # Generate random email prefixes
        email_prefixes = [
            'security', 'notifications', 'alerts', 'support', 'admin',
            'noreply', 'verification', 'fraud', 'delivery', 'official'
        ]
        
        prefix = random.choice(email_prefixes)
        return f"{prefix}@{selected_domain}"
    
    def create_personalized_email(self, template_name, recipient_email, tracking_url):
        """
        Personalized email content তৈরি করে recipient অনুযায়ী
        """
        if template_name not in EMAIL_TEMPLATES:
            return None
        
        template = EMAIL_TEMPLATES[template_name]
        
        # Extract recipient name from email
        recipient_name = recipient_email.split('@')[0].replace('.', ' ').title()
        
        # Personalize content
        html_content = template['template'].replace('{{recipient_name}}', recipient_name)
        html_content = html_content.replace('{{recipient_email}}', recipient_email)
        html_content = html_content.replace('{{tracking_link}}', tracking_url)
        
        return {
            'subject': template['subject'],
            'from_email': template['from_email'],
            'from_name': template['from_name'],
            'html_content': html_content
        }
    
    def send_multi_domain_campaign(self, target_emails, campaign_config):
        """
        Multiple domains ব্যবহার করে phishing campaign পাঠায়
        """
        results = {
            'sent': 0,
            'failed': 0,
            'emails_sent': [],
            'errors': []
        }
        
        template_names = list(EMAIL_TEMPLATES.keys())
        
        for i, recipient_email in enumerate(target_emails):
            try:
                # Rotate templates and domains for variety
                template_name = template_names[i % len(template_names)]
                
                # Generate tracking URL
                tracking_url = self.generate_tracking_url(recipient_email, campaign_config.get('campaign_id'))
                
                # Create personalized email
                email_data = self.create_personalized_email(template_name, recipient_email, tracking_url)
                
                if not email_data:
                    results['failed'] += 1
                    continue
                
                # Override sender email with random domain if configured
                if campaign_config.get('use_random_domains', True):
                    email_data['from_email'] = self.get_random_sender_email()
                
                # Send email
                success = self.send_single_email(
                    recipient_email=recipient_email,
                    **email_data
                )
                
                if success:
                    results['sent'] += 1
                    results['emails_sent'].append({
                        'recipient': recipient_email,
                        'sender': email_data['from_email'],
                        'template': template_name,
                        'tracking_url': tracking_url
                    })
                else:
                    results['failed'] += 1
                
                # Rate limiting - SendGrid এর limit অনুযায়ী
                time.sleep(campaign_config.get('delay_seconds', 2))
                
            except Exception as e:
                logger.error(f"Error sending to {recipient_email}: {str(e)}")
                results['failed'] += 1
                results['errors'].append(f"{recipient_email}: {str(e)}")
        
        return results
    
    def send_single_email(self, recipient_email, subject, from_email, from_name, html_content):
        """
        Single email পাঠানোর function
        """
        try:
            message = Mail()
            
            # Sender information
            message.from_email = From(from_email, from_name)
            
            # Recipient
            message.add_to(To(recipient_email))
            
            # Subject
            message.subject = Subject(subject)
            
            # Content
            message.add_content(Content("text/html", html_content))
            
            # Enable tracking
            message.tracking_settings = {
                "click_tracking": {"enable": True},
                "open_tracking": {"enable": True}
            }
            
            # Custom headers for better spoofing
            message.headers = {
                'X-Mailer': 'Microsoft Outlook 16.0',
                'X-Priority': '1',
                'Importance': 'high'
            }
            
            # Send via SendGrid
            response = self.sendgrid_client.send(message)
            
            if response.status_code == 202:
                logger.info(f"✅ Email sent: {from_email} -> {recipient_email}")
                return True
            else:
                logger.error(f"❌ SendGrid error {response.status_code}: {response.body}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to send email: {str(e)}")
            return False
    
    def generate_tracking_url(self, recipient_email, campaign_id):
        """
        Tracking URL generate করে click monitoring এর জন্য
        """
        import hashlib
        
        # Create unique tracking ID
        tracking_data = f"{recipient_email}_{campaign_id}_{time.time()}"
        tracking_id = hashlib.md5(tracking_data.encode()).hexdigest()
        
        # Return tracking URL
        base_url = settings.PHISHING_TRACKING_DOMAIN or "http://localhost:8000"
        return f"{base_url}/track/click/{tracking_id}/"
    
    def get_domain_statistics(self):
        """
        Domain wise statistics return করে
        """
        from .domain_models import EmailDomain
        
        domains = EmailDomain.objects.filter(status='verified')
        stats = []
        
        for domain in domains:
            stats.append({
                'domain': domain.name,
                'emails_sent': domain.emails_sent,
                'success_rate': domain.success_rate,
                'click_rate': domain.click_rate,
                'last_used': domain.last_used
            })
        
        return stats


def test_multi_domain_campaign():
    """
    Multi-domain campaign এর test function
    """
    service = MultiDomainPhishingService()
    
    # Test emails
    test_emails = [
        'bolbonakano@gmail.com',
        'test2@example.com'
    ]
    
    # Campaign configuration
    campaign_config = {
        'campaign_id': 'test_multi_domain_001',
        'use_random_domains': True,
        'delay_seconds': 3
    }
    
    # Send campaign
    results = service.send_multi_domain_campaign(test_emails, campaign_config)
    
    print("📊 Campaign Results:")
    print(f"✅ Sent: {results['sent']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"📧 Total Emails: {len(test_emails)}")
    
    if results['emails_sent']:
        print("\n📤 Emails Sent Details:")
        for email_info in results['emails_sent']:
            print(f"  {email_info['recipient']} <- {email_info['sender']} (Template: {email_info['template']})")
    
    if results['errors']:
        print("\n❌ Errors:")
        for error in results['errors']:
            print(f"  {error}")
    
    return results
