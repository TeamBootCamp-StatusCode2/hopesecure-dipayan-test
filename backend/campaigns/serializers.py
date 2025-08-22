from rest_framework import serializers
from .models import Campaign, CampaignTarget, CampaignEvent
from templates.serializers import TemplateListSerializer


class CampaignTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTarget
        fields = [
            'id', 'email', 'first_name', 'last_name', 'department', 'status',
            'email_sent_at', 'email_opened_at', 'link_clicked_at', 'data_submitted_at',
            'attachment_downloaded_at', 'user_agent', 'ip_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CampaignEventSerializer(serializers.ModelSerializer):
    target_email = serializers.CharField(source='target.email', read_only=True)
    
    class Meta:
        model = CampaignEvent
        fields = [
            'id', 'event_type', 'timestamp', 'ip_address', 'user_agent',
            'additional_data', 'target_email'
        ]
        read_only_fields = ['id', 'timestamp']


class CampaignSerializer(serializers.ModelSerializer):
    template = TemplateListSerializer(read_only=True)
    targets = CampaignTargetSerializer(many=True, read_only=True)
    events = CampaignEventSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    success_rate = serializers.ReadOnlyField()
    open_rate = serializers.ReadOnlyField()
    click_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'description', 'campaign_type', 'template', 'status',
            'target_count', 'emails_sent', 'emails_opened', 'links_clicked',
            'credentials_submitted', 'data_submitted', 'attachments_downloaded',
            'scheduled_start', 'scheduled_end', 'actual_start', 'actual_end',
            'send_reminder', 'reminder_delay_hours', 'track_clicks', 'track_downloads',
            'capture_credentials', 'redirect_url', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'success_rate', 'open_rate', 'click_rate',
            'targets', 'events'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at', 'target_count',
            'emails_sent', 'emails_opened', 'links_clicked', 'credentials_submitted',
            'data_submitted', 'attachments_downloaded', 'actual_start', 'actual_end'
        ]


class CampaignCreateSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField(write_only=True)
    domain_id = serializers.IntegerField(write_only=True, required=False)  # Add domain_id field
    target_emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Campaign
        fields = [
            'name', 'description', 'campaign_type', 'template_id', 'domain_id', 'status',
            'scheduled_start', 'scheduled_end', 'send_reminder', 'reminder_delay_hours',
            'track_clicks', 'track_downloads', 'capture_credentials', 'redirect_url',
            'target_emails'
        ]
    
    def create(self, validated_data):
        from templates.models import Template
        from .domain_models import EmailDomain
        
        template_id = validated_data.pop('template_id')
        domain_id = validated_data.pop('domain_id', None)
        target_emails = validated_data.pop('target_emails', [])
        
        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            raise serializers.ValidationError({'template_id': 'Template not found'})
        
        # Get domain if provided
        domain = None
        if domain_id:
            try:
                domain = EmailDomain.objects.get(id=domain_id)
            except EmailDomain.DoesNotExist:
                raise serializers.ValidationError({'domain_id': 'Domain not found'})
        
        campaign = Campaign.objects.create(template=template, domain=domain, **validated_data)
        
        # Create campaign targets
        for email in target_emails:
            CampaignTarget.objects.create(campaign=campaign, email=email)
        
        campaign.target_count = len(target_emails)
        campaign.save()
        
        return campaign


class CampaignListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing campaigns"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    success_rate = serializers.ReadOnlyField()
    open_rate = serializers.ReadOnlyField()
    click_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'campaign_type', 'template_name', 'status', 'target_count',
            'emails_sent', 'emails_opened', 'links_clicked', 'credentials_submitted',
            'scheduled_start', 'actual_start', 'created_by_name', 'created_at',
            'success_rate', 'open_rate', 'click_rate'
        ]


class CampaignStatsSerializer(serializers.Serializer):
    """Serializer for campaign statistics"""
    total_campaigns = serializers.IntegerField()
    active_campaigns = serializers.IntegerField()
    completed_campaigns = serializers.IntegerField()
    total_targets = serializers.IntegerField()
    total_emails_sent = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_submissions = serializers.IntegerField()
    average_success_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    recent_campaigns = CampaignListSerializer(many=True, read_only=True)


class CampaignUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            'name', 'description', 'status', 'scheduled_start', 'scheduled_end',
            'send_reminder', 'reminder_delay_hours', 'redirect_url'
        ]
