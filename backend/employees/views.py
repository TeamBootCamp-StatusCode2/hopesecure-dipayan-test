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
    queryset = Employee.objects.all()
    permission_classes = []  # Temporarily allow unauthenticated access for testing
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeCreateSerializer
        return EmployeeListSerializer


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an employee"""
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EmployeeUpdateSerializer
        return EmployeeSerializer


class DepartmentListCreateView(generics.ListCreateAPIView):
    """List all departments or create a new department"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []  # Temporarily allow unauthenticated access for testing


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def employee_stats(request):
    """Get employee statistics"""
    employees = Employee.objects.filter(is_active=True)
    
    stats = {
        'total_employees': employees.count(),
        'active_employees': employees.count(),
        'high_risk_employees': employees.filter(risk_level='high').count(),
        'medium_risk_employees': employees.filter(risk_level='medium').count(),
        'low_risk_employees': employees.filter(risk_level='low').count(),
        'average_susceptibility_score': employees.aggregate(
            avg_score=Avg('phishing_susceptibility_score')
        )['avg_score'] or 0,
        'departments': Department.objects.all(),
        'recent_hires': employees.order_by('-hire_date')[:5]
    }
    
    serializer = EmployeeStatsSerializer(stats)
    return Response(serializer.data, status=status.HTTP_200_OK)
