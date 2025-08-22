"""
Domain DNS Management Service
Handle multiple domains for email campaigns
"""

import dns.resolver
import dns.exception
import hashlib
import secrets
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .domain_models import EmailDomain, DomainDNSRecord, DomainVerificationToken
import logging

logger = logging.getLogger(__name__)

class DomainDNSManager:
    """
    Manage DNS settings for email domains
    """
    
    def __init__(self):
        self.verification_timeout = 24 * 60 * 60  # 24 hours
    
    def add_domain(self, domain_name, domain_type='spoofing', user=None):
        """
        Add a new domain for email campaigns
        """
        try:
            # Check if domain already exists
            if EmailDomain.objects.filter(name=domain_name).exists():
                return False, "Domain already exists"
            
            # Create domain record
            domain = EmailDomain.objects.create(
                name=domain_name,
                domain_type=domain_type,
                status='pending',
                created_by=user
            )
            
            # Generate verification token
            verification_token = self.generate_verification_token(domain)
            
            # Create default DNS records
            self.create_default_dns_records(domain)
            
            return True, {
                'domain_id': domain.id,
                'verification_token': verification_token.token,
                'dns_records': self.get_required_dns_records(domain)
            }
            
        except Exception as e:
            logger.error(f"Failed to add domain {domain_name}: {str(e)}")
            return False, f"Error adding domain: {str(e)}"
    
    def generate_verification_token(self, domain):
        """
        Generate verification token for domain
        """
        token = secrets.token_hex(32)
        expires_at = timezone.now() + timedelta(seconds=self.verification_timeout)
        
        verification_token = DomainVerificationToken.objects.create(
            domain=domain,
            token=token,
            verification_type='dns',
            expires_at=expires_at
        )
        
        return verification_token
    
    def create_default_dns_records(self, domain):
        """
        Create default DNS records for email domain
        """
        # Default records for email sending
        default_records = [
            {
                'record_type': 'MX',
                'name': '@',
                'value': 'mail.sendgrid.net',
                'priority': 10,
                'ttl': 3600
            },
            {
                'record_type': 'TXT',
                'name': '@',
                'value': f'v=spf1 include:sendgrid.net ~all',
                'ttl': 3600
            },
            {
                'record_type': 'CNAME',
                'name': 'email',
                'value': 'sendgrid.net',
                'ttl': 3600
            },
            {
                'record_type': 'TXT',
                'name': '_dmarc',
                'value': 'v=DMARC1; p=quarantine; rua=mailto:dmarc@' + domain.name,
                'ttl': 3600
            }
        ]
        
        for record_data in default_records:
            DomainDNSRecord.objects.create(
                domain=domain,
                **record_data
            )
    
    def get_required_dns_records(self, domain):
        """
        Get all required DNS records for a domain
        """
        records = DomainDNSRecord.objects.filter(domain=domain)
        
        dns_setup = []
        for record in records:
            dns_setup.append({
                'id': record.id,
                'record_type': record.record_type,  # Change to record_type for frontend compatibility
                'name': record.name,
                'value': record.value,
                'ttl': record.ttl,
                'priority': record.priority,
                'is_verified': record.is_verified,  # Change to is_verified for frontend compatibility
                'verification_error': record.verification_error
            })
        
        return dns_setup
    
    def verify_domain_dns(self, domain_id):
        """
        Verify DNS records for a domain
        """
        try:
            domain = EmailDomain.objects.get(id=domain_id)
            dns_records = DomainDNSRecord.objects.filter(domain=domain)
            
            verification_results = []
            all_verified = True
            
            for record in dns_records:
                is_verified = self.verify_dns_record(domain.name, record)
                
                # Update record verification status
                record.is_verified = is_verified
                record.last_verification = timezone.now()
                record.verification_attempts += 1
                
                if not is_verified:
                    all_verified = False
                    record.verification_error = f"DNS record not found or incorrect"
                else:
                    record.verification_error = ""
                
                record.save()
                
                verification_results.append({
                    'record_type': record.record_type,
                    'name': record.name,
                    'verified': is_verified,
                    'error': record.verification_error
                })
            
            # Update domain status
            if all_verified:
                domain.status = 'verified'
                domain.verified_at = timezone.now()
            else:
                domain.status = 'failed'
            
            domain.save()
            
            return True, {
                'domain_verified': all_verified,
                'records': verification_results
            }
            
        except EmailDomain.DoesNotExist:
            return False, "Domain not found"
        except Exception as e:
            logger.error(f"DNS verification failed: {str(e)}")
            return False, f"Verification error: {str(e)}"
    
    def verify_dns_record(self, domain_name, dns_record):
        """
        Verify a specific DNS record
        """
        try:
            full_name = f"{dns_record.name}.{domain_name}" if dns_record.name != '@' else domain_name
            
            if dns_record.record_type == 'MX':
                answers = dns.resolver.resolve(full_name, 'MX')
                for answer in answers:
                    if dns_record.value in str(answer.exchange):
                        return True
            
            elif dns_record.record_type == 'TXT':
                answers = dns.resolver.resolve(full_name, 'TXT')
                for answer in answers:
                    txt_data = ''.join([part.decode() for part in answer.strings])
                    if dns_record.value in txt_data:
                        return True
            
            elif dns_record.record_type == 'CNAME':
                answers = dns.resolver.resolve(full_name, 'CNAME')
                for answer in answers:
                    if dns_record.value in str(answer.target):
                        return True
            
            elif dns_record.record_type == 'A':
                answers = dns.resolver.resolve(full_name, 'A')
                for answer in answers:
                    if dns_record.value == str(answer.address):
                        return True
            
            return False
            
        except dns.exception.DNSException:
            return False
        except Exception as e:
            logger.error(f"DNS record verification error: {str(e)}")
            return False
    
    def get_domain_analytics(self, domain_id):
        """
        Get analytics for a domain
        """
        try:
            domain = EmailDomain.objects.get(id=domain_id)
            
            analytics = {
                'domain_name': domain.name,
                'status': domain.status,
                'emails_sent': domain.emails_sent,
                'emails_opened': domain.emails_opened,
                'links_clicked': domain.links_clicked,
                'success_rate': domain.success_rate,
                'click_rate': domain.click_rate,
                'last_used': domain.last_used,
                'created_at': domain.created_at,
                'verified_at': domain.verified_at
            }
            
            return True, analytics
            
        except EmailDomain.DoesNotExist:
            return False, "Domain not found"
    
    def list_user_domains(self, user):
        """
        List all domains for a user
        """
        domains = EmailDomain.objects.filter(created_by=user).order_by('-created_at')
        
        domain_list = []
        for domain in domains:
            domain_list.append({
                'id': domain.id,
                'name': domain.name,
                'type': domain.domain_type,
                'status': domain.status,
                'emails_sent': domain.emails_sent,
                'success_rate': domain.success_rate,
                'verified_at': domain.verified_at,
                'created_at': domain.created_at
            })
        
        return domain_list
    
    def delete_domain(self, domain_id, user):
        """
        Delete a domain and all associated records
        """
        try:
            domain = EmailDomain.objects.get(id=domain_id, created_by=user)
            domain_name = domain.name
            domain.delete()
            
            return True, f"Domain {domain_name} deleted successfully"
            
        except EmailDomain.DoesNotExist:
            return False, "Domain not found or no permission"
    
    def update_domain_settings(self, domain_id, settings_data, user):
        """
        Update domain settings
        """
        try:
            domain = EmailDomain.objects.get(id=domain_id, created_by=user)
            
            # Update allowed settings
            if 'max_emails_per_day' in settings_data:
                domain.max_emails_per_day = settings_data['max_emails_per_day']
            
            if 'rate_limit_per_hour' in settings_data:
                domain.rate_limit_per_hour = settings_data['rate_limit_per_hour']
            
            if 'click_tracking_enabled' in settings_data:
                domain.click_tracking_enabled = settings_data['click_tracking_enabled']
            
            if 'open_tracking_enabled' in settings_data:
                domain.open_tracking_enabled = settings_data['open_tracking_enabled']
            
            domain.save()
            
            return True, "Domain settings updated successfully"
            
        except EmailDomain.DoesNotExist:
            return False, "Domain not found or no permission"

# Helper functions
def get_sendgrid_domain_suggestions():
    """
    Get domain suggestions for SendGrid integration
    """
    return [
        {
            'domain': 'secure-notifications.com',
            'type': 'spoofing',
            'description': 'General security notifications'
        },
        {
            'domain': 'company-alerts.net',
            'type': 'spoofing',
            'description': 'Corporate alert messages'
        },
        {
            'domain': 'account-verify.org',
            'type': 'spoofing',
            'description': 'Account verification emails'
        },
        {
            'domain': 'security-updates.info',
            'type': 'spoofing',
            'description': 'Security update notifications'
        }
    ]

def validate_domain_name(domain_name):
    """
    Validate domain name format
    """
    import re
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return re.match(pattern, domain_name) is not None
