"""
API endpoint to get available domains for campaign creation
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .domain_models import EmailDomain

@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Temporarily disable auth for testing
def get_available_domains(request):
    """
    Get list of verified and active domains for campaign creation
    """
    try:
        # Get only verified and active domains
        domains = EmailDomain.objects.filter(
            status__in=['verified', 'active']
        ).values('id', 'name', 'domain_type', 'status', 'emails_sent', 'emails_opened')
        
        # Format domain data for frontend
        domain_list = []
        for domain in domains:
            # Calculate success rate
            success_rate = 0
            if domain['emails_sent'] > 0:
                success_rate = (domain['emails_opened'] / domain['emails_sent']) * 100
                
            domain_list.append({
                'id': domain['id'],
                'name': domain['name'],
                'domain_type': domain['domain_type'],
                'status': domain['status'],
                'success_rate': round(success_rate, 2),
                'click_rate': 0,  # Default for now
                'display_name': f"{domain['name']} ({domain['domain_type'].title()})"
            })
        
        return Response({
            'success': True,
            'domains': domain_list,
            'total_domains': len(domain_list)
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_custom_email(request):
    """
    Generate custom email addresses with selected domains
    """
    try:
        data = request.data
        domain_id = data.get('domain_id')
        email_prefix = data.get('email_prefix', 'noreply')
        
        # Get domain
        domain = EmailDomain.objects.get(id=domain_id, created_by=request.user)
        
        # Generate email address
        custom_email = f"{email_prefix}@{domain.name}"
        
        return Response({
            'success': True,
            'email_address': custom_email,
            'domain_name': domain.name,
            'domain_type': domain.domain_type
        })
        
    except EmailDomain.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Domain not found or not accessible'
        }, status=404)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)
