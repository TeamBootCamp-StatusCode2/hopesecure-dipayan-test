from rest_framework import serializers
from .models import Template, TemplateTag, TemplateAttachment


class TemplateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateTag
        fields = ['id', 'name']


class TemplateAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateAttachment
        fields = ['id', 'file', 'filename', 'file_type', 'file_size', 'is_malicious_simulation', 'created_at']


class TemplateSerializer(serializers.ModelSerializer):
    tags = TemplateTagSerializer(many=True, read_only=True)
    attachments = TemplateAttachmentSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    creator_is_admin = serializers.SerializerMethodField()
    
    def get_creator_is_admin(self, obj):
        """Check if the template creator is an admin user"""
        if obj.created_by:
            return obj.created_by.is_staff
        return False  # No creator means system template (considered admin/pre-created)
    
    class Meta:
        model = Template
        fields = [
            'id', 'name', 'category', 'description', 'email_subject', 'sender_name', 
            'sender_email', 'html_content', 'css_styles', 'landing_page_url', 'domain',
            'difficulty', 'risk_level', 'status', 'has_attachments', 'has_css', 
            'is_responsive', 'thumbnail', 'usage_count', 'success_rate', 'rating',
            'tracking_enabled', 'priority', 'created_by', 'created_by_name', 'creator_is_admin',
            'created_at', 'updated_at', 'last_used', 'tags', 'attachments'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'usage_count', 'success_rate']


class TemplateCreateSerializer(serializers.ModelSerializer):
    tag_names = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    
    class Meta:
        model = Template
        fields = [
            'name', 'category', 'description', 'email_subject', 'sender_name', 
            'sender_email', 'html_content', 'css_styles', 'landing_page_url', 'domain',
            'difficulty', 'risk_level', 'status', 'has_attachments', 'has_css', 
            'is_responsive', 'thumbnail', 'tracking_enabled', 'priority', 'tag_names'
        ]
    
    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        template = Template.objects.create(**validated_data)
        
        # Create or get tags and associate with template
        for tag_name in tag_names:
            tag, created = TemplateTag.objects.get_or_create(name=tag_name)
            template.tags.add(tag)
        
        return template


class TemplateListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing templates"""
    tags = serializers.StringRelatedField(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    creator_is_admin = serializers.SerializerMethodField()
    
    def get_creator_is_admin(self, obj):
        """Check if the template creator is an admin user"""
        if obj.created_by:
            return obj.created_by.is_staff
        return False  # No creator means system template (considered admin/pre-created)
    
    class Meta:
        model = Template
        fields = [
            'id', 'name', 'category', 'description', 'email_subject', 'difficulty',
            'risk_level', 'status', 'thumbnail', 'usage_count', 'success_rate', 
            'rating', 'priority', 'created_by', 'created_by_name', 'creator_is_admin', 
            'created_at', 'last_used', 'tags'
        ]


class TemplateStatsSerializer(serializers.Serializer):
    """Serializer for template statistics"""
    total_templates = serializers.IntegerField()
    active_templates = serializers.IntegerField()
    categories = serializers.DictField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    most_used = TemplateListSerializer(read_only=True)
