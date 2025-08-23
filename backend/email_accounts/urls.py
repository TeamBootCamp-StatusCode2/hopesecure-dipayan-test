"""
Email Accounts URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailAccountViewSet, SendEmailView, EmailDomainQuickSetupView

router = DefaultRouter()
router.register(r'accounts', EmailAccountViewSet, basename='email-accounts')
router.register(r'send', SendEmailView, basename='send-email')
router.register(r'domains', EmailDomainQuickSetupView, basename='email-domains')

urlpatterns = [
    path('', include(router.urls)),
]
