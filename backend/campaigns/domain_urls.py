"""
Domain Management URLs
URL patterns for domain API endpoints
"""

from django.urls import path, include
try:
    from rest_framework.routers import DefaultRouter
    from . import domain_views
    
    # Create router for ViewSets
    router = DefaultRouter()
    router.register(r'domains', domain_views.DomainManagementViewSet, basename='domain')
    router.register(r'domain-templates', domain_views.DomainTemplateViewSet, basename='domain-template')
    
    urlpatterns = [
        # ViewSet URLs
        path('api/', include(router.urls)),
        
        # Function-based view URLs
        path('api/domain-suggestions/', domain_views.domain_suggestions, name='domain-suggestions'),
        path('api/validate-domain/', domain_views.validate_domain, name='validate-domain'),
        path('api/domain-verification-token/<int:domain_id>/', domain_views.domain_verification_token, name='domain-verification-token'),
        path('api/bulk-domain-verification/', domain_views.bulk_domain_verification, name='bulk-domain-verification'),
    ]
except ImportError:
    # Fallback URLs if REST framework not available
    from . import domain_views
    
    urlpatterns = [
        # Function-based view URLs only
        path('api/domain-suggestions/', domain_views.domain_suggestions, name='domain-suggestions'),
        path('api/validate-domain/', domain_views.validate_domain, name='validate-domain'),
        path('api/domain-verification-token/<int:domain_id>/', domain_views.domain_verification_token, name='domain-verification-token'),
        path('api/bulk-domain-verification/', domain_views.bulk_domain_verification, name='bulk-domain-verification'),
    ]

"""
Available API Endpoints:

Domain Management:
- GET /api/domains/ - List user's domains
- POST /api/domains/ - Create new domain
- GET /api/domains/{id}/ - Get domain details
- PUT /api/domains/{id}/ - Update domain
- DELETE /api/domains/{id}/ - Delete domain
- POST /api/domains/{id}/verify/ - Verify domain DNS
- GET /api/domains/{id}/analytics/ - Get domain analytics
- PUT /api/domains/{id}/update_settings/ - Update domain settings
- GET /api/domains/{id}/dns_records/ - Get DNS records
- POST /api/domains/{id}/add_dns_record/ - Add DNS record

Domain Templates:
- GET /api/domain-templates/ - List templates (filter by domain_id)
- POST /api/domain-templates/ - Create template
- GET /api/domain-templates/{id}/ - Get template details
- PUT /api/domain-templates/{id}/ - Update template
- DELETE /api/domain-templates/{id}/ - Delete template

Utility Endpoints:
- GET /api/domain-suggestions/ - Get suggested domains
- POST /api/validate-domain/ - Validate domain format
- GET /api/domain-verification-token/{domain_id}/ - Get verification token
- POST /api/bulk-domain-verification/ - Verify multiple domains

Example Usage:

1. Create Domain:
POST /api/domains/
{
    "name": "secure-alerts.com",
    "domain_type": "spoofing",
    "verification_method": "dns"
}

2. Verify Domain:
POST /api/domains/1/verify/

3. Add DNS Record:
POST /api/domains/1/add_dns_record/
{
    "record_type": "TXT",
    "name": "_dmarc",
    "value": "v=DMARC1; p=quarantine;",
    "ttl": 3600
}

4. Get Domain Analytics:
GET /api/domains/1/analytics/

5. Update Settings:
PUT /api/domains/1/update_settings/
{
    "max_emails_per_day": 1000,
    "click_tracking_enabled": true
}
"""
