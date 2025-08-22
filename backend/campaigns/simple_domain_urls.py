"""
Simple Domain URLs
Basic URL patterns for domain API
"""

from django.urls import path
from . import simple_domain_api

urlpatterns = [
    # Simple domain API endpoints
    path('api/domains/', simple_domain_api.simple_domain_api, name='simple-domain-api'),
    path('api/domains/<int:domain_id>/verify/', simple_domain_api.simple_domain_verify, name='simple-domain-verify'),
    path('api/domains/<int:domain_id>/dns_records/', simple_domain_api.simple_domain_dns_records, name='simple-domain-dns-records'),
    path('api/domains/<int:domain_id>/', simple_domain_api.simple_domain_delete, name='simple-domain-delete'),
    path('api/domain-suggestions/', simple_domain_api.simple_domain_suggestions, name='simple-domain-suggestions'),
    path('api/validate-domain/', simple_domain_api.simple_validate_domain, name='simple-validate-domain'),
]
