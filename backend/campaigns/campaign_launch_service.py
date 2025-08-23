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
        
        # Debug logging
        print(f"🔍 Campaign Launch Debug:")
        print(f"   Received data: {data}")
        print(f"   Sender email: {data.get('sender_email')}")
        print(f"   Target emails: {data.get('target_emails')}")
        
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
        
        # Get template content if template_id is provided
        template_id = data.get('template_id')
        email_subject = f"Security Update - {campaign_name}"
        email_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Security Notice</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
                .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .content {{ background: white; padding: 25px; border: 1px solid #e0e0e0; border-radius: 8px; }}
                .notice {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
                .btn {{ display: inline-block; padding: 12px 24px; background: #1976d2; color: white; text-decoration: none; border-radius: 6px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2 style="margin: 0; color: #1976d2;">IT Security Department</h2>
                <p style="margin: 5px 0 0 0; color: #666;">Security Awareness Training</p>
            </div>
            <div class="content">
                <h3>Security Training Exercise</h3>
                <p>Dear Team Member,</p>
                <p>This message is part of our ongoing cybersecurity awareness training program.</p>
                <p><strong>Training Campaign:</strong> {campaign_name}</p>
                <div class="notice">
                    <p><strong>📚 Educational Purpose</strong></p>
                    <p>This is a simulated security scenario designed to help you identify potential threats.</p>
                    <p>Your participation helps strengthen our organization's security posture.</p>
                </div>
                <p>For more information about cybersecurity best practices, please visit our internal security portal.</p>
            </div>
            <div class="footer">
                <p><strong>Security Awareness Training Program</strong></p>
                <p>This email is part of your organization's cybersecurity education initiative.</p>
                <p>Questions? Contact your IT security team at security@company.com</p>
                <p>© 2025 IT Security Department</p>
            </div>
        </body>
        </html>
        """
        
        # If template_id is provided, use template content
        if template_id:
            try:
                from templates.models import Template
                template = Template.objects.get(id=template_id)
                email_subject = template.email_subject or email_subject
                
                # Use template's HTML content if available
                if template.html_content:
                    email_html = template.html_content
                    
                    # Add CSS styles if available
                    if template.css_styles:
                        email_html = f"""
                        <html>
                        <head>
                            <style>
                                {template.css_styles}
                            </style>
                        </head>
                        <body>
                            {template.html_content}
                        </body>
                        </html>
                        """
                
                # Update template usage count
                template.usage_count += 1
                template.save()
                
            except Template.DoesNotExist:
                # If template not found, use default content but don't fail
                pass
            except Exception as e:
                # Log error but continue with default template
                print(f"Error loading template {template_id}: {e}")
        
        
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
                    # Use SendGrid directly for regular campaigns (Fallback)
                    import os
                    from django.conf import settings
                    
                    try:
                        # Try to use anti-spam service first
                        from .anti_spam_service import AntiSpamEmailService
                        email_service = AntiSpamEmailService()
                        result = email_service.send_campaign_email(
                            recipient_email=target_email,
                            subject=email_subject,
                            html_content=email_html,
                            sender_name="IT Security Team",
                            campaign_id=campaign_name
                        )
                    except Exception as fallback_error:
                        print(f"Anti-spam service failed, using fallback: {fallback_error}")
                        
                        # Fallback to basic SendGrid
                        try:
                            from sendgrid import SendGridAPIClient
                            from sendgrid.helpers.mail import Mail
                            
                            # Get API key from Django settings
                            api_key = settings.PHISHING_EMAIL_SETTINGS.get('SENDGRID_API_KEY')
                            sg = SendGridAPIClient(api_key=api_key)
                            
                            # Use verified sender email
                            verified_sender_email = "hope@hopesecure.tech"
                            
                            message = Mail(
                                from_email=verified_sender_email,
                                to_emails=target_email,
                                subject=email_subject,
                                html_content=email_html
                            )
                            
                            response = sg.send(message)
                            result = {
                                'success': True,
                                'status_code': response.status_code,
                                'message': 'Email sent successfully via SendGrid (fallback)',
                                'sender_email': verified_sender_email,
                                'recipient': target_email
                            }
                        except Exception as sg_error:
                            result = {
                                'success': False,
                                'message': f'SendGrid fallback error: {str(sg_error)}',
                                'sender_email': 'hope@hopesecure.tech',
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
