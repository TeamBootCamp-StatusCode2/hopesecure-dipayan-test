from django.urls import path
from . import views

urlpatterns = [
    # Campaign URLs will be added here
    path('', views.CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('stats/', views.campaign_stats, name='campaign-stats'),
    
    # Real-time campaign control endpoints
    path('<int:campaign_id>/start/', views.start_campaign, name='campaign-start'),
    path('<int:campaign_id>/pause/', views.pause_campaign, name='campaign-pause'),
    path('<int:campaign_id>/stop/', views.stop_campaign, name='campaign-stop'),
    path('<int:campaign_id>/live-stats/', views.campaign_live_stats, name='campaign-live-stats'),
]
