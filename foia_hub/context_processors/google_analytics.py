from django.conf import settings

def google_analytics(request):
    """ This should make the Google ANALYTICS_ID available to all templates.
    """
    return {'ANALYTICS_ID': settings.ANALYTICS_ID}
