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
        company = Company.get_instance(user=request.user)
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
        company = Company.get_instance(user=request.user)
        
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
        company = Company.get_instance(user=request.user)
        
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
