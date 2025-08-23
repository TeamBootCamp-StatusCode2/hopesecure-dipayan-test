"""
SendGrid Verification API Views
Manage sender verification through web interface
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from sendgrid import SendGridAPIClient
import json
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_verified_senders(request):
    """
    Get list of all verified senders with their status
    """
    try:
        api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient(api_key=api_key)
        
        response = sg.client.verified_senders.get()
        data = json.loads(response.body.decode('utf-8'))
        
        # Format response for frontend
        senders = []
        for sender in data.get('results', []):
            senders.append({
                'id': sender.get('id'),
                'email': sender.get('from_email'),
                'name': sender.get('from_name'),
                'verified': sender.get('verified', False),
                'nickname': sender.get('nickname'),
                'reply_to': sender.get('reply_to'),
                'created_at': sender.get('created_at')
            })
        
        return Response({
            'success': True,
            'senders': senders,
            'total': len(senders),
            'verified_count': len([s for s in senders if s['verified']])
        })
        
    except Exception as e:
        logger.error(f"Error getting verified senders: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_verified_sender(request):
    """
    Create a new verified sender
    """
    try:
        email = request.data.get('email')
        name = request.data.get('name', 'HopeSecure Team')
        reply_to = request.data.get('reply_to', email)
        
        if not email:
            return Response({
                'success': False,
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient(api_key=api_key)
        
        # Create sender data
        data = {
            'nickname': email.split('@')[0].replace('.', '_').replace('+', '_'),
            'from_email': email,
            'from_name': name,
            'reply_to': reply_to,
            'reply_to_name': name,
            'address': 'HopeSecure Security Training',
            'address2': 'Digital Security Division',
            'city': 'Dhaka',
            'state': 'DH',  # 2 character state code
            'country': 'Bangladesh',
            'zip': '1000'
        }
        
        response = sg.client.verified_senders.post(request_body=data)
        result = json.loads(response.body.decode('utf-8'))
        
        return Response({
            'success': True,
            'message': f'Verification email sent to {email}',
            'sender_id': result.get('id'),
            'email': email,
            'verification_required': True
        })
        
    except Exception as e:
        logger.error(f"Error creating verified sender: {e}")
        error_message = str(e)
        
        # Parse SendGrid error details
        if hasattr(e, 'body'):
            try:
                error_data = json.loads(e.body.decode('utf-8'))
                if 'errors' in error_data:
                    error_message = error_data['errors'][0].get('message', str(e))
            except:
                pass
        
        return Response({
            'success': False,
            'error': error_message
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification(request):
    """
    Resend verification email for a sender
    """
    try:
        sender_id = request.data.get('sender_id')
        
        if not sender_id:
            return Response({
                'success': False,
                'error': 'sender_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient(api_key=api_key)
        
        # Try different API endpoints for resending verification
        try:
            response = sg.client.verified_senders._(sender_id).resend.post()
        except:
            # Alternative endpoint
            response = sg.client.verified_senders.resend.post(request_body={'id': sender_id})
        
        return Response({
            'success': True,
            'message': 'Verification email resent successfully'
        })
        
    except Exception as e:
        logger.error(f"Error resending verification: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_verified_sender(request, sender_id):
    """
    Delete a verified sender
    """
    try:
        api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient(api_key=api_key)
        
        response = sg.client.verified_senders._(sender_id).delete()
        
        return Response({
            'success': True,
            'message': 'Sender deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting sender: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_verification_status(request):
    """
    Check overall verification status and provide recommendations
    """
    try:
        api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient(api_key=api_key)
        
        # Get verified senders
        response = sg.client.verified_senders.get()
        senders_data = json.loads(response.body.decode('utf-8'))
        senders = senders_data.get('results', [])
        
        # Check domain authentication
        try:
            domain_response = sg.client.whitelabel.domains.get()
            domains = json.loads(domain_response.body.decode('utf-8'))
        except:
            domains = []
        
        # Analyze status
        verified_senders = [s for s in senders if s.get('verified')]
        pending_senders = [s for s in senders if not s.get('verified')]
        
        # Recommendations
        recommendations = []
        if not verified_senders:
            recommendations.append({
                'type': 'warning',
                'message': 'No verified senders found. Add and verify at least one sender email.',
                'action': 'create_sender'
            })
        
        if not domains:
            recommendations.append({
                'type': 'info',
                'message': 'Consider adding domain authentication for better email deliverability.',
                'action': 'setup_domain'
            })
        
        if pending_senders:
            recommendations.append({
                'type': 'info',
                'message': f'{len(pending_senders)} sender(s) pending verification. Check email inbox.',
                'action': 'verify_email'
            })
        
        return Response({
            'success': True,
            'status': {
                'total_senders': len(senders),
                'verified_senders': len(verified_senders),
                'pending_senders': len(pending_senders),
                'domain_authenticated': len([d for d in domains if d.get('valid')])
            },
            'verified_emails': [s.get('from_email') for s in verified_senders],
            'pending_emails': [s.get('from_email') for s in pending_senders],
            'recommendations': recommendations,
            'ready_for_sending': len(verified_senders) > 0
        })
        
    except Exception as e:
        logger.error(f"Error checking verification status: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
