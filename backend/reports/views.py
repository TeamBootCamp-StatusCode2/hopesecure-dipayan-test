from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Report, CampaignReport, SecurityMetrics


class ReportListCreateView(generics.ListCreateAPIView):
    """List all reports or create a new report"""
    queryset = Report.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a report"""
    queryset = Report.objects.all()
    permission_classes = [permissions.IsAuthenticated]
