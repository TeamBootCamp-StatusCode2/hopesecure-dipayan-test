"""
Enhanced Email Service to Avoid Spam Filters
Optimized for better email deliverability and inbox placement
"""

import sendgrid
from sendgrid.helpers.mail import Mail, From, To, Subject, Content, Header, CustomArg
from sendgrid.helpers.tracking import ClickTracking, OpenTracking, SubscriptionTracking
import json
import re
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class AntiSpamEmailService:
    """
    Enhanced email service designed to avoid spam filters
    """
    
    def __init__(self):
        self.api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        self.sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
        self.verified_sender = "hope@hopesecure.tech"
        
    def optimize_email_content(self, html_content, subject):
        """
        Optimize email content to avoid spam triggers
        """
        # Remove spam-triggering words and phrases
        spam_words = [
            'FREE', 'URGENT', 'ACT NOW', 'LIMITED TIME', 'CLICK HERE NOW',
            'WINNER', 'CONGRATULATIONS', '$$$', '100% FREE', 'CALL NOW',
            'URGENT ACTION REQUIRED', 'VERIFY IMMEDIATELY'
        ]
        
        optimized_content = html_content
        optimized_subject = subject
        
        # Replace spam words with safer alternatives
        for word in spam_words:
            optimized_content = re.sub(word, word.lower(), optimized_content, flags=re.IGNORECASE)
            optimized_subject = re.sub(word, word.lower(), optimized_subject, flags=re.IGNORECASE)
        
        # Ensure proper HTML structure
        if not optimized_content.strip().startswith('<html'):
            optimized_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Security Notice</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                    .content {{ background: white; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
                    .btn {{ display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="content">
                        {optimized_content}
                    </div>
                    <div class="footer">
                        <p>This is a security awareness training email.</p>
                        <p>If you have questions, contact your IT security team.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        return optimized_content, optimized_subject
    
    def create_professional_headers(self, recipient_email, sender_name="IT Security Team"):
        """
        Create professional email headers to improve deliverability
        """
        headers = {
            "X-Priority": "3",
            "X-MSMail-Priority": "Normal",
            "X-Mailer": "Microsoft Outlook 16.0",
            "X-MimeOLE": "Produced By Microsoft MimeOLE V16.0.5078.0",
            "Importance": "Normal",
            "X-Auto-Response-Suppress": "All",
            "X-Security-Training": "true",
            "List-Unsubscribe": f"<mailto:unsubscribe@hopesecure.tech?subject=unsubscribe-{recipient_email}>",
        }
        return headers
    
    def send_campaign_email(self, recipient_email, subject, html_content, sender_name="IT Security Team", campaign_id=None):
        """
        Send email with anti-spam optimizations
        """
        try:
            # Optimize content for deliverability
            optimized_content, optimized_subject = self.optimize_email_content(html_content, subject)
            
            # Create professional headers
            headers = self.create_professional_headers(recipient_email, sender_name)
            
            # Create mail object
            message = Mail()
            
            # Set sender with professional name
            message.from_email = From(self.verified_sender, sender_name)
            
            # Set recipient
            message.to = [To(recipient_email)]
            
            # Set subject (keep it professional and non-spammy)
            message.subject = Subject(optimized_subject)
            
            # Set content
            message.content = Content("text/html", optimized_content)
            
            # Add professional headers
            for header_name, header_value in headers.items():
                message.header = Header(header_name, header_value)
            
            # Configure tracking (but make it subtle)
            message.tracking_settings = self._get_tracking_settings()
            
            # Add custom arguments for campaign tracking
            if campaign_id:
                message.custom_arg = [CustomArg("campaign_id", str(campaign_id))]
            
            # Send email
            response = self.sg.send(message)
            
            logger.info(f"Email sent successfully to {recipient_email}. Status: {response.status_code}")
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Email sent successfully with anti-spam optimization',
                'sender_email': self.verified_sender,
                'recipient': recipient_email,
                'headers_applied': True
            }
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send email: {str(e)}',
                'sender_email': self.verified_sender,
                'recipient': recipient_email,
                'headers_applied': False
            }
    
    def _get_tracking_settings(self):
        """
        Configure email tracking settings
        """
        tracking_settings = {}
        
        # Open tracking (subtle)
        try:
            tracking_settings['open_tracking'] = OpenTracking(enable=True, substitution_tag=None)
        except:
            pass
        
        # Click tracking (minimal)
        try:
            tracking_settings['click_tracking'] = ClickTracking(enable=True, enable_text=False)
        except:
            pass
        
        # Subscription tracking (professional)
        try:
            tracking_settings['subscription_tracking'] = SubscriptionTracking(
                enable=True,
                text="If you no longer wish to receive security training emails, please contact your IT administrator.",
                html="<p style='font-size: 12px; color: #666;'>If you no longer wish to receive security training emails, please contact your IT administrator.</p>"
            )
        except:
            pass
        
        return tracking_settings
    
    def validate_email_deliverability(self, subject, content):
        """
        Validate email content for potential spam issues
        """
        issues = []
        recommendations = []
        
        # Check subject line
        if len(subject) > 50:
            issues.append("Subject line is too long (>50 characters)")
        
        if any(word in subject.upper() for word in ['FREE', 'URGENT', 'ACT NOW']):
            issues.append("Subject contains spam-trigger words")
            recommendations.append("Use professional, descriptive subject lines")
        
        # Check content
        if len(content) < 100:
            issues.append("Email content is too short")
        
        if content.count('!') > 3:
            issues.append("Too many exclamation marks")
            recommendations.append("Use professional tone")
        
        # Check for proper HTML structure
        if '<html>' not in content.lower():
            recommendations.append("Add proper HTML structure for better rendering")
        
        if 'unsubscribe' not in content.lower():
            recommendations.append("Add unsubscribe information for compliance")
        
        return {
            'deliverability_score': max(0, 100 - len(issues) * 20),
            'issues': issues,
            'recommendations': recommendations,
            'is_ready': len(issues) == 0
        }

# Utility functions
def improve_subject_line(subject):
    """
    Improve subject line for better deliverability
    """
    improvements = {
        'URGENT': 'Important',
        'FREE': 'Complimentary',
        'ACT NOW': 'Please review',
        'CLICK HERE': 'Please visit',
        'LIMITED TIME': 'Time-sensitive',
        '!!!': '.',
        'WINNER': 'Selected',
        '$$$': 'financial'
    }
    
    improved = subject
    for old, new in improvements.items():
        improved = improved.replace(old, new)
    
    return improved

def add_professional_footer(html_content):
    """
    Add professional footer to email content
    """
    footer = """
    <div style="border-top: 1px solid #ddd; margin-top: 30px; padding-top: 20px; text-align: center; font-size: 12px; color: #666;">
        <p><strong>Security Awareness Training</strong></p>
        <p>This email is part of your organization's cybersecurity training program.</p>
        <p>For questions about this training, please contact your IT security team.</p>
        <p>© 2025 HopeSecure Security Training Platform</p>
    </div>
    """
    
    if '</body>' in html_content:
        return html_content.replace('</body>', f'{footer}</body>')
    else:
        return f"{html_content}{footer}"
