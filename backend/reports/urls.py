from django.urls import path
from . import views

urlpatterns = [
    # Report URLs will be added here
    path('', views.ReportListCreateView.as_view(), name='report-list-create'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
]
