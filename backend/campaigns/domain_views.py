"""
Domain Management Views
API endpoints for managing email domains
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json

from .domain_models import EmailDomain, DomainDNSRecord, EmailTemplate, DomainVerificationToken
from .domain_serializers import (
    EmailDomainSerializer, EmailDomainCreateSerializer, DomainDNSRecordSerializer,
    EmailTemplateSerializer, DomainVerificationTokenSerializer, DomainAnalyticsSerializer,
    DomainListSerializer, DomainSettingsSerializer, DNSRecordCreateSerializer,
    DomainVerificationRequestSerializer, DomainSuggestionSerializer
)
from .domain_service import DomainDNSManager, get_sendgrid_domain_suggestions, validate_domain_name


class DomainManagementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing email domains
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmailDomain.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmailDomainCreateSerializer
        elif self.action == 'analytics':
            return DomainAnalyticsSerializer
        elif self.action == 'list':
            return DomainListSerializer
        elif self.action == 'update_settings':
            return DomainSettingsSerializer
        return EmailDomainSerializer
    
    def create(self, request):
        """
        Create a new email domain
        """
        serializer = EmailDomainCreateSerializer(data=request.data)
        if serializer.is_valid():
            domain_name = serializer.validated_data['name']
            domain_type = serializer.validated_data.get('domain_type', 'spoofing')
            
            # Use domain service to add domain
            dns_manager = DomainDNSManager()
            success, result = dns_manager.add_domain(
                domain_name=domain_name,
                domain_type=domain_type,
                user=request.user
            )
            
            if success:
                return Response({
                    'success': True,
                    'message': 'Domain added successfully',
                    'data': result
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': result
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """
        List user's domains
        """
        dns_manager = DomainDNSManager()
        domains = dns_manager.list_user_domains(request.user)
        
        serializer = DomainListSerializer(domains, many=True)
        return Response({
            'success': True,
            'domains': serializer.data
        })
    
    def retrieve(self, request, pk=None):
        """
        Get domain details
        """
        domain = get_object_or_404(EmailDomain, id=pk, created_by=request.user)
        serializer = EmailDomainSerializer(domain)
        return Response({
            'success': True,
            'domain': serializer.data
        })
    
    def destroy(self, request, pk=None):
        """
        Delete a domain
        """
        dns_manager = DomainDNSManager()
        success, message = dns_manager.delete_domain(pk, request.user)
        
        if success:
            return Response({
                'success': True,
                'message': message
            })
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify domain DNS records
        """
        dns_manager = DomainDNSManager()
        success, result = dns_manager.verify_domain_dns(pk)
        
        if success:
            return Response({
                'success': True,
                'verification_result': result
            })
        else:
            return Response({
                'success': False,
                'message': result
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """
        Get domain analytics
        """
        dns_manager = DomainDNSManager()
        success, analytics = dns_manager.get_domain_analytics(pk)
        
        if success:
            serializer = DomainAnalyticsSerializer(analytics)
            return Response({
                'success': True,
                'analytics': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': analytics
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['put'])
    def update_settings(self, request, pk=None):
        """
        Update domain settings
        """
        serializer = DomainSettingsSerializer(data=request.data)
        if serializer.is_valid():
            dns_manager = DomainDNSManager()
            success, message = dns_manager.update_domain_settings(
                pk, serializer.validated_data, request.user
            )
            
            if success:
                return Response({
                    'success': True,
                    'message': message
                })
            else:
                return Response({
                    'success': False,
                    'message': message
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def dns_records(self, request, pk=None):
        """
        Get DNS records for domain
        """
        domain = get_object_or_404(EmailDomain, id=pk, created_by=request.user)
        dns_records = DomainDNSRecord.objects.filter(domain=domain)
        
        serializer = DomainDNSRecordSerializer(dns_records, many=True)
        return Response({
            'success': True,
            'dns_records': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def add_dns_record(self, request, pk=None):
        """
        Add DNS record to domain
        """
        domain = get_object_or_404(EmailDomain, id=pk, created_by=request.user)
        
        serializer = DNSRecordCreateSerializer(data=request.data)
        if serializer.is_valid():
            dns_record = serializer.save(domain=domain)
            
            response_serializer = DomainDNSRecordSerializer(dns_record)
            return Response({
                'success': True,
                'message': 'DNS record added successfully',
                'dns_record': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DomainTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing email templates linked to domains
    """
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        domain_id = self.request.query_params.get('domain_id')
        if domain_id:
            return EmailTemplate.objects.filter(
                domain__id=domain_id,
                domain__created_by=self.request.user
            )
        return EmailTemplate.objects.filter(domain__created_by=self.request.user)
    
    def create(self, request):
        """
        Create email template for domain
        """
        domain_id = request.data.get('domain')
        domain = get_object_or_404(EmailDomain, id=domain_id, created_by=request.user)
        
        serializer = EmailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            template = serializer.save()
            return Response({
                'success': True,
                'message': 'Template created successfully',
                'template': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Function-based views for simple operations
@csrf_exempt
@require_http_methods(["GET"])
def domain_suggestions(request):
    """
    Get domain suggestions for phishing campaigns
    """
    suggestions = get_sendgrid_domain_suggestions()
    serializer = DomainSuggestionSerializer(suggestions, many=True)
    
    return JsonResponse({
        'success': True,
        'suggestions': serializer.data
    })


@csrf_exempt
@require_http_methods(["POST"])
def validate_domain(request):
    """
    Validate domain name format
    """
    try:
        data = json.loads(request.body)
        domain_name = data.get('domain_name', '')
        
        # Check format
        is_valid = validate_domain_name(domain_name)
        
        # Check if exists
        exists = EmailDomain.objects.filter(name=domain_name.lower()).exists()
        
        return JsonResponse({
            'success': True,
            'is_valid': is_valid,
            'exists': exists,
            'message': 'Valid domain format' if is_valid else 'Invalid domain format'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def domain_verification_token(request, domain_id):
    """
    Get verification token for domain
    """
    try:
        domain = EmailDomain.objects.get(id=domain_id, created_by=request.user)
        token = DomainVerificationToken.objects.filter(domain=domain, is_used=False).first()
        
        if token:
            serializer = DomainVerificationTokenSerializer(token)
            return JsonResponse({
                'success': True,
                'token': serializer.data
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No active verification token found'
            }, status=404)
            
    except EmailDomain.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Domain not found'
        }, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def bulk_domain_verification(request):
    """
    Verify multiple domains at once
    """
    try:
        data = json.loads(request.body)
        domain_ids = data.get('domain_ids', [])
        
        dns_manager = DomainDNSManager()
        results = []
        
        for domain_id in domain_ids:
            success, result = dns_manager.verify_domain_dns(domain_id)
            results.append({
                'domain_id': domain_id,
                'success': success,
                'result': result
            })
        
        return JsonResponse({
            'success': True,
            'verification_results': results
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
