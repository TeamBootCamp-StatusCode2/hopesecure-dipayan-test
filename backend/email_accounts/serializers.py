"""
Email Accounts API Serializers
"""
from rest_framework import serializers
from .models import EmailAccount, EmailAlias, IncomingEmail, SentEmail
from campaigns.domain_models import EmailDomain


class EmailAccountSerializer(serializers.ModelSerializer):
    """Serializer for email accounts"""
    email_address = serializers.ReadOnlyField()
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    
    class Meta:
        model = EmailAccount
        fields = [
            'id', 'username', 'domain', 'domain_name', 'email_address',
            'account_type', 'status', 'created_at', 'updated_at',
            'emails_sent', 'emails_received', 'last_used',
            'auto_reply_enabled', 'auto_reply_message', 'forward_to_email'
        ]
        read_only_fields = ['created_at', 'updated_at', 'emails_sent', 'emails_received']


class EmailAccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating email accounts"""
    domain_id = serializers.IntegerField()
    
    class Meta:
        model = EmailAccount
        fields = ['username', 'domain_id', 'account_type', 'auto_reply_enabled', 'auto_reply_message']
    
    def validate(self, data):
        # Check if domain exists and user owns it
        try:
            domain = EmailDomain.objects.get(id=data['domain_id'])
            if domain.created_by != self.context['request'].user:
                raise serializers.ValidationError("You don't own this domain")
            data['domain'] = domain
        except EmailDomain.DoesNotExist:
            raise serializers.ValidationError("Domain not found")
        
        # Check if email account already exists
        if EmailAccount.objects.filter(username=data['username'], domain=domain).exists():
            raise serializers.ValidationError(f"Email account {data['username']}@{domain.name} already exists")
        
        return data
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        domain = validated_data.pop('domain')
        validated_data['domain'] = domain
        return super().create(validated_data)


class EmailAliasSerializer(serializers.ModelSerializer):
    """Serializer for email aliases"""
    alias_email = serializers.ReadOnlyField()
    target_email = serializers.CharField(source='target_account.email_address', read_only=True)
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    
    class Meta:
        model = EmailAlias
        fields = [
            'id', 'alias_name', 'domain', 'domain_name', 'alias_email',
            'target_account', 'target_email', 'created_at', 'is_active'
        ]


class IncomingEmailSerializer(serializers.ModelSerializer):
    """Serializer for incoming emails"""
    account_email = serializers.CharField(source='account.email_address', read_only=True)
    
    class Meta:
        model = IncomingEmail
        fields = [
            'id', 'account', 'account_email', 'from_email', 'from_name',
            'subject', 'text_content', 'html_content', 'received_at',
            'is_read', 'is_spam', 'has_attachments', 'attachment_count'
        ]


class SentEmailSerializer(serializers.ModelSerializer):
    """Serializer for sent emails"""
    account_email = serializers.CharField(source='account.email_address', read_only=True)
    
    class Meta:
        model = SentEmail
        fields = [
            'id', 'account', 'account_email', 'to_emails', 'cc_emails', 'bcc_emails',
            'subject', 'text_content', 'html_content', 'sent_at',
            'delivery_status', 'sendgrid_message_id'
        ]


class SendEmailSerializer(serializers.Serializer):
    """Serializer for sending emails through webmail"""
    account_id = serializers.IntegerField()
    to_emails = serializers.ListField(child=serializers.EmailField())
    cc_emails = serializers.ListField(child=serializers.EmailField(), required=False, default=list)
    bcc_emails = serializers.ListField(child=serializers.EmailField(), required=False, default=list)
    subject = serializers.CharField(max_length=500)
    text_content = serializers.CharField(required=False, default='')
    html_content = serializers.CharField(required=False, default='')
    
    def validate_account_id(self, value):
        try:
            account = EmailAccount.objects.get(id=value)
            if account.created_by != self.context['request'].user:
                raise serializers.ValidationError("You don't own this email account")
            return value
        except EmailAccount.DoesNotExist:
            raise serializers.ValidationError("Email account not found")
