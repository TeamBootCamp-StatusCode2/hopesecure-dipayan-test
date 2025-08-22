"""
Campaign Launch Service
Handles complete campaign execution with custom domains
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .domain_models import EmailDomain
from .custom_domain_email_service import CustomDomainEmailService

@csrf_exempt
@require_http_methods(["POST"])
def launch_campaign(request):
    """
    Launch a complete phishing campaign with custom domain
    """
    try:
        data = json.loads(request.body)
        
        # Extract campaign data
        campaign_name = data.get('name')
        target_emails = data.get('target_emails', [])
        sender_email = data.get('sender_email')
        domain_id = data.get('domain_id')
        template_id = data.get('template_id')
        use_custom_domain = data.get('use_custom_domain', False)
        
        # Validation
        if not campaign_name or not target_emails or not sender_email:
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields: name, target_emails, sender_email'
            }, status=400)
        
        # Initialize results
        campaign_results = {
            'campaign_name': campaign_name,
            'sender_email': sender_email,
            'total_targets': len(target_emails),
            'successful_sends': 0,
            'failed_sends': 0,
            'email_results': [],
            'domain_info': None
        }
        
        # Get domain info if using custom domain
        if use_custom_domain and domain_id:
            try:
                domain = EmailDomain.objects.get(id=domain_id)
                campaign_results['domain_info'] = {
                    'name': domain.name,
                    'type': domain.domain_type,
                    'status': domain.status
                }
            except EmailDomain.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f'Domain with ID {domain_id} not found'
                }, status=404)
        
        # Email content (simplified for now)
        email_subject = f"Security Awareness Test - {campaign_name}"
        email_html = f"""
        <html>
        <body>
            <h2>Security Awareness Test</h2>
            <p>This is a simulated phishing email for security awareness training.</p>
            <p><strong>Campaign:</strong> {campaign_name}</p>
            <p><strong>From:</strong> {sender_email}</p>
            <br>
            <div style="background: #f0f0f0; padding: 15px; border-radius: 5px;">
                <p><strong>⚠️ This is a simulation!</strong></p>
                <p>If this were a real phishing attack, you would have been compromised.</p>
                <p>Learn more about cybersecurity awareness.</p>
            </div>
        </body>
        </html>
        """
        
        # Initialize email service
        if use_custom_domain:
            email_service = CustomDomainEmailService()
        
        # Send emails to each target
        for target_email in target_emails:
            try:
                if use_custom_domain:
                    # Use custom domain email service
                    email_service = CustomDomainEmailService()
                    result = email_service.send_phishing_email(
                        sender_email=sender_email,
                        recipient_email=target_email,
                        subject=email_subject,
                        html_content=email_html,
                        domain_id=domain_id
                    )
                else:
                    # Use SendGrid directly for regular campaigns
                    import os
                    from sendgrid import SendGridAPIClient
                    from sendgrid.helpers.mail import Mail
                    
                    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
                    message = Mail(
                        from_email=sender_email,
                        to_emails=target_email,
                        subject=email_subject,
                        html_content=email_html
                    )
                    
                    try:
                        response = sg.send(message)
                        result = {
                            'success': True,
                            'status_code': response.status_code,
                            'message': 'Email sent successfully via SendGrid',
                            'sender_email': sender_email,
                            'recipient': target_email
                        }
                    except Exception as sg_error:
                        result = {
                            'success': False,
                            'message': f'SendGrid error: {str(sg_error)}',
                            'sender_email': sender_email,
                            'recipient': target_email
                        }
                
                if result['success']:
                    campaign_results['successful_sends'] += 1
                else:
                    campaign_results['failed_sends'] += 1
                
                campaign_results['email_results'].append({
                    'recipient': target_email,
                    'success': result['success'],
                    'message': result.get('message', 'Unknown status'),
                    'details': result.get('status_code', 'N/A')
                })
                
            except Exception as e:
                campaign_results['failed_sends'] += 1
                campaign_results['email_results'].append({
                    'recipient': target_email,
                    'success': False,
                    'message': f'Exception: {str(e)}'
                })
        
        # Calculate success rate
        success_rate = 0
        if campaign_results['total_targets'] > 0:
            success_rate = (campaign_results['successful_sends'] / campaign_results['total_targets']) * 100
        
        campaign_results['success_rate'] = round(success_rate, 2)
        
        return JsonResponse({
            'success': True,
            'message': 'Campaign launched successfully',
            'results': campaign_results
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Campaign launch failed: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def validate_campaign_setup(request):
    """
    Validate campaign setup before launch
    """
    try:
        data = json.loads(request.body)
        
        validation_results = {
            'ready_to_launch': True,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check required fields
        required_fields = ['name', 'target_emails', 'template_id']
        for field in required_fields:
            if not data.get(field):
                validation_results['issues'].append(f'Missing required field: {field}')
                validation_results['ready_to_launch'] = False
        
        # Check target emails
        target_emails = data.get('target_emails', [])
        if len(target_emails) == 0:
            validation_results['issues'].append('No target emails specified')
            validation_results['ready_to_launch'] = False
        elif len(target_emails) > 100:
            validation_results['warnings'].append(f'Large recipient list ({len(target_emails)} emails). Consider splitting into smaller campaigns.')
        
        # Check custom domain setup
        if data.get('use_custom_domain'):
            domain_id = data.get('domain_id')
            if not domain_id:
                validation_results['issues'].append('Custom domain selected but no domain specified')
                validation_results['ready_to_launch'] = False
            else:
                try:
                    domain = EmailDomain.objects.get(id=domain_id)
                    if domain.status != 'verified':
                        validation_results['issues'].append(f'Domain {domain.name} is not verified')
                        validation_results['ready_to_launch'] = False
                    else:
                        validation_results['recommendations'].append(f'Using verified domain: {domain.name}')
                except EmailDomain.DoesNotExist:
                    validation_results['issues'].append('Selected domain not found')
                    validation_results['ready_to_launch'] = False
        
        return JsonResponse({
            'success': True,
            'validation': validation_results
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
