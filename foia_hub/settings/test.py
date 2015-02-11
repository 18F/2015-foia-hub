from .base import *

SECRET_KEY = '#-nl=1b8yr*zr&6dmnv8rj5(f8w7^lv6lyd)7eyjg_xqk$zhe$'

# Flag to determine whether the FOIA request form gets shown.
SHOW_WEBFORM = True
ANALYTICS_ID = 'MyAwesomeAnalyticsCode'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
