from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.get_company_info, name='get_company_info'),
    path('company/update/', views.update_company_info, name='update_company_info'),
    path('company/upload-logo/', views.upload_company_logo, name='upload_company_logo'),
    # Super admin endpoints
    path('admin/organizations/', views.get_all_organizations, name='get_all_organizations'),
    path('admin/stats/', views.get_system_stats, name='get_system_stats'),
]
