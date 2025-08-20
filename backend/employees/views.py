from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Employee, Department, EmployeeGroup, TrainingRecord
from .serializers import (
    EmployeeSerializer, EmployeeCreateSerializer, EmployeeListSerializer,
    DepartmentSerializer, EmployeeStatsSerializer, EmployeeUpdateSerializer
)


class EmployeeListCreateView(generics.ListCreateAPIView):
    """List all employees or create a new employee"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only show employees created by the current user
        return Employee.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeCreateSerializer
        return EmployeeListSerializer
    
    def perform_create(self, serializer):
        # Set the created_by to the current user
        serializer.save(created_by=self.request.user)


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an employee"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only allow access to employees created by the current user
        return Employee.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EmployeeUpdateSerializer
        return EmployeeSerializer


class DepartmentListCreateView(generics.ListCreateAPIView):
    """List all departments or create a new department"""
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only show departments created by the current user
        return Department.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        # Set the created_by to the current user
        serializer.save(created_by=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def employee_stats(request):
    """Get employee statistics for the current user"""
    employees = Employee.objects.filter(created_by=request.user, is_active=True)
    
    stats = {
        'total_employees': employees.count(),
        'active_employees': employees.count(),
        'high_risk_employees': employees.filter(risk_level='high').count(),
        'medium_risk_employees': employees.filter(risk_level='medium').count(),
        'low_risk_employees': employees.filter(risk_level='low').count(),
        'average_susceptibility_score': employees.aggregate(
            avg_score=Avg('phishing_susceptibility_score')
        )['avg_score'] or 0,
        'departments': Department.objects.filter(created_by=request.user),
        'recent_hires': employees.order_by('-hire_date')[:5]
    }
    
    serializer = EmployeeStatsSerializer(stats)
    return Response(serializer.data, status=status.HTTP_200_OK)
