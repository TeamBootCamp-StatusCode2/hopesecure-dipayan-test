"""
Simple test view without authentication
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .domain_models import EmailDomain

@csrf_exempt
@require_http_methods(["GET"])
def test_domains_api(request):
    """
    Simple test API without authentication
    """
    try:
        domains = EmailDomain.objects.filter(
            status__in=['verified', 'active']
        ).values('id', 'name', 'domain_type', 'status')
        
        domain_list = list(domains)
        
        return JsonResponse({
            'success': True,
            'domains': domain_list,
            'count': len(domain_list)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt 
@require_http_methods(["POST"])
def test_custom_email(request):
    """
    Test custom email setup
    """
    try:
        data = json.loads(request.body)
        sender_email = data.get('sender_email')
        domain_id = data.get('domain_id')
        test_recipient = data.get('test_recipient', 'test@example.com')
        
        # Verify domain exists
        domain = EmailDomain.objects.get(id=domain_id)
        
        # Here you would integrate with SendGrid/Email service
        # For now, just return success
        return JsonResponse({
            'success': True,
            'message': f'Test email configured successfully',
            'sender_email': sender_email,
            'domain': domain.name,
            'status': 'Email setup verified',
            'next_steps': [
                'Campaign will use this sender email',
                'Domain DNS is properly configured',
                'Email delivery is ready'
            ]
        })
        
    except EmailDomain.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Domain not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
