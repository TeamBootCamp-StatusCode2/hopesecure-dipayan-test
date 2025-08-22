"""
SendGrid Enhanced Email Service for Phishing Campaigns
SendGrid API integration with advanced tracking features
"""

import sendgrid
from sendgrid.helpers.mail import Mail, From, To, Subject, Content, Personalization
# Updated imports for newer SendGrid version
try:
    from sendgrid.helpers.tracking import ClickTracking, OpenTracking, SubscriptionTracking
except ImportError:
    # Fallback for newer versions
    ClickTracking = None
    OpenTracking = None
    SubscriptionTracking = None
import json
import time
import logging
from django.conf import settings
from django.core.mail import send_mail
from .email_service import PhishingEmailService

logger = logging.getLogger(__name__)

class SendGridPhishingService(PhishingEmailService):
    """
    SendGrid enhanced phishing email service
    Features: Advanced tracking, templates, webhooks
    """
    
    def __init__(self, campaign=None):
        super().__init__(campaign)
        self.sendgrid_client = None
        self.setup_sendgrid()
    
    def setup_sendgrid(self):
        """Initialize SendGrid client"""
        api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        if api_key:
            self.sendgrid_client = sendgrid.SendGridAPIClient(api_key=api_key)
        else:
            logger.warning("SendGrid API key not found in settings")
    
    def create_tracking_links(self, html_content, campaign_id, recipient_email):
        """
        Create tracking links for click monitoring
        """
        import hashlib
        
        # Generate unique tracking ID
        tracking_id = hashlib.md5(f"{campaign_id}_{recipient_email}_{time.time()}".encode()).hexdigest()
        
        # Replace placeholder links with tracking URLs
        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        tracking_url = f"{base_url}/api/campaigns/track-click/{tracking_id}/"
        
        # Replace common link patterns
        html_content = html_content.replace('{{tracking_url}}', tracking_url)
        html_content = html_content.replace('{{click_here}}', tracking_url)
        
        # Add tracking pixel for email opens
        tracking_pixel = f'<img src="{base_url}/api/campaigns/track-open/{tracking_id}/" width="1" height="1" style="display:none;" />'
        html_content += tracking_pixel
        
        return html_content, tracking_id
    
    def send_phishing_email_sendgrid(self, 
                                   recipient_email, 
                                   subject, 
                                   html_content, 
                                   sender_name="IT Security Team",
                                   sender_email="security@company.com",
                                   target_domain="company.com",
                                   use_spoofing=True,
                                   campaign_id=None):
        """
        Send phishing email using SendGrid API
        """
        try:
            if not self.sendgrid_client:
                logger.error("SendGrid client not initialized")
                return False
            
            # Create tracking links
            if campaign_id:
                html_content, tracking_id = self.create_tracking_links(
                    html_content, campaign_id, recipient_email
                )
            
            # Setup spoofed sender if enabled
            if use_spoofing:
                headers, spoofed_sender = self.create_spoofed_email_headers(
                    sender_name, sender_email, target_domain
                )
                from_email = spoofed_sender
            else:
                from_email = sender_email
            
            # Create SendGrid Mail object
            message = Mail()
            
            # Set sender
            message.from_email = From(from_email, sender_name)
            
            # Set recipient  
            message.add_to(To(recipient_email))
            
            # Set subject
            message.subject = Subject(subject)
            
            # Set content
            message.add_content(Content("text/html", html_content))
            
            # Enable tracking
            message.tracking_settings = self._setup_tracking_settings()
            
            # Add custom headers for spoofing
            if use_spoofing:
                message.headers = {
                    'X-Originating-IP': '[192.168.1.100]',
                    'X-Mailer': 'Microsoft Outlook 16.0',
                    'Reply-To': from_email
                }
            
            # Send email
            response = self.sendgrid_client.send(message)
            
            if response.status_code == 202:
                logger.info(f"SendGrid email sent to {recipient_email}, Message ID: {response.headers.get('X-Message-Id', 'Unknown')}")
                return True
            else:
                logger.error(f"SendGrid API error: {response.status_code} - {response.body}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send SendGrid email: {str(e)}")
            return False
    
    def _setup_tracking_settings(self):
        """
        Configure SendGrid tracking settings
        """
        tracking_settings = {}
        
        # For newer SendGrid versions, tracking is handled differently
        if ClickTracking:
            # Click tracking
            click_tracking = ClickTracking()
            click_tracking.enable = True
            click_tracking.enable_text = True
            tracking_settings['click_tracking'] = click_tracking
        
        if OpenTracking:
            # Open tracking
            open_tracking = OpenTracking()
            open_tracking.enable = True
            open_tracking.substitution_tag = '%tracking_pixel%'
            tracking_settings['open_tracking'] = open_tracking
        
        return tracking_settings
    
    def send_campaign_emails_sendgrid(self, target_emails, template_data, campaign_id=None):
        """
        Send campaign emails using SendGrid with rate limiting
        """
        sent_count = 0
        failed_count = 0
        
        # Rate limiting
        delay = settings.PHISHING_EMAIL_SETTINGS.get('EMAIL_DELAY_SECONDS', 2)
        
        for email in target_emails:
            try:
                # Personalize email content
                personalized_content = self.personalize_email_content(
                    template_data['html_content'], 
                    email
                )
                
                success = self.send_phishing_email_sendgrid(
                    recipient_email=email,
                    subject=template_data['subject'],
                    html_content=personalized_content,
                    sender_name=template_data.get('sender_name', 'IT Security'),
                    sender_email=template_data.get('sender_email', 'security@company.com'),
                    target_domain=template_data.get('target_domain', 'company.com'),
                    use_spoofing=template_data.get('use_spoofing', True),
                    campaign_id=campaign_id
                )
                
                if success:
                    sent_count += 1
                else:
                    failed_count += 1
                
                # Rate limiting delay
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error sending to {email}: {str(e)}")
                failed_count += 1
        
        return {
            'sent': sent_count,
            'failed': failed_count,
            'total': len(target_emails)
        }
    
    def send_template_email(self, recipient_email, template_id, template_data):
        """
        Send email using SendGrid dynamic templates
        """
        try:
            if not self.sendgrid_client:
                return False
            
            message = Mail()
            message.from_email = From(template_data.get('sender_email', 'security@company.com'))
            message.add_to(To(recipient_email))
            message.template_id = template_id
            
            # Add dynamic template data
            personalization = Personalization()
            personalization.add_to(To(recipient_email))
            personalization.dynamic_template_data = template_data
            message.add_personalization(personalization)
            
            response = self.sendgrid_client.send(message)
            return response.status_code == 202
            
        except Exception as e:
            logger.error(f"Failed to send template email: {str(e)}")
            return False

# Helper functions for SendGrid
def verify_sendgrid_setup():
    """
    Verify SendGrid configuration
    """
    api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
    if not api_key:
        return False, "SendGrid API key not configured"
    
    try:
        client = sendgrid.SendGridAPIClient(api_key=api_key)
        # Test API key by getting user info
        response = client.user.get()
        if response.status_code == 200:
            return True, "SendGrid configuration is valid"
        else:
            return False, f"SendGrid API error: {response.status_code}"
    except Exception as e:
        return False, f"SendGrid connection failed: {str(e)}"

def get_sendgrid_stats():
    """
    Get SendGrid account statistics
    """
    api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
    if not api_key:
        return None
    
    try:
        client = sendgrid.SendGridAPIClient(api_key=api_key)
        response = client.stats.get()
        if response.status_code == 200:
            return json.loads(response.body)
        return None
    except Exception as e:
        logger.error(f"Failed to get SendGrid stats: {str(e)}")
        return None
