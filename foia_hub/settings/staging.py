from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

# Flag to determine whether the FOIA request form gets shown.
SHOW_WEBFORM = False

# Some possible hosts
ALLOWED_HOSTS = ['openfoia-staging.cf.18f.us', 'krang-staging.cf.18f.us']

# Importing bucket names
AWS_STORAGE_STATIC_BUCKET = os.getenv('FOIA_S3_STATIC_BUCKET_NAME')
AWS_STORAGE_DOC_BUCKET = os.getenv('FOIA_S3_DOCS_BUCKET_NAME')
# Settings for the staticfile bucket
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_STATIC_BUCKET
STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# Settings for the document bucket
DOC_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_DOC_BUCKET
DOC_URL = 'https://%s/' % DOC_DOMAIN

# Don't add complex authentication related query parameters for requests
AWS_QUERYSTRING_AUTH = False

try:
    from .local_settings import *
except ImportError:
    pass
