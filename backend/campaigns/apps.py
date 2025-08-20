from django.apps import AppConfig


class CampaignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campaigns'
    
    def ready(self):
        # Import signals when ready
        try:
            import campaigns.signals
        except ImportError as e:
            print(f"Warning: Could not import signals: {e}")
