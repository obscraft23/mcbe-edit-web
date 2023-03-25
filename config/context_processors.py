from django.conf import settings

def google_analytics(request):
    
    ga_tracking_id = getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', False)

    if not settings.DEBUG and ga_tracking_id:
        return {
            'GOOGLE_ANALYTICS_TRACKING_ID': ga_tracking_id,
        }
    return {}