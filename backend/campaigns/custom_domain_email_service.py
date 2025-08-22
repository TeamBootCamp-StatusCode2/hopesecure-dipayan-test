"""
Custom Domain Email Service
Handles email sending with custom domains using SendGrid
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from .domain_models import EmailDomain

class CustomDomainEmailService:
    """
    Service for sending emails using custom domains
    """
    
    def __init__(self):
        self.sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    
    def send_phishing_email(self, sender_email, recipient_email, subject, html_content, domain_id=None):
        """
        Send phishing email using custom domain
        """
        try:
            # Get domain info if provided
            domain_info = None
            if domain_id:
                domain_info = EmailDomain.objects.get(id=domain_id)
            
            # Create email message
            message = Mail(
                from_email=sender_email,
                to_emails=recipient_email,
                subject=subject,
                html_content=html_content
            )
            
            # Add tracking if domain supports it
            if domain_info and domain_info.click_tracking_enabled:
                message.tracking_settings = {
                    "click_tracking": {"enable": True},
                    "open_tracking": {"enable": domain_info.open_tracking_enabled}
                }
            
            # Send email
            response = self.sg.send(message)
            
            # Update domain statistics
            if domain_info:
                domain_info.emails_sent += 1
                domain_info.save()
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Email sent successfully',
                'sender_email': sender_email,
                'recipient': recipient_email
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'sender_email': sender_email,
                'recipient': recipient_email
            }
    
    def validate_domain_setup(self, domain_id):
        """
        Validate if domain is properly configured for email sending
        """
        try:
            domain = EmailDomain.objects.get(id=domain_id)
            
            validation_results = {
                'domain_exists': True,
                'domain_verified': domain.status == 'verified',
                'dns_configured': bool(domain.mx_records),
                'spf_record': bool(domain.spf_record),
                'dkim_record': bool(domain.dkim_record),
                'sendgrid_integrated': True,  # Assume true for now
                'ready_for_sending': False
            }
            
            # Check if ready for sending
            validation_results['ready_for_sending'] = all([
                validation_results['domain_verified'],
                validation_results['dns_configured'],
                validation_results['sendgrid_integrated']
            ])
            
            return validation_results
            
        except EmailDomain.DoesNotExist:
            return {
                'domain_exists': False,
                'error': 'Domain not found'
            }
    
    def create_campaign_emails(self, campaign_data, target_emails):
        """
        Create and send campaign emails to multiple recipients
        """
        results = []
        sender_email = campaign_data.get('sender_email')
        subject = campaign_data.get('subject', 'Important Security Notice')
        html_content = campaign_data.get('html_content', '<p>Security awareness test email</p>')
        domain_id = campaign_data.get('domain_id')
        
        for recipient in target_emails:
            result = self.send_phishing_email(
                sender_email=sender_email,
                recipient_email=recipient,
                subject=subject,
                html_content=html_content,
                domain_id=domain_id
            )
            results.append(result)
        
        return {
            'total_emails': len(target_emails),
            'successful_sends': len([r for r in results if r['success']]),
            'failed_sends': len([r for r in results if not r['success']]),
            'results': results
        }
