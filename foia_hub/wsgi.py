"""
WSGI config for foia_hub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import subprocess

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from foia_hub.settings.base import BASE_DIR


# If running on Cloud Foundry and using 0th instance apply migrations
# and load agency contacts
instance_id = os.getenv('CF_INSTANCE_INDEX')
if instance_id == '0':
    subprocess.Popen(['echo', '"----- Applying Migrations -----"'])
    subprocess.Popen(['python', 'manage.py', 'migrate', '--noinput'])
    subprocess.Popen(['echo', '"-----Loading Agency Contacts -----"'])
    subprocess.Popen(['python', 'manage.py', 'load_agency_contacts'])


if os.getenv("NEW_RELIC_LICENSE_KEY"):
    import newrelic.agent
    newrelic.agent.initialize(os.path.join(
        BASE_DIR, 'newrelic.ini'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foia_hub.settings")
application = Cling(get_wsgi_application())
