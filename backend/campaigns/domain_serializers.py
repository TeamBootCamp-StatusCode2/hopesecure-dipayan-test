"""
Domain Management Serializers
For API endpoints to manage email domains
"""

from rest_framework import serializers
from .domain_models import EmailDomain, DomainDNSRecord, EmailTemplate, DomainVerificationToken


class DomainDNSRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for DNS records
    """
    class Meta:
        model = DomainDNSRecord
        fields = [
            'id', 'record_type', 'name', 'value', 'ttl', 'priority',
            'is_verified', 'verification_attempts', 'verification_error',
            'last_verification', 'created_at'
        ]
        read_only_fields = ['is_verified', 'verification_attempts', 'verification_error', 'last_verification']


class EmailDomainSerializer(serializers.ModelSerializer):
    """
    Serializer for email domains
    """
    dns_records = DomainDNSRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = EmailDomain
        fields = [
            'id', 'name', 'domain_type', 'status', 'verification_method',
            'max_emails_per_day', 'rate_limit_per_hour', 'emails_sent',
            'emails_opened', 'links_clicked', 'success_rate', 'click_rate',
            'click_tracking_enabled', 'open_tracking_enabled', 'last_used',
            'verified_at', 'created_at', 'dns_records'
        ]
        read_only_fields = [
            'status', 'emails_sent', 'emails_opened', 'links_clicked',
            'success_rate', 'click_rate', 'last_used', 'verified_at'
        ]
    
    def validate_name(self, value):
        """
        Validate domain name format
        """
        import re
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid domain name format")
        return value.lower()


class EmailDomainCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating email domains
    """
    class Meta:
        model = EmailDomain
        fields = ['name', 'domain_type', 'verification_method']
    
    def validate_name(self, value):
        """
        Validate domain name and check uniqueness
        """
        import re
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid domain name format")
        
        # Check if domain already exists
        if EmailDomain.objects.filter(name=value.lower()).exists():
            raise serializers.ValidationError("Domain already exists")
        
        return value.lower()


class EmailTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for email templates linked to domains
    """
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    
    class Meta:
        model = EmailTemplate
        fields = [
            'id', 'name', 'subject', 'content', 'template_type',
            'language', 'is_active', 'domain', 'domain_name',
            'usage_count', 'success_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['usage_count', 'success_rate']


class DomainVerificationTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for domain verification tokens
    """
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    
    class Meta:
        model = DomainVerificationToken
        fields = [
            'id', 'domain', 'domain_name', 'token', 'verification_type',
            'is_used', 'expires_at', 'created_at'
        ]
        read_only_fields = ['token', 'is_used']


class DomainAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for domain analytics data
    """
    domain_name = serializers.CharField()
    status = serializers.CharField()
    emails_sent = serializers.IntegerField()
    emails_opened = serializers.IntegerField()
    links_clicked = serializers.IntegerField()
    success_rate = serializers.FloatField()
    click_rate = serializers.FloatField()
    last_used = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    verified_at = serializers.DateTimeField()


class DomainListSerializer(serializers.Serializer):
    """
    Serializer for domain list view
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    status = serializers.CharField()
    emails_sent = serializers.IntegerField()
    success_rate = serializers.FloatField()
    verified_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class DomainSettingsSerializer(serializers.Serializer):
    """
    Serializer for updating domain settings
    """
    max_emails_per_day = serializers.IntegerField(min_value=1, max_value=10000, required=False)
    rate_limit_per_hour = serializers.IntegerField(min_value=1, max_value=1000, required=False)
    click_tracking_enabled = serializers.BooleanField(required=False)
    open_tracking_enabled = serializers.BooleanField(required=False)


class DNSRecordCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating DNS records
    """
    class Meta:
        model = DomainDNSRecord
        fields = ['record_type', 'name', 'value', 'ttl', 'priority']
    
    def validate_record_type(self, value):
        """
        Validate DNS record type
        """
        valid_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SRV']
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid record type. Must be one of: {', '.join(valid_types)}")
        return value
    
    def validate_ttl(self, value):
        """
        Validate TTL value
        """
        if value < 300 or value > 86400:
            raise serializers.ValidationError("TTL must be between 300 and 86400 seconds")
        return value


class DomainVerificationRequestSerializer(serializers.Serializer):
    """
    Serializer for domain verification requests
    """
    domain_id = serializers.IntegerField()
    verification_method = serializers.ChoiceField(choices=['dns', 'file', 'email'])


class DomainSuggestionSerializer(serializers.Serializer):
    """
    Serializer for domain suggestions
    """
    domain = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField()
