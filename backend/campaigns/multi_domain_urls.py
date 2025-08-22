"""
Multi-Domain Campaign URLs
Multiple domain দিয়ে phishing campaigns এর জন্য API endpoints
"""

from django.urls import path
from . import multi_domain_views

urlpatterns = [
    # Multi-domain campaign endpoints
    path('multi-domain/create/', multi_domain_views.create_multi_domain_campaign, name='create_multi_domain_campaign'),
    path('multi-domain/domains/', multi_domain_views.get_available_domains, name='get_available_domains'),
    path('multi-domain/test-email/', multi_domain_views.test_domain_email, name='test_domain_email'),
    path('multi-domain/statistics/', multi_domain_views.get_domain_statistics, name='get_domain_statistics'),
    path('multi-domain/add-domain/', multi_domain_views.add_new_domain, name='add_new_domain'),
]
