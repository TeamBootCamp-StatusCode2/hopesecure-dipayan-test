from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'industry', 'employee_count', 'created_at']
    list_filter = ['industry', 'employee_count', 'created_at']
    search_fields = ['name', 'domain']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'domain', 'industry', 'employee_count')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'website')
        }),
        ('Registration Information', {
            'fields': ('registration_number', 'founded_year')
        }),
        ('Settings', {
            'fields': ('timezone', 'language', 'logo')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
