from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/details/', views.UserProfileUpdateView.as_view(), name='profile-details'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]
