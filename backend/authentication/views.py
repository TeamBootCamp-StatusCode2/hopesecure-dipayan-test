from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import User, UserProfile, ActivityLog, SystemAlert
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserUpdateSerializer, PasswordChangeSerializer, UserProfileSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create authentication token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """User login endpoint"""
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get or create authentication token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        # Delete the user's token
        request.user.auth_token.delete()
    except:
        pass
    
    logout(request)
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.UpdateAPIView):
    """Update user profile information"""
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.GenericAPIView):
    """Change user password"""
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Invalidate all existing tokens
        Token.objects.filter(user=user).delete()
        # Create new token
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Password changed successfully',
            'token': token.key
        }, status=status.HTTP_200_OK)


class UserProfileUpdateView(generics.UpdateAPIView):
    """Update user profile details"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for the current user"""
    user = request.user
    
    # Basic user stats
    stats = {
        'user': UserSerializer(user).data,
        'role': user.role,
        'department': user.department,
    }
    
    # Role-specific stats
    if user.role in ['admin', 'manager', 'analyst']:
        from campaigns.models import Campaign
        from templates.models import Template
        from employees.models import Employee
        
        stats.update({
            'total_campaigns': Campaign.objects.count(),
            'active_campaigns': Campaign.objects.filter(status='active').count(),
            'total_templates': Template.objects.count(),
            'total_employees': Employee.objects.filter(is_active=True).count(),
        })
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_logs(request):
    """Get activity logs for admin monitoring"""
    user = request.user
    
    # Only allow admins and super admins to view logs
    if user.role not in ['admin', 'super_admin']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get filter parameters
    days = int(request.GET.get('days', 7))  # Default to 7 days
    severity = request.GET.get('severity', None)
    action_type = request.GET.get('action_type', None)
    page_size = int(request.GET.get('page_size', 50))
    
    # Base queryset
    logs = ActivityLog.objects.all()
    
    # Apply filters
    if user.role != 'super_admin' and user.organization:
        # Regular admins only see their organization's logs
        logs = logs.filter(organization=user.organization)
    
    # Time filter
    start_date = timezone.now() - timedelta(days=days)
    logs = logs.filter(timestamp__gte=start_date)
    
    # Severity filter
    if severity:
        logs = logs.filter(severity=severity)
    
    # Action type filter
    if action_type:
        logs = logs.filter(action_type=action_type)
    
    # Limit results
    logs = logs[:page_size]
    
    # Serialize data
    log_data = []
    for log in logs:
        log_data.append({
            'id': log.id,
            'user': log.user.email if log.user else 'System',
            'user_name': log.user.full_name if log.user else 'System',
            'organization': log.organization.name if log.organization else 'System',
            'action_type': log.action_type,
            'action_display': log.get_action_type_display(),
            'description': log.description,
            'severity': log.severity,
            'severity_display': log.get_severity_display(),
            'ip_address': log.ip_address,
            'timestamp': log.timestamp.isoformat(),
            'metadata': log.metadata,
        })
    
    # Get summary statistics
    stats = {
        'total_logs': logs.count(),
        'critical_count': logs.filter(severity='critical').count(),
        'high_count': logs.filter(severity='high').count(),
        'medium_count': logs.filter(severity='medium').count(),
        'low_count': logs.filter(severity='low').count(),
    }
    
    return Response({
        'logs': log_data,
        'stats': stats,
        'filters': {
            'days': days,
            'severity': severity,
            'action_type': action_type,
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def system_alerts(request):
    """Get system alerts for admin monitoring"""
    user = request.user
    
    # Only allow admins and super admins to view alerts
    if user.role not in ['admin', 'super_admin']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'active')
    severity_filter = request.GET.get('severity', None)
    alert_type_filter = request.GET.get('alert_type', None)
    page_size = int(request.GET.get('page_size', 20))
    
    # Base queryset
    alerts = SystemAlert.objects.all()
    
    # Apply filters
    if user.role != 'super_admin' and user.organization:
        # Regular admins only see their organization's alerts
        alerts = alerts.filter(Q(organization=user.organization) | Q(organization__isnull=True))
    
    # Status filter
    if status_filter:
        alerts = alerts.filter(status=status_filter)
    
    # Severity filter
    if severity_filter:
        alerts = alerts.filter(severity=severity_filter)
    
    # Alert type filter
    if alert_type_filter:
        alerts = alerts.filter(alert_type=alert_type_filter)
    
    # Limit results
    alerts = alerts[:page_size]
    
    # Serialize data
    alert_data = []
    for alert in alerts:
        alert_data.append({
            'id': alert.id,
            'alert_type': alert.alert_type,
            'alert_type_display': alert.get_alert_type_display(),
            'title': alert.title,
            'description': alert.description,
            'severity': alert.severity,
            'severity_display': alert.get_severity_display(),
            'status': alert.status,
            'status_display': alert.get_status_display(),
            'organization': alert.organization.name if alert.organization else 'System-wide',
            'created_by': alert.created_by.email if alert.created_by else 'System',
            'created_at': alert.created_at.isoformat(),
            'resolved_at': alert.resolved_at.isoformat() if alert.resolved_at else None,
            'resolved_by': alert.resolved_by.email if alert.resolved_by else None,
        })
    
    # Get summary statistics
    stats = {
        'total_alerts': alerts.count(),
        'active_alerts': SystemAlert.objects.filter(status='active').count(),
        'critical_alerts': SystemAlert.objects.filter(severity='critical', status='active').count(),
        'security_alerts': SystemAlert.objects.filter(alert_type='security', status='active').count(),
    }
    
    return Response({
        'alerts': alert_data,
        'stats': stats,
        'filters': {
            'status': status_filter,
            'severity': severity_filter,
            'alert_type': alert_type_filter,
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_dashboard_overview(request):
    """Get comprehensive dashboard overview for admins"""
    user = request.user
    
    # Only allow admins and super admins
    if user.role not in ['admin', 'super_admin']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Time ranges
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    # Base querysets
    logs_qs = ActivityLog.objects.all()
    alerts_qs = SystemAlert.objects.all()
    
    if user.role != 'super_admin' and user.organization:
        logs_qs = logs_qs.filter(organization=user.organization)
        alerts_qs = alerts_qs.filter(Q(organization=user.organization) | Q(organization__isnull=True))
    
    # Activity statistics
    activity_stats = {
        'total_activities_24h': logs_qs.filter(timestamp__gte=last_24h).count(),
        'total_activities_7d': logs_qs.filter(timestamp__gte=last_7d).count(),
        'critical_activities_24h': logs_qs.filter(timestamp__gte=last_24h, severity='critical').count(),
        'login_attempts_24h': logs_qs.filter(timestamp__gte=last_24h, action_type__in=['login', 'failed_login']).count(),
        'failed_logins_24h': logs_qs.filter(timestamp__gte=last_24h, action_type='failed_login').count(),
        'security_events_24h': logs_qs.filter(timestamp__gte=last_24h, action_type__in=['phishing_attempt', 'security_alert']).count(),
    }
    
    # Alert statistics
    alert_stats = {
        'active_alerts': alerts_qs.filter(status='active').count(),
        'critical_alerts': alerts_qs.filter(status='active', severity='critical').count(),
        'security_alerts': alerts_qs.filter(status='active', alert_type='security').count(),
        'new_alerts_24h': alerts_qs.filter(created_at__gte=last_24h).count(),
    }
    
    # Recent critical activities (last 10)
    recent_critical = logs_qs.filter(severity__in=['critical', 'high']).order_by('-timestamp')[:10]
    critical_activities = []
    for log in recent_critical:
        critical_activities.append({
            'action': log.get_action_type_display(),
            'description': log.description,
            'severity': log.severity,
            'user': log.user.email if log.user else 'System',
            'timestamp': log.timestamp.isoformat(),
        })
    
    # Recent alerts (last 5)
    recent_alerts = alerts_qs.filter(status='active').order_by('-created_at')[:5]
    alert_summary = []
    for alert in recent_alerts:
        alert_summary.append({
            'title': alert.title,
            'severity': alert.severity,
            'alert_type': alert.get_alert_type_display(),
            'created_at': alert.created_at.isoformat(),
        })
    
    # System health indicators
    system_health = {
        'overall_status': 'healthy',  # Can be 'healthy', 'warning', 'critical'
        'uptime_percentage': 99.8,
        'active_users_24h': logs_qs.filter(timestamp__gte=last_24h, action_type='login').values('user').distinct().count(),
        'active_organizations': User.objects.filter(organization__isnull=False).values('organization').distinct().count(),
    }
    
    # Determine overall system status
    if alert_stats['critical_alerts'] > 0:
        system_health['overall_status'] = 'critical'
    elif alert_stats['security_alerts'] > 3 or activity_stats['failed_logins_24h'] > 20:
        system_health['overall_status'] = 'warning'
    
    return Response({
        'activity_stats': activity_stats,
        'alert_stats': alert_stats,
        'critical_activities': critical_activities,
        'recent_alerts': alert_summary,
        'system_health': system_health,
        'timestamp': now.isoformat(),
    }, status=status.HTTP_200_OK)
