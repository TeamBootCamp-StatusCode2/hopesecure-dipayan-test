from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile
from organization.models import Company


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    # Company/Organization fields
    company_name = serializers.CharField(max_length=200)
    company_domain = serializers.CharField(max_length=100, required=False, allow_blank=True)
    company_industry = serializers.ChoiceField(choices=Company.INDUSTRY_CHOICES, default='technology')
    company_employee_count = serializers.ChoiceField(choices=Company.EMPLOYEE_COUNT_CHOICES, default='1-50')
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'password', 'password_confirm', 
            'role', 'department', 'phone_number',
            'company_name', 'company_domain', 'company_industry', 'company_employee_count'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        # Extract company data
        company_data = {
            'name': validated_data.pop('company_name'),
            'domain': validated_data.pop('company_domain', ''),
            'industry': validated_data.pop('company_industry', 'technology'),
            'employee_count': validated_data.pop('company_employee_count', '1-50'),
        }
        
        # Create user
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Set user as admin for their organization
        validated_data['role'] = 'admin'
        
        user = User.objects.create_user(password=password, **validated_data)
        UserProfile.objects.create(user=user)
        
        # Create company/organization for this user
        company = Company.objects.create(
            name=company_data['name'],
            domain=company_data['domain'],
            industry=company_data['industry'],
            employee_count=company_data['employee_count'],
            created_by=user
        )
        
        # Link user to their organization
        user.organization = company
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            data['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'security_score', 'training_completed', 'notifications_enabled']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name', 'role', 'department', 'phone_number', 'is_email_verified', 'created_at', 'profile']
        read_only_fields = ['id', 'created_at', 'is_email_verified']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'department', 'phone_number']


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid old password')
        return value
