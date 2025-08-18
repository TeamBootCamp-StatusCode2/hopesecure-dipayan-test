from django.urls import path
from . import views

urlpatterns = [
    path('', views.TemplateListCreateView.as_view(), name='template-list-create'),
    path('<int:pk>/', views.TemplateDetailView.as_view(), name='template-detail'),
    path('<int:pk>/clone/', views.clone_template, name='template-clone'),
    path('<int:pk>/preview/', views.preview_template, name='template-preview'),
    path('stats/', views.template_stats, name='template-stats'),
    path('categories/', views.template_categories, name='template-categories'),
    path('by-category/', views.template_by_category, name='template-by-category'),
    path('tags/', views.TemplateTagListView.as_view(), name='template-tags'),
]
