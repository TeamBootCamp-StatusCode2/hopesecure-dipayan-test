from django.urls import path
from . import views

urlpatterns = [
    # Campaign URLs will be added here
    path('', views.CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('stats/', views.campaign_stats, name='campaign-stats'),
]
