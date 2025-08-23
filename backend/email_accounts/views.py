"""
Email Accounts API Views
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
import sendgrid
from sendgrid.helpers.mail import Mail

from .models import EmailAccount, EmailAlias, IncomingEmail, SentEmail
from campaigns.domain_models import EmailDomain
from .serializers import (
    EmailAccountSerializer, EmailAccountCreateSerializer,
    EmailAliasSerializer, IncomingEmailSerializer, SentEmailSerializer,
    SendEmailSerializer
)
from campaigns.domain_models import EmailDomain


class EmailAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing email accounts
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmailAccountCreateSerializer
        return EmailAccountSerializer
    
    def get_queryset(self):
        # Simplified - show all email accounts for any authenticated user
        return EmailAccount.objects.all()
    
    def create(self, request, *args, **kwargs):
        """Create a new email account and return with ID"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        
        # Return full account data including ID
        response_serializer = EmailAccountSerializer(account)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def send_test_email(self, request, pk=None):
        """Send a test email from this account"""
        account = self.get_object()
        
        try:
            from django.conf import settings
            sg = sendgrid.SendGridAPIClient(api_key=settings.PHISHING_EMAIL_SETTINGS['SENDGRID_API_KEY'])
            
            message = Mail(
                from_email=account.email_address,
                to_emails=request.user.email,
                subject=f'Test Email from {account.email_address}',
                html_content=f'''
                <h2>✅ Email Account Test Successful</h2>
                <p>This test email was sent from: <strong>{account.email_address}</strong></p>
                <p>Account Type: {account.get_account_type_display()}</p>
                <p>Domain: {account.domain.name}</p>
                <hr>
                <small>Sent from HopeSecure Email Management System</small>
                '''
            )
            
            response = sg.send(message)
            
            if response.status_code == 202:
                # Update account stats
                account.emails_sent += 1
                account.last_used = timezone.now()
                account.save()
                
                return Response({
                    'success': True,
                    'message': f'Test email sent successfully from {account.email_address}'
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Failed to send test email'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error sending test email: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def inbox(self, request, pk=None):
        """Get inbox emails for this account"""
        account = self.get_object()
        emails = IncomingEmail.objects.filter(account=account).order_by('-received_at')[:50]
        serializer = IncomingEmailSerializer(emails, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def sent_emails(self, request, pk=None):
        """Get sent emails for this account"""
        account = self.get_object()
        emails = SentEmail.objects.filter(account=account).order_by('-sent_at')[:50]
        serializer = SentEmailSerializer(emails, many=True)
        return Response(serializer.data)


class SendEmailView(viewsets.ViewSet):
    """
    API endpoint for sending emails
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request):
        """Send an email through webmail interface"""
        serializer = SendEmailSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                # Get validated data
                account_id = serializer.validated_data['account_id']
                account = get_object_or_404(EmailAccount, id=account_id, created_by=request.user)
                
                to_emails = serializer.validated_data['to_emails']
                cc_emails = serializer.validated_data.get('cc_emails', [])
                bcc_emails = serializer.validated_data.get('bcc_emails', [])
                subject = serializer.validated_data['subject']
                text_content = serializer.validated_data.get('text_content', '')
                html_content = serializer.validated_data.get('html_content', '')
                
                # Send via SendGrid
                from django.conf import settings
                sg = sendgrid.SendGridAPIClient(api_key=settings.PHISHING_EMAIL_SETTINGS['SENDGRID_API_KEY'])
                
                # Create email message
                message = Mail(
                    from_email=account.email_address,
                    to_emails=to_emails,
                    subject=subject
                )
                
                if html_content:
                    message.content = html_content
                else:
                    message.content = text_content
                
                # Add CC and BCC
                if cc_emails:
                    for cc_email in cc_emails:
                        message.add_cc(cc_email)
                
                if bcc_emails:
                    for bcc_email in bcc_emails:
                        message.add_bcc(bcc_email)
                
                # Send email
                response = sg.send(message)
                
                if response.status_code == 202:
                    # Save to sent emails
                    sent_email = SentEmail.objects.create(
                        account=account,
                        to_emails=to_emails,
                        cc_emails=cc_emails,
                        bcc_emails=bcc_emails,
                        subject=subject,
                        text_content=text_content,
                        html_content=html_content,
                        delivery_status='sent',
                        sendgrid_message_id=response.headers.get('X-Message-Id', '')
                    )
                    
                    # Update account stats
                    account.emails_sent += 1
                    account.last_used = timezone.now()
                    account.save()
                    
                    return Response({
                        'success': True,
                        'message': 'Email sent successfully',
                        'email_id': sent_email.id,
                        'recipients': len(to_emails + cc_emails + bcc_emails)
                    })
                else:
                    return Response({
                        'success': False,
                        'message': f'Failed to send email. Status: {response.status_code}'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
            except Exception as e:
                return Response({
                    'success': False,
                    'message': f'Error sending email: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailDomainQuickSetupView(viewsets.ViewSet):
    """
    Quick setup for email accounts on existing domains
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def available_domains(self, request):
        """Get all verified domains - simplified access"""
        domains = EmailDomain.objects.filter(status='verified')
        domain_data = domains.values('id', 'name', 'status', 'emails_sent')
        return Response(list(domain_data))
    
    @action(detail=False, methods=['post'])
    def quick_setup(self, request):
        """Quickly create common email accounts for a domain"""
        domain_id = request.data.get('domain_id')
        account_types = request.data.get('account_types', ['admin', 'support'])
        
        try:
            domain = get_object_or_404(EmailDomain, id=domain_id, created_by=request.user)
            created_accounts = []
            
            for account_type in account_types:
                # Check if account already exists
                if not EmailAccount.objects.filter(username=account_type, domain=domain).exists():
                    account = EmailAccount.objects.create(
                        username=account_type,
                        domain=domain,
                        account_type=account_type,
                        created_by=request.user,
                        status='active'
                    )
                    created_accounts.append({
                        'email': account.email_address,
                        'type': account.account_type
                    })
            
            return Response({
                'success': True,
                'message': f'Created {len(created_accounts)} email accounts',
                'accounts': created_accounts,
                'domain': domain.name
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error creating accounts: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
