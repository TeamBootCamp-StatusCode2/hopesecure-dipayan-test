"""
Activity logging utilities for the admin dashboard
"""
from .models import ActivityLog, SystemAlert


def log_activity(user=None, organization=None, action_type='admin_action', 
                description='', severity='low', ip_address=None, 
                user_agent='', metadata=None):
    """Helper function to log activities"""
    if metadata is None:
        metadata = {}
    
    ActivityLog.objects.create(
        user=user,
        organization=organization,
        action_type=action_type,
        description=description,
        severity=severity,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata
    )


def create_system_alert(alert_type, title, description, severity='medium', 
                       organization=None, created_by=None):
    """Helper function to create system alerts"""
    SystemAlert.objects.create(
        alert_type=alert_type,
        title=title,
        description=description,
        severity=severity,
        organization=organization,
        created_by=created_by
    )


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Get user agent from request"""
    return request.META.get('HTTP_USER_AGENT', '')


# Activity logging decorators and middleware can be added here
class ActivityLoggerMiddleware:
    """Middleware to log important activities automatically"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Log failed login attempts
        if request.path == '/api/auth/login/' and response.status_code == 400:
            log_activity(
                user=None,
                action_type='failed_login',
                description=f'Failed login attempt for {request.data.get("email", "unknown")}',
                severity='medium',
                ip_address=get_client_ip(request),
                user_agent=get_user_agent(request),
                metadata={'endpoint': request.path}
            )
        
        # Log successful logins
        elif request.path == '/api/auth/login/' and response.status_code == 200:
            if hasattr(request, 'user') and request.user.is_authenticated:
                log_activity(
                    user=request.user,
                    organization=request.user.organization,
                    action_type='login',
                    description=f'User {request.user.email} logged in successfully',
                    severity='low',
                    ip_address=get_client_ip(request),
                    user_agent=get_user_agent(request),
                    metadata={'endpoint': request.path}
                )
        
        return response
