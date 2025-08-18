from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count
from .models import Template, TemplateTag, TemplateAttachment
from .serializers import (
    TemplateSerializer, TemplateCreateSerializer, TemplateListSerializer,
    TemplateStatsSerializer, TemplateTagSerializer, TemplateAttachmentSerializer
)


class TemplateListCreateView(generics.ListCreateAPIView):
    """List all templates or create a new template"""
    queryset = Template.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TemplateCreateSerializer
        return TemplateListSerializer
    
    def get_queryset(self):
        queryset = Template.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by risk level
        risk_level = self.request.query_params.get('risk_level')
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
        
        # Search by name or description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        # Order by usage count or rating
        order_by = self.request.query_params.get('order_by', '-created_at')
        if order_by in ['usage_count', '-usage_count', 'rating', '-rating', 'created_at', '-created_at']:
            queryset = queryset.order_by(order_by)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a template"""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def template_stats(request):
    """Get template statistics"""
    templates = Template.objects.all()
    
    stats = {
        'total_templates': templates.count(),
        'active_templates': templates.filter(status='active').count(),
        'categories': dict(templates.values('category').annotate(count=Count('category')).values_list('category', 'count')),
        'average_rating': templates.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
        'most_used': templates.order_by('-usage_count').first()
    }
    
    serializer = TemplateStatsSerializer(stats)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def template_categories(request):
    """Get all template categories"""
    categories = Template.CATEGORY_CHOICES
    return Response([{'value': choice[0], 'label': choice[1]} for choice in categories])


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def template_by_category(request):
    """Get templates grouped by category"""
    categories = {}
    for category_key, category_label in Template.CATEGORY_CHOICES:
        templates = Template.objects.filter(category=category_key, status='active')
        categories[category_key] = {
            'label': category_label,
            'count': templates.count(),
            'templates': TemplateListSerializer(templates[:5], many=True).data  # Top 5 per category
        }
    
    return Response(categories, status=status.HTTP_200_OK)


class TemplateTagListView(generics.ListCreateAPIView):
    """List all template tags or create a new tag"""
    queryset = TemplateTag.objects.all()
    serializer_class = TemplateTagSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def clone_template(request, pk):
    """Clone an existing template"""
    try:
        original_template = Template.objects.get(pk=pk)
    except Template.DoesNotExist:
        return Response({'error': 'Template not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Create a copy with modified name
    cloned_template = Template.objects.create(
        name=f"{original_template.name} (Copy)",
        category=original_template.category,
        description=original_template.description,
        email_subject=original_template.email_subject,
        sender_name=original_template.sender_name,
        sender_email=original_template.sender_email,
        html_content=original_template.html_content,
        css_styles=original_template.css_styles,
        landing_page_url=original_template.landing_page_url,
        domain=original_template.domain,
        difficulty=original_template.difficulty,
        risk_level=original_template.risk_level,
        status='draft',  # New cloned templates start as draft
        has_attachments=original_template.has_attachments,
        has_css=original_template.has_css,
        is_responsive=original_template.is_responsive,
        tracking_enabled=original_template.tracking_enabled,
        priority=original_template.priority,
        created_by=request.user
    )
    
    # Copy tags
    cloned_template.tags.set(original_template.tags.all())
    
    serializer = TemplateSerializer(cloned_template)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def preview_template(request, pk):
    """Generate a preview of the template"""
    try:
        template = Template.objects.get(pk=pk)
    except Template.DoesNotExist:
        return Response({'error': 'Template not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Return the HTML content for preview
    preview_data = {
        'html_content': template.html_content,
        'css_styles': template.css_styles,
        'email_subject': template.email_subject,
        'sender_name': template.sender_name,
        'sender_email': template.sender_email
    }
    
    return Response(preview_data, status=status.HTTP_200_OK)
