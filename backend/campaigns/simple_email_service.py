"""
Simplified SendGrid Email Service for Basic Testing
"""

import json
import time
import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

class SimpleSendGridService:
    """
    Simplified SendGrid service using Django's built-in email backend
    """
    
    def __init__(self, campaign=None):
        self.campaign = campaign
    
    def send_simple_email(self, recipient_email, subject, html_content, sender_email=None):
        """
        Send email using Django's send_mail with SendGrid backend
        """
        try:
            from_email = sender_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'test@example.com')
            
            result = send_mail(
                subject=subject,
                message=html_content,  # Plain text fallback
                from_email=from_email,
                recipient_list=[recipient_email],
                html_message=html_content,  # HTML content
                fail_silently=False,
            )
            
            if result == 1:
                logger.info(f"Email sent successfully to {recipient_email}")
                return True
            else:
                logger.error(f"Failed to send email to {recipient_email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_campaign_emails(self, target_emails, template_data):
        """
        Send campaign emails to multiple recipients
        """
        sent_count = 0
        failed_count = 0
        
        # Rate limiting
        delay = getattr(settings, 'EMAIL_DELAY_SECONDS', 2)
        
        for email in target_emails:
            try:
                # Personalize email content
                personalized_content = template_data['html_content'].replace(
                    '{{recipient_email}}', email
                ).replace(
                    '{{recipient_name}}', email.split('@')[0].title()
                )
                
                success = self.send_simple_email(
                    recipient_email=email,
                    subject=template_data['subject'],
                    html_content=personalized_content,
                    sender_email=template_data.get('sender_email')
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

def test_sendgrid_connection():
    """
    Test SendGrid connection by sending a simple email
    """
    try:
        service = SimpleSendGridService()
        
        result = service.send_simple_email(
            recipient_email='bolbonakano@gmail.com',
            subject='HopeSecure Test Email - Simple Service',
            html_content='''
            <html>
            <body>
                <h2>🚀 HopeSecure SendGrid Test</h2>
                <p>If you receive this email, your SendGrid configuration is working!</p>
                <p><strong>✅ Email sending successful</strong></p>
                <hr>
                <small>Sent from HopeSecure Phishing Platform</small>
            </body>
            </html>
            ''',
            sender_email='bolbonakano@gmail.com'
        )
        
        return result, "Email sent successfully" if result else "Email sending failed"
        
    except Exception as e:
        return False, f"Error: {str(e)}"
