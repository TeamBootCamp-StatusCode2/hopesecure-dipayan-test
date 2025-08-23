"""
Simple Domain API Views
Basic domain management without REST framework dependency
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import json

from .domain_service import DomainDNSManager, get_sendgrid_domain_suggestions, validate_domain_name
from .domain_models import EmailDomain

User = get_user_model()

def get_user_from_token(request):
    """Extract user from token in Authorization header"""
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header and auth_header.startswith('Token '):
        token_key = auth_header.split(' ')[1]
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            pass
    
    # Fallback: try to get user from session (for testing)
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    
    # Last fallback: get first superuser (for development/testing)
    try:
        return User.objects.filter(is_superuser=True).first()
    except User.DoesNotExist:
        return None

@csrf_exempt
@require_http_methods(["GET", "POST"])
def simple_domain_api(request):
    """
    Simple domain management API
    GET: List domains
    POST: Create domain
    """
    try:
        # Get user from token
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
        
        dns_manager = DomainDNSManager()
        
        if request.method == 'GET':
            # List domains
            print(f"=== API GET DOMAINS DEBUG ===")
            print(f"Request user: {user.username} (ID: {user.id})")
            print(f"User is_superuser: {user.is_superuser}")
            
            domains = dns_manager.list_user_domains(user)
            print(f"API returning {len(domains)} domains:")
            for domain in domains:
                print(f"  - {domain['name']} (ID: {domain['id']})")
            
            response_data = {
                'success': True,
                'domains': domains
            }
            print(f"Final API response: {response_data}")
            return JsonResponse(response_data)
        
        elif request.method == 'POST':
            # Create domain
            try:
                data = json.loads(request.body)
                domain_name = data.get('name', '').strip()
                domain_type = data.get('domain_type', 'spoofing')
                
                if not domain_name:
                    return JsonResponse({'success': False, 'message': 'Domain name required'})
                
                # Validate domain name
                if not validate_domain_name(domain_name):
                    return JsonResponse({'success': False, 'message': 'Invalid domain name format'})
                
                # Check if domain exists
                if EmailDomain.objects.filter(name=domain_name.lower()).exists():
                    return JsonResponse({'success': False, 'message': 'Domain already exists'})
                
                # Add domain
                success, result = dns_manager.add_domain(
                    domain_name=domain_name,
                    domain_type=domain_type,
                    user=user
                )
                
                if success:
                    return JsonResponse({
                        'success': True,
                        'message': 'Domain added successfully',
                        'data': result
                    })
                else:
                    return JsonResponse({'success': False, 'message': result})
                    
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def simple_domain_verify(request, domain_id):
    """
    Verify domain DNS records
    """
    try:
        # Get user from token
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
            
        dns_manager = DomainDNSManager()
        success, result = dns_manager.verify_domain_dns(domain_id)
        
        if success:
            return JsonResponse({
                'success': True,
                'verification_result': result
            })
        else:
            return JsonResponse({
                'success': False,
                'message': result
            }, status=400)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def simple_domain_dns_records(request, domain_id):
    """
    Get DNS records for domain
    """
    try:
        # Get user from token
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
            
        domain = EmailDomain.objects.get(id=domain_id)
        dns_manager = DomainDNSManager()
        dns_records = dns_manager.get_required_dns_records(domain)
        
        return JsonResponse({
            'success': True,
            'dns_records': dns_records
        })
    
    except EmailDomain.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Domain not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def simple_domain_delete(request, domain_id):
    """
    Delete domain
    """
    try:
        # Get user from token
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
            
        dns_manager = DomainDNSManager()
        success, message = dns_manager.delete_domain(domain_id, user)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': message
            })
        else:
            return JsonResponse({
                'success': False,
                'message': message
            }, status=404)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def simple_domain_suggestions(request):
    """
    Get domain suggestions
    """
    try:
        suggestions = get_sendgrid_domain_suggestions()
        return JsonResponse({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def simple_validate_domain(request):
    """
    Validate domain name format
    """
    try:
        data = json.loads(request.body)
        domain_name = data.get('domain_name', '')
        
        # Check format
        is_valid = validate_domain_name(domain_name)
        
        # Check if exists
        exists = EmailDomain.objects.filter(name=domain_name.lower()).exists()
        
        return JsonResponse({
            'success': True,
            'is_valid': is_valid,
            'exists': exists,
            'message': 'Valid domain format' if is_valid else 'Invalid domain format'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
