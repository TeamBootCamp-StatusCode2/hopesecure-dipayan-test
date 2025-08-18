from rest_framework import serializers
from .models import Department, Employee, EmployeeGroup, TrainingRecord


class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'manager', 'manager_name', 'employee_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.ReadOnlyField()
    click_rate = serializers.ReadOnlyField()
    submission_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'first_name', 'last_name', 'full_name', 'email',
            'department', 'department_name', 'position', 'manager_email', 'phone_number',
            'office_location', 'hire_date', 'is_active', 'security_clearance_level',
            'has_admin_access', 'risk_level', 'last_security_training',
            'phishing_susceptibility_score', 'total_campaigns_received',
            'total_campaigns_clicked', 'total_campaigns_submitted', 'last_campaign_date',
            'click_rate', 'submission_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'total_campaigns_received',
            'total_campaigns_clicked', 'total_campaigns_submitted', 'last_campaign_date'
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'email', 'department',
            'position', 'manager_email', 'phone_number', 'office_location',
            'hire_date', 'security_clearance_level', 'has_admin_access', 'risk_level'
        ]


class EmployeeListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing employees"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.ReadOnlyField()
    click_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'full_name', 'email', 'department_name',
            'position', 'risk_level', 'phishing_susceptibility_score',
            'total_campaigns_received', 'click_rate', 'is_active'
        ]


class EmployeeGroupSerializer(serializers.ModelSerializer):
    employees = EmployeeListSerializer(many=True, read_only=True)
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = EmployeeGroup
        fields = [
            'id', 'name', 'description', 'employees', 'employee_count',
            'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class EmployeeGroupCreateSerializer(serializers.ModelSerializer):
    employee_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = EmployeeGroup
        fields = ['name', 'description', 'employee_ids']
    
    def create(self, validated_data):
        employee_ids = validated_data.pop('employee_ids', [])
        group = EmployeeGroup.objects.create(**validated_data)
        
        if employee_ids:
            employees = Employee.objects.filter(id__in=employee_ids)
            group.employees.set(employees)
        
        return group


class TrainingRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    
    class Meta:
        model = TrainingRecord
        fields = [
            'id', 'employee', 'employee_name', 'training_type', 'training_name',
            'status', 'scheduled_date', 'completion_date', 'score',
            'duration_minutes', 'trainer', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EmployeeStatsSerializer(serializers.Serializer):
    """Serializer for employee statistics"""
    total_employees = serializers.IntegerField()
    active_employees = serializers.IntegerField()
    high_risk_employees = serializers.IntegerField()
    medium_risk_employees = serializers.IntegerField()
    low_risk_employees = serializers.IntegerField()
    average_susceptibility_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    departments = DepartmentSerializer(many=True, read_only=True)
    recent_hires = EmployeeListSerializer(many=True, read_only=True)


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'department', 'position',
            'manager_email', 'phone_number', 'office_location', 'is_active',
            'security_clearance_level', 'has_admin_access', 'risk_level',
            'phishing_susceptibility_score'
        ]
