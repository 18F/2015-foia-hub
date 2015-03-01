"""
WSGI config for foia_hub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

from foia_hub.settings.base import BASE_DIR

if os.getenv("NEW_RELIC_LICENSE_KEY"):
    import newrelic.agent
    newrelic.agent.initialize(os.path.join(
        BASE_DIR, 'newrelic.ini'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foia_hub.settings")
application = Cling(get_wsgi_application())
