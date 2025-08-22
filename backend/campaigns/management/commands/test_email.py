"""
Django management command to test SendGrid email sending
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test SendGrid email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default='bolbonakano@gmail.com',
            help='Recipient email address'
        )
        parser.add_argument(
            '--from',
            type=str,
            default=None,
            help='Sender email address'
        )

    def handle(self, *args, **options):
        recipient = options['to']
        sender = options['from'] or getattr(settings, 'DEFAULT_FROM_EMAIL', 'bolbonakano@gmail.com')
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Testing SendGrid Email Configuration')
        )
        self.stdout.write(f"From: {sender}")
        self.stdout.write(f"To: {recipient}")
        self.stdout.write(f"SMTP Host: {getattr(settings, 'EMAIL_HOST', 'Not configured')}")
        
        try:
            result = send_mail(
                subject='HopeSecure SendGrid Test - Management Command',
                message='This is a test email from HopeSecure using Django management command.',
                from_email=sender,
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            if result == 1:
                self.stdout.write(
                    self.style.SUCCESS('✅ Email sent successfully!')
                )
                self.stdout.write('Check your inbox and spam folder.')
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Email sending failed')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {e}')
            )
            
            # Provide helpful suggestions
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('💡 Troubleshooting tips:'))
            self.stdout.write('1. Verify your sender identity in SendGrid:')
            self.stdout.write('   https://app.sendgrid.com/settings/sender_auth')
            self.stdout.write('2. Use a verified email address as sender')
            self.stdout.write('3. Check your SendGrid API key permissions')
