from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'domain', 'industry', 'employee_count',
            'address', 'phone', 'website', 'registration_number',
            'founded_year', 'timezone', 'language', 'logo',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_logo(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'name', 'domain', 'industry', 'employee_count',
            'address', 'phone', 'website', 'registration_number',
            'founded_year', 'timezone', 'language'
        ]
