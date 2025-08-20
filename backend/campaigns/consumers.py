import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .models import Campaign, CampaignEvent
from authentication.models import ActivityLog, SystemAlert

User = get_user_model()


class CampaignConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time campaign monitoring"""
    
    async def connect(self):
        self.campaign_id = self.scope['url_route']['kwargs']['campaign_id']
        self.campaign_group_name = f'campaign_{self.campaign_id}'
        
        # Authenticate user
        user = await self.get_user_from_token()
        if user is None or user.is_anonymous:
            await self.close(code=4001)
            return
            
        self.user = user
        
        # Join campaign group
        await self.channel_layer.group_add(
            self.campaign_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial campaign data
        campaign_data = await self.get_campaign_data()
        await self.send(text_data=json.dumps({
            'type': 'campaign_data',
            'data': campaign_data
        }))
    
    async def disconnect(self, close_code):
        # Leave campaign group
        await self.channel_layer.group_discard(
            self.campaign_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'get_campaign_stats':
            campaign_data = await self.get_campaign_data()
            await self.send(text_data=json.dumps({
                'type': 'campaign_stats',
                'data': campaign_data
            }))
    
    # Receive message from campaign group
    async def campaign_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'campaign_update',
            'data': event['data']
        }))
    
    async def campaign_event(self, event):
        await self.send(text_data=json.dumps({
            'type': 'campaign_event',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_user_from_token(self):
        """Authenticate user from token in query string"""
        try:
            query_string = self.scope.get('query_string', b'').decode()
            if 'token=' in query_string:
                token_key = query_string.split('token=')[1].split('&')[0]
                token = Token.objects.get(key=token_key)
                return token.user
        except (Token.DoesNotExist, IndexError):
            pass
        return AnonymousUser()
    
    @database_sync_to_async
    def get_campaign_data(self):
        """Get current campaign statistics"""
        try:
            campaign = Campaign.objects.get(id=self.campaign_id)
            return {
                'id': campaign.id,
                'name': campaign.name,
                'status': campaign.status,
                'target_count': campaign.target_count,
                'emails_sent': campaign.emails_sent,
                'emails_opened': campaign.emails_opened,
                'links_clicked': campaign.links_clicked,
                'credentials_submitted': campaign.credentials_submitted,
                'data_submitted': campaign.data_submitted,
                'attachments_downloaded': campaign.attachments_downloaded,
                'success_rate': campaign.success_rate,
                'open_rate': campaign.open_rate,
                'click_rate': campaign.click_rate,
                'updated_at': campaign.updated_at.isoformat(),
            }
        except Campaign.DoesNotExist:
            return None


class DashboardConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time dashboard updates"""
    
    async def connect(self):
        # Authenticate user
        user = await self.get_user_from_token()
        if user is None or user.is_anonymous:
            await self.close(code=4001)
            return
            
        self.user = user
        self.dashboard_group_name = f'dashboard_{user.id}'
        
        # Join dashboard group
        await self.channel_layer.group_add(
            self.dashboard_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial dashboard data
        dashboard_data = await self.get_dashboard_data()
        await self.send(text_data=json.dumps({
            'type': 'dashboard_data',
            'data': dashboard_data
        }))
    
    async def disconnect(self, close_code):
        # Leave dashboard group
        await self.channel_layer.group_discard(
            self.dashboard_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'get_dashboard_stats':
            dashboard_data = await self.get_dashboard_data()
            await self.send(text_data=json.dumps({
                'type': 'dashboard_stats',
                'data': dashboard_data
            }))
    
    # Receive message from dashboard group
    async def dashboard_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'dashboard_update',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_user_from_token(self):
        """Authenticate user from token in query string"""
        try:
            query_string = self.scope.get('query_string', b'').decode()
            if 'token=' in query_string:
                token_key = query_string.split('token=')[1].split('&')[0]
                token = Token.objects.get(key=token_key)
                return token.user
        except (Token.DoesNotExist, IndexError):
            pass
        return AnonymousUser()
    
    @database_sync_to_async
    def get_dashboard_data(self):
        """Get current dashboard statistics for user"""
        try:
            # Get user's campaigns
            campaigns = Campaign.objects.filter(created_by=self.user)
            
            total_campaigns = campaigns.count()
            active_campaigns = campaigns.filter(status='active').count()
            total_emails_sent = sum(c.emails_sent for c in campaigns)
            total_emails_opened = sum(c.emails_opened for c in campaigns)
            
            return {
                'total_campaigns': total_campaigns,
                'active_campaigns': active_campaigns,
                'total_emails_sent': total_emails_sent,
                'total_emails_opened': total_emails_opened,
                'avg_open_rate': (total_emails_opened / total_emails_sent * 100) if total_emails_sent > 0 else 0,
                'updated_at': timezone.now().isoformat(),
            }
        except Exception as e:
            return {'error': str(e)}


class AdminMonitoringConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for admin monitoring and alerts"""
    
    async def connect(self):
        # Authenticate user
        user = await self.get_user_from_token()
        if user is None or user.is_anonymous or not user.is_staff:
            await self.close(code=4001)
            return
            
        self.user = user
        self.admin_group_name = 'admin_monitoring'
        
        # Join admin group
        await self.channel_layer.group_add(
            self.admin_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial admin data
        admin_data = await self.get_admin_data()
        await self.send(text_data=json.dumps({
            'type': 'admin_data',
            'data': admin_data
        }))
    
    async def disconnect(self, close_code):
        # Leave admin group
        await self.channel_layer.group_discard(
            self.admin_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'get_system_stats':
            admin_data = await self.get_admin_data()
            await self.send(text_data=json.dumps({
                'type': 'system_stats',
                'data': admin_data
            }))
    
    # Receive message from admin group
    async def admin_alert(self, event):
        await self.send(text_data=json.dumps({
            'type': 'admin_alert',
            'data': event['data']
        }))
    
    async def system_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'system_update',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_user_from_token(self):
        """Authenticate user from token in query string"""
        try:
            query_string = self.scope.get('query_string', b'').decode()
            if 'token=' in query_string:
                token_key = query_string.split('token=')[1].split('&')[0]
                token = Token.objects.get(key=token_key)
                return token.user
        except (Token.DoesNotExist, IndexError):
            pass
        return AnonymousUser()
    
    @database_sync_to_async
    def get_admin_data(self):
        """Get current admin/system statistics"""
        try:
            from datetime import timedelta
            
            # System overview stats
            total_users = User.objects.count()
            active_users = User.objects.filter(last_login__gte=timezone.now() - timedelta(days=7)).count()
            total_campaigns = Campaign.objects.count()
            active_campaigns = Campaign.objects.filter(status='active').count()
            
            # Recent alerts
            recent_alerts = SystemAlert.objects.filter(
                created_at__gte=timezone.now() - timedelta(hours=24)
            ).count()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_campaigns': total_campaigns,
                'active_campaigns': active_campaigns,
                'recent_alerts': recent_alerts,
                'updated_at': timezone.now().isoformat(),
            }
        except Exception as e:
            return {'error': str(e)}
