from django.contrib import admin
from .models import EmailAccount, EmailAlias, IncomingEmail, SentEmail


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ['email_address', 'account_type', 'status', 'created_at', 'emails_sent']
    list_filter = ['account_type', 'status', 'domain']
    search_fields = ['username', 'domain__name']
    readonly_fields = ['email_address', 'created_at', 'updated_at']


@admin.register(EmailAlias)
class EmailAliasAdmin(admin.ModelAdmin):
    list_display = ['alias_email', 'target_account', 'is_active', 'created_at']
    list_filter = ['is_active', 'domain']


@admin.register(IncomingEmail)
class IncomingEmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'from_email', 'account', 'received_at', 'is_read']
    list_filter = ['is_read', 'is_spam', 'received_at']
    search_fields = ['subject', 'from_email']


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'account', 'sent_at', 'delivery_status']
    list_filter = ['delivery_status', 'sent_at']
    search_fields = ['subject', 'to_emails']
