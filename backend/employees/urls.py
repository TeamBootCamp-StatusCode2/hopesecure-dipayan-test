from django.urls import path
from . import views

urlpatterns = [
    # Employee URLs will be added here
    path('', views.EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('stats/', views.employee_stats, name='employee-stats'),
]
