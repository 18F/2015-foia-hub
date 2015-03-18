from .base import *
import os
import dj_database_url

# See env.example for an explanation of these settings.

SECRET_KEY = os.getenv("FOIA_SECRET_SESSION_KEY")
DATABASES = {'default': dj_database_url.parse(os.getenv("DATABASE_URL"))}
SHOW_WEBFORM = (os.getenv("FOIA_SHOW_WEBFORM") == "true")
ANALYTICS_ID = os.getenv("FOIA_ANALYTICS_ID")

AWS_ACCESS_KEY_ID = os.getenv('FOIA_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('FOIA_AWS_SECRET_ACCESS_KEY')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE':
        'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
