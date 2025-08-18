from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Campaign, CampaignTarget, CampaignEvent
from .serializers import (
    CampaignSerializer, CampaignCreateSerializer, CampaignListSerializer,
    CampaignStatsSerializer, CampaignUpdateSerializer
)


class CampaignListCreateView(generics.ListCreateAPIView):
    """List all campaigns or create a new campaign"""
    queryset = Campaign.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CampaignCreateSerializer
        return CampaignListSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a campaign"""
    queryset = Campaign.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CampaignUpdateSerializer
        return CampaignSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def campaign_stats(request):
    """Get campaign statistics"""
    campaigns = Campaign.objects.all()
    
    stats = {
        'total_campaigns': campaigns.count(),
        'active_campaigns': campaigns.filter(status='active').count(),
        'completed_campaigns': campaigns.filter(status='completed').count(),
        'total_targets': CampaignTarget.objects.count(),
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
