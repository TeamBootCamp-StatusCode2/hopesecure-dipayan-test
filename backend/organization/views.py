from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer, CompanyUpdateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company_info(request):
    """Get company information for authenticated user"""
    try:
        # Super admin can see all companies
        if request.user.is_super_admin:
            companies = Company.get_all_companies()
            serializer = CompanySerializer(companies, many=True, context={'request': request})
            return Response({
                'is_super_admin': True,
                'companies': serializer.data
            })
        
        # Regular users see their organization
        company = Company.get_user_company(user=request.user)
        serializer = CompanySerializer(company, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to get company information: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_company_info(request):
    """Update company information"""
    try:
        company = Company.get_user_company(user=request.user)
        
        serializer = CompanyUpdateSerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanySerializer(company, context={'request': request})
            return Response(response_serializer.data)
        
        # Log validation errors for debugging
        print(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Exception in update_company_info: {str(e)}")
        return Response(
            {'error': f'Failed to update company information: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_company_logo(request):
    """Upload company logo"""
    try:
        company = Company.get_user_company(user=request.user)
        
        if 'logo' not in request.FILES:
            return Response(
                {'error': 'No logo file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logo_file = request.FILES['logo']
        
        # Validate file size (max 5MB)
        if logo_file.size > 5 * 1024 * 1024:
            return Response(
                {'error': 'File size must be less than 5MB'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        if logo_file.content_type not in allowed_types:
            return Response(
                {'error': 'Only PNG and JPG files are allowed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save the logo
        company.logo = logo_file
        company.save()
        
        serializer = CompanySerializer(company, context={'request': request})
        return Response(serializer.data)
        
    except Exception as e:
        print(f"Exception in upload_company_logo: {str(e)}")
        return Response(
            {'error': f'Failed to upload logo: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_organizations(request):
    """Super admin endpoint to get all organizations"""
    if not request.user.is_super_admin:
        return Response(
            {'error': 'Access denied. Super admin privileges required.'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        companies = Company.objects.all().order_by('-created_at')
        serializer = CompanySerializer(companies, many=True, context={'request': request})
        
        # Add additional stats for each organization
        organizations_data = []
        for company_data in serializer.data:
            company = Company.objects.get(id=company_data['id'])
            org_data = company_data.copy()
            org_data.update({
                'user_count': company.users.count(),
                'admin_email': company.created_by.email if company.created_by else None,
                'employee_count_actual': company.organization_employees.count(),
                'campaign_count': company.campaigns.count() if hasattr(company, 'campaigns') else 0,
                'template_count': company.templates.count() if hasattr(company, 'templates') else 0,
            })
            organizations_data.append(org_data)
        
        return Response({
            'total_organizations': companies.count(),
            'organizations': organizations_data
        })
    except Exception as e:
        return Response(
            {'error': f'Failed to get organizations: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_system_stats(request):
    """Super admin endpoint to get system-wide statistics"""
    if not request.user.is_super_admin:
        return Response(
            {'error': 'Access denied. Super admin privileges required.'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        from django.contrib.auth import get_user_model
        from employees.models import Employee
        from campaigns.models import Campaign
        from templates.models import Template
        
        User = get_user_model()
        
        stats = {
            'total_organizations': Company.objects.count(),
            'total_users': User.objects.count(),
            'total_employees': Employee.objects.count(),
            'total_campaigns': Campaign.objects.count(),
            'total_templates': Template.objects.count(),
            'super_admins': User.objects.filter(role='super_admin').count(),
            'org_admins': User.objects.filter(role='admin').count(),
            'active_organizations': Company.objects.filter(users__isnull=False).distinct().count(),
        }
        
        return Response(stats)
    except Exception as e:
        return Response(
            {'error': f'Failed to get system stats: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
