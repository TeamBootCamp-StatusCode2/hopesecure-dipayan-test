from django.urls import path, include
from . import views
from . import campaign_domain_api
from . import simple_domain_test
from . import campaign_launch_service
from . import sendgrid_views

urlpatterns = [
    # Campaign URLs
    path('', views.CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('stats/', views.campaign_stats, name='campaign-stats'),
    path('global-stats/', views.global_platform_stats, name='global-platform-stats'),
    
    # Campaign Launch APIs
    path('launch/', campaign_launch_service.launch_campaign, name='launch-campaign'),
    path('validate/', campaign_launch_service.validate_campaign_setup, name='validate-campaign'),
    
    # Domain APIs for campaigns
    path('available-domains/', campaign_domain_api.get_available_domains, name='available-domains'),
    path('test-domains/', simple_domain_test.test_domains_api, name='test-domains'),
    path('test-custom-email/', simple_domain_test.test_custom_email, name='test-custom-email'),
    path('generate-email/', campaign_domain_api.generate_custom_email, name='generate-custom-email'),
    
    # Real-time campaign control endpoints
    path('<int:campaign_id>/start/', views.start_campaign, name='campaign-start'),
    path('<int:campaign_id>/pause/', views.pause_campaign, name='campaign-pause'),
    path('<int:campaign_id>/stop/', views.stop_campaign, name='campaign-stop'),
    path('<int:campaign_id>/live-stats/', views.campaign_live_stats, name='campaign-live-stats'),
    
    # Email configuration endpoints
    path('email-configs/', views.get_email_configurations, name='email-configurations'),
    path('test-spoofing/', views.test_email_spoofing, name='test-email-spoofing'),
    path('verify-setup/', views.verify_email_setup, name='verify-email-setup'),
    path('send-test-email/', views.send_test_email, name='send-test-email'),
    
    # SendGrid Verification APIs
    path('sendgrid/senders/', sendgrid_views.get_verified_senders, name='sendgrid-verified-senders'),
    path('sendgrid/senders/create/', sendgrid_views.create_verified_sender, name='sendgrid-create-sender'),
    path('sendgrid/senders/resend/', sendgrid_views.resend_verification, name='sendgrid-resend-verification'),
    path('sendgrid/senders/<int:sender_id>/delete/', sendgrid_views.delete_verified_sender, name='sendgrid-delete-sender'),
    path('sendgrid/status/', sendgrid_views.check_verification_status, name='sendgrid-verification-status'),
    
    # Domain management endpoints - Simple API
    path('domains/', include('campaigns.simple_domain_urls')),
    
    # Multi-domain campaign endpoints
    path('', include('campaigns.multi_domain_urls')),
]
