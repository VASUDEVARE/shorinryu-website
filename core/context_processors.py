from .models import SiteSettings

def site_settings(request):
    """
    Makes SiteSettings available in ALL templates automatically.
    Use {{ settings.phone }}, {{ settings.email }} anywhere in templates.
    """
    return {'settings': SiteSettings.get()}
