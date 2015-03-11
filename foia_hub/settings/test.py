import os
from .base import *

SECRET_KEY = '#-nl=1b8yr*zr&6dmnv8rj5(f8w7^lv6lyd)7eyjg_xqk$zhe$'

# Flag to determine whether the FOIA request form gets shown.
SHOW_WEBFORM = True
ANALYTICS_ID = 'MyAwesomeAnalyticsCode'

# To run with postgresql `export TEST_ENGINE=postgresql_psycopg2`
# Default will be sqlite3
custom_backend = os.getenv("TEST_ENGINE")
if custom_backend:
    ENGINE = "django.db.backends.%s" % custom_backend
else:
    ENGINE = "django.db.backends.sqlite3"

DATABASES = {
    'default': {
        'ENGINE': ENGINE
    }
}
