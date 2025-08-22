"""
Phishing Email Service
Email domain mimicking এবং spoofing এর জন্য service
"""

from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import ssl
from .email_config import EMAIL_CONFIGURATIONS, DOMAIN_SPOOFING_METHODS
import logging

logger = logging.getLogger(__name__)

class PhishingEmailService:
    """
    Phishing Campaign এর জন্য email sending service
    Domain mimicking এবং spoofing capabilities সহ
    """
    
    def __init__(self, campaign=None):
        self.campaign = campaign
        self.email_config = None
        
    def setup_email_config(self, config_type='corporate_mimic'):
        """Email configuration setup করা"""
        if config_type in EMAIL_CONFIGURATIONS:
            self.email_config = EMAIL_CONFIGURATIONS[config_type]
            return True
        return False
    
    def generate_mimic_domain(self, target_domain, method='homograph'):
        """
        Target domain এর অনুকরণে নতুন domain তৈরি করা
        """
        if method == 'homograph':
            # Character substitution
            mimic_domains = []
            substitutions = {
                'o': '0',
                'i': '1',
                'l': 'I',
                'e': '3',
                'a': '@'
            }
            
            for char, sub in substitutions.items():
                if char in target_domain:
                    mimic_domains.append(target_domain.replace(char, sub, 1))
            
            return mimic_domains
            
        elif method == 'subdomain':
            # Subdomain spoofing
            return [
                f"security.{target_domain.split('.')[0]}-verify.com",
                f"login.{target_domain.split('.')[0]}-support.net",
                f"notification.{target_domain.split('.')[0]}-alert.org"
            ]
            
        elif method == 'tld_variation':
            # TLD variation
            domain_name = target_domain.split('.')[0]
            return [
                f"{domain_name}.net",
                f"{domain_name}.org", 
                f"{domain_name}.co",
                f"{domain_name}.info"
            ]
    
    def create_spoofed_email_headers(self, sender_name, sender_email, target_domain):
        """
        Spoofed email headers তৈরি করা
        """
        # Generate mimic domain
        mimic_domains = self.generate_mimic_domain(target_domain)
        selected_domain = mimic_domains[0] if mimic_domains else sender_email.split('@')[1]
        
        # Create spoofed sender
        spoofed_email = f"{sender_email.split('@')[0]}@{selected_domain}"
        
        headers = {
            'From': f"{sender_name} <{spoofed_email}>",
            'Reply-To': spoofed_email,
            'Return-Path': spoofed_email,
            'X-Originating-IP': '[192.168.1.100]',  # Fake IP
            'X-Mailer': 'Microsoft Outlook 16.0',  # Fake mailer
        }
        
        return headers, spoofed_email
    
    def send_phishing_email(self, 
                          recipient_email, 
                          subject, 
                          html_content, 
                          sender_name="IT Security Team",
                          sender_email="security@company.com",
                          target_domain="company.com",
                          use_spoofing=True):
        """
        Phishing email পাঠানো
        """
        try:
            # Email configuration setup
            if not self.email_config:
                self.setup_email_config('corporate_mimic')
            
            if use_spoofing:
                # Create spoofed headers
                headers, spoofed_sender = self.create_spoofed_email_headers(
                    sender_name, sender_email, target_domain
                )
                from_email = headers['From']
            else:
                from_email = f"{sender_name} <{sender_email}>"
                headers = {}
            
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['To'] = recipient_email
            msg['From'] = from_email
            
            # Add custom headers for spoofing
            for header_name, header_value in headers.items():
                if header_name not in ['From', 'To', 'Subject']:
                    msg[header_name] = header_value
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Send email using SMTP
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.email_config['smtp_host'], self.email_config['smtp_port']) as server:
                if self.email_config.get('use_tls'):
                    server.starttls(context=context)
                
                # For development, you might need authentication
                # server.login(username, password)
                
                # Send email
                server.send_message(msg)
                
            logger.info(f"Phishing email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send phishing email: {str(e)}")
            return False
    
    def send_campaign_emails(self, target_emails, template_data):
        """
        Campaign এর সব emails পাঠানো
        """
        sent_count = 0
        failed_count = 0
        
        for email in target_emails:
            # Personalize email content
            personalized_content = self.personalize_email_content(
                template_data['html_content'], 
                email
            )
            
            success = self.send_phishing_email(
                recipient_email=email,
                subject=template_data['subject'],
                html_content=personalized_content,
                sender_name=template_data.get('sender_name', 'IT Security'),
                sender_email=template_data.get('sender_email', 'security@company.com'),
                target_domain=template_data.get('target_domain', 'company.com'),
                use_spoofing=template_data.get('use_spoofing', True)
            )
            
            if success:
                sent_count += 1
            else:
                failed_count += 1
        
        return {
            'sent': sent_count,
            'failed': failed_count,
            'total': len(target_emails)
        }
    
    def personalize_email_content(self, html_content, recipient_email):
        """
        Email content personalization
        """
        # Extract name from email
        name = recipient_email.split('@')[0].title()
        
        # Replace placeholders
        personalized = html_content.replace('{{recipient_name}}', name)
        personalized = personalized.replace('{{recipient_email}}', recipient_email)
        
        return personalized

# Helper functions
def get_available_mimic_domains():
    """Available mimic domains এর list"""
    domains = []
    for config in EMAIL_CONFIGURATIONS.values():
        domains.extend(config.get('mimic_domains', []))
    return domains

def get_spoofing_methods():
    """Available spoofing methods"""
    return list(DOMAIN_SPOOFING_METHODS.keys())
