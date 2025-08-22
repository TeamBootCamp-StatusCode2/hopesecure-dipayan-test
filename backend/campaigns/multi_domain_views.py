"""
Multi-Domain Campaign API Views
Frontend থেকে multiple domain দিয়ে phishing campaigns চালানোর জন্য
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
import logging
from .multi_domain_service import MultiDomainPhishingService
from .domain_models import EmailDomain

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_multi_domain_campaign(request):
    """
    Multiple domains দিয়ে phishing campaign তৈরি ও পাঠানো
    """
    try:
        data = json.loads(request.body)
        
        # Required fields validation
        required_fields = ['target_emails', 'campaign_name']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Initialize service
        service = MultiDomainPhishingService()
        
        # Campaign configuration
        campaign_config = {
            'campaign_id': f"multi_domain_{data['campaign_name']}_{request.user.id}",
            'use_random_domains': data.get('use_random_domains', True),
            'delay_seconds': data.get('delay_seconds', 2),
            'domain_type': data.get('domain_type', 'corporate')  # corporate, banking, social, etc.
        }
        
        # Send campaign
        results = service.send_multi_domain_campaign(
            target_emails=data['target_emails'],
            campaign_config=campaign_config
        )
        
        # Save campaign results to database (optional)
        # save_campaign_results(data['campaign_name'], results, request.user)
        
        return JsonResponse({
            'success': True,
            'message': 'Multi-domain campaign sent successfully',
            'results': results,
            'campaign_id': campaign_config['campaign_id']
        })
        
    except Exception as e:
        logger.error(f"Error in multi-domain campaign: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_available_domains(request):
    """
    Available verified domains এর list return করে
    """
    try:
        domains = EmailDomain.objects.filter(status='verified').values(
            'id', 'name', 'domain_type', 'emails_sent', 'success_rate'
        )
        
        domain_examples = {
            'corporate': [
                'security@microsoft-update.com',
                'notifications@google-security.net',
                'admin@office-update.org'
            ],
            'banking': [
                'fraud@bank-verification.org',
                'alerts@secure-banking.net'
            ],
            'social': [
                'security@facebook-security.info',
                'notifications@social-verify.com'
            ],
            'ecommerce': [
                'delivery@amazon-delivery.co',
                'orders@shop-tracking.net'
            ]
        }
        
        return JsonResponse({
            'success': True,
            'verified_domains': list(domains),
            'domain_examples': domain_examples,
            'total_domains': len(domains)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def test_domain_email(request):
    """
    Specific domain দিয়ে test email পাঠানো
    """
    try:
        data = json.loads(request.body)
        
        required_fields = ['test_email', 'sender_domain', 'template_type']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        service = MultiDomainPhishingService()
        
        # Create test email data
        from .domain_examples import EMAIL_TEMPLATES
        
        template_name = data['template_type']
        if template_name not in EMAIL_TEMPLATES:
            return JsonResponse({
                'success': False,
                'error': f'Invalid template type: {template_name}'
            }, status=400)
        
        tracking_url = service.generate_tracking_url(data['test_email'], 'test_campaign')
        email_data = service.create_personalized_email(template_name, data['test_email'], tracking_url)
        
        # Override sender domain if specified
        if data.get('sender_domain'):
            email_prefixes = ['security', 'notifications', 'alerts', 'support']
            prefix = data.get('sender_prefix', 'security')
            email_data['from_email'] = f"{prefix}@{data['sender_domain']}"
        
        # Send test email
        success = service.send_single_email(
            recipient_email=data['test_email'],
            **email_data
        )
        
        return JsonResponse({
            'success': success,
            'message': 'Test email sent successfully' if success else 'Failed to send test email',
            'email_details': {
                'recipient': data['test_email'],
                'sender': email_data['from_email'],
                'subject': email_data['subject'],
                'template': template_name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_domain_statistics(request):
    """
    Domain wise email statistics
    """
    try:
        service = MultiDomainPhishingService()
        stats = service.get_domain_statistics()
        
        return JsonResponse({
            'success': True,
            'domain_statistics': stats
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def add_new_domain(request):
    """
    নতুন domain add করার জন্য
    """
    try:
        data = json.loads(request.body)
        
        required_fields = ['domain_name', 'domain_type']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Check if domain already exists
        if EmailDomain.objects.filter(name=data['domain_name']).exists():
            return JsonResponse({
                'success': False,
                'error': 'Domain already exists'
            }, status=400)
        
        # Create new domain
        domain = EmailDomain.objects.create(
            name=data['domain_name'],
            domain_type=data['domain_type'],
            status='pending',
            created_by=request.user
        )
        
        # Generate DNS setup instructions
        dns_instructions = generate_dns_setup_instructions(domain)
        
        return JsonResponse({
            'success': True,
            'message': 'Domain added successfully',
            'domain_id': domain.id,
            'dns_setup': dns_instructions
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def generate_dns_setup_instructions(domain):
    """
    DNS setup instructions generate করে
    """
    return {
        'domain': domain.name,
        'instructions': [
            {
                'type': 'TXT',
                'name': f'_sendgrid.{domain.name}',
                'value': 'v=spf1 include:sendgrid.net ~all',
                'description': 'SendGrid verification record'
            },
            {
                'type': 'CNAME',
                'name': f'mail.{domain.name}',
                'value': 'sendgrid.net',
                'description': 'Email routing'
            },
            {
                'type': 'MX',
                'name': domain.name,
                'value': f'10 mx.sendgrid.net',
                'description': 'Mail exchange record'
            }
        ],
        'verification_steps': [
            '1. Add the above DNS records to your domain registrar',
            '2. Wait 24-48 hours for DNS propagation',
            '3. Click "Verify Domain" button',
            '4. Once verified, you can use this domain for campaigns'
        ]
    }
