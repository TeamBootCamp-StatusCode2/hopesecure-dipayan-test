from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Campaign, CampaignEvent
from authentication.models import ActivityLog, SystemAlert


@receiver(post_save, sender=Campaign)
def campaign_updated(sender, instance, created, **kwargs):
    """Broadcast campaign updates to WebSocket clients"""
    channel_layer = get_channel_layer()
    campaign_group_name = f'campaign_{instance.id}'
    
    # Campaign data for real-time update
    campaign_data = {
        'id': instance.id,
        'name': instance.name,
        'status': instance.status,
        'target_count': instance.target_count,
        'emails_sent': instance.emails_sent,
        'emails_opened': instance.emails_opened,
        'links_clicked': instance.links_clicked,
        'credentials_submitted': instance.credentials_submitted,
        'data_submitted': instance.data_submitted,
        'attachments_downloaded': instance.attachments_downloaded,
        'success_rate': instance.success_rate,
        'open_rate': instance.open_rate,
        'click_rate': instance.click_rate,
        'updated_at': instance.updated_at.isoformat(),
    }
    
    # Broadcast to campaign-specific group
    async_to_sync(channel_layer.group_send)(
        campaign_group_name,
        {
            'type': 'campaign_update',
            'data': campaign_data
        }
    )
    
    # Also broadcast to dashboard group for campaign creator
    dashboard_group_name = f'dashboard_{instance.created_by.id}'
    async_to_sync(channel_layer.group_send)(
        dashboard_group_name,
        {
            'type': 'dashboard_update',
            'data': {
                'campaign_id': instance.id,
                'campaign_name': instance.name,
                'action': 'created' if created else 'updated',
                'stats': campaign_data
            }
        }
    )


@receiver(post_save, sender=CampaignEvent)
def campaign_event_created(sender, instance, created, **kwargs):
    """Broadcast new campaign events to WebSocket clients"""
    if not created:
        return
        
    channel_layer = get_channel_layer()
    campaign_group_name = f'campaign_{instance.campaign.id}'
    
    event_data = {
        'id': instance.id,
        'event_type': instance.event_type,
        'target_email': instance.target_email,
        'user_agent': instance.user_agent,
        'ip_address': instance.ip_address,
        'created_at': instance.created_at.isoformat(),
        'campaign_id': instance.campaign.id,
    }
    
    # Broadcast to campaign-specific group
    async_to_sync(channel_layer.group_send)(
        campaign_group_name,
        {
            'type': 'campaign_event',
            'data': event_data
        }
    )


@receiver(post_save, sender=SystemAlert)
def system_alert_created(sender, instance, created, **kwargs):
    """Broadcast new system alerts to admin monitoring clients"""
    if not created:
        return
        
    channel_layer = get_channel_layer()
    admin_group_name = 'admin_monitoring'
    
    alert_data = {
        'id': instance.id,
        'alert_type': instance.alert_type,
        'message': instance.message,
        'severity': instance.severity,
        'created_at': instance.created_at.isoformat(),
        'is_resolved': instance.is_resolved,
    }
    
    # Broadcast to admin monitoring group
    async_to_sync(channel_layer.group_send)(
        admin_group_name,
        {
            'type': 'admin_alert',
            'data': alert_data
        }
    )


@receiver(post_save, sender=ActivityLog)
def activity_log_created(sender, instance, created, **kwargs):
    """Broadcast new activity logs to admin monitoring clients"""
    if not created:
        return
        
    channel_layer = get_channel_layer()
    admin_group_name = 'admin_monitoring'
    
    log_data = {
        'id': instance.id,
        'user_email': instance.user.email if instance.user else 'System',
        'action': instance.action,
        'model_name': instance.model_name,
        'object_id': instance.object_id,
        'timestamp': instance.timestamp.isoformat(),
        'ip_address': instance.ip_address,
    }
    
    # Broadcast to admin monitoring group
    async_to_sync(channel_layer.group_send)(
        admin_group_name,
        {
            'type': 'system_update',
            'data': {
                'type': 'activity_log',
                'log': log_data
            }
        }
    )
