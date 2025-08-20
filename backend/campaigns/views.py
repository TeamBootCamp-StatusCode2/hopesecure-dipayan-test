from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.utils import timezone
from .models import Campaign, CampaignTarget, CampaignEvent
from .serializers import (
    CampaignSerializer, CampaignCreateSerializer, CampaignListSerializer,
    CampaignStatsSerializer, CampaignUpdateSerializer
)


class CampaignListCreateView(generics.ListCreateAPIView):
    """List all campaigns or create a new campaign"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only show campaigns created by the current user
        return Campaign.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CampaignCreateSerializer
        return CampaignListSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a campaign"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only allow access to campaigns created by the current user
        return Campaign.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CampaignUpdateSerializer
        return CampaignSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def campaign_stats(request):
    """Get campaign statistics for the current user"""
    campaigns = Campaign.objects.filter(created_by=request.user)
    
    stats = {
        'total_campaigns': campaigns.count(),
        'active_campaigns': campaigns.filter(status='active').count(),
        'completed_campaigns': campaigns.filter(status='completed').count(),
        'total_targets': CampaignTarget.objects.filter(campaign__created_by=request.user).count(),
        'total_emails_sent': sum(campaigns.values_list('emails_sent', flat=True)),
        'total_clicks': sum(campaigns.values_list('links_clicked', flat=True)),
        'total_submissions': sum(campaigns.values_list('credentials_submitted', flat=True)),
        'average_success_rate': campaigns.exclude(emails_sent=0).aggregate(
            avg_rate=Avg('credentials_submitted') / Avg('emails_sent') * 100
        )['avg_rate'] or 0,
        'recent_campaigns': campaigns.order_by('-created_at')[:5]
    }
    
    serializer = CampaignStatsSerializer(stats)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_campaign(request, campaign_id):
    """Start a campaign"""
    try:
        campaign = Campaign.objects.get(id=campaign_id, created_by=request.user)
        
        if campaign.status == 'active':
            return Response({'error': 'Campaign is already active'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update campaign status
        campaign.status = 'active'
        campaign.actual_start = timezone.now()
        campaign.save()
        
        return Response({
            'message': 'Campaign started successfully',
            'campaign': {
                'id': campaign.id,
                'status': campaign.status,
                'actual_start': campaign.actual_start.isoformat()
            }
        }, status=status.HTTP_200_OK)
        
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def pause_campaign(request, campaign_id):
    """Pause a campaign"""
    try:
        campaign = Campaign.objects.get(id=campaign_id, created_by=request.user)
        
        if campaign.status != 'active':
            return Response({'error': 'Campaign is not active'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update campaign status
        campaign.status = 'paused'
        campaign.save()
        
        return Response({
            'message': 'Campaign paused successfully',
            'campaign': {
                'id': campaign.id,
                'status': campaign.status
            }
        }, status=status.HTTP_200_OK)
        
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def stop_campaign(request, campaign_id):
    """Stop a campaign"""
    try:
        campaign = Campaign.objects.get(id=campaign_id, created_by=request.user)
        
        if campaign.status in ['completed', 'stopped']:
            return Response({'error': 'Campaign is already stopped'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update campaign status
        campaign.status = 'stopped'
        campaign.actual_end = timezone.now()
        campaign.save()
        
        return Response({
            'message': 'Campaign stopped successfully',
            'campaign': {
                'id': campaign.id,
                'status': campaign.status,
                'actual_end': campaign.actual_end.isoformat()
            }
        }, status=status.HTTP_200_OK)
        
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def campaign_live_stats(request, campaign_id):
    """Get live campaign statistics for real-time updates"""
    try:
        campaign = Campaign.objects.get(id=campaign_id, created_by=request.user)
        
        # Get latest events
        recent_events = CampaignEvent.objects.filter(
            campaign=campaign
        ).order_by('-created_at')[:10]
        
        live_stats = {
            'campaign_id': campaign.id,
            'status': campaign.status,
            'emails_sent': campaign.emails_sent,
            'emails_opened': campaign.emails_opened,
            'links_clicked': campaign.links_clicked,
            'credentials_submitted': campaign.credentials_submitted,
            'data_submitted': campaign.data_submitted,
            'attachments_downloaded': campaign.attachments_downloaded,
            'success_rate': campaign.success_rate,
            'open_rate': campaign.open_rate,
            'click_rate': campaign.click_rate,
            'recent_events': [
                {
                    'event_type': event.event_type,
                    'target_email': event.target_email,
                    'created_at': event.created_at.isoformat(),
                }
                for event in recent_events
            ],
            'last_updated': timezone.now().isoformat(),
        }
        
        return Response(live_stats, status=status.HTTP_200_OK)
        
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
