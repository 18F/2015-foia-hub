from .base import *
import os
import json
import dj_database_url

# See env.example for an explanation of these settings.

SECRET_KEY = os.getenv("FOIA_SECRET_SESSION_KEY")
DATABASES = {'default': dj_database_url.parse(os.getenv("DATABASE_URL"))}
SHOW_WEBFORM = (os.getenv("FOIA_SHOW_WEBFORM") == "true")
ANALYTICS_ID = os.getenv("FOIA_ANALYTICS_ID")

AWS_ACCESS_KEY_ID = os.getenv('FOIA_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('FOIA_AWS_SECRET_ACCESS_KEY')
DOCS_SOURCE_BUCKET = os.getenv('FOIA_DOCS_SOURCE_BUCKET')

CF_SERVICES = os.getenv('VCAP_SERVICES')
if CF_SERVICES:
    CF_SERVICES = json.loads(CF_SERVICES)
    ES_URL = CF_SERVICES['elasticsearch-0.20'][0]['credentials']['url']
else:
    ES_URL = 'http://127.0.0.1:9200/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE':
        'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': ES_URL,
        'INDEX_NAME': 'documents',
        'TIMEOUT': 60 * 5,
    },
}
