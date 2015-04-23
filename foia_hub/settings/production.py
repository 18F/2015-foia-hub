from .base import *
import os

DEBUG = False
TEMPLATE_DEBUG = False

# Flag to determine whether the FOIA request form gets shown.
SHOW_WEBFORM = False

# Some possible hosts
ALLOWED_HOSTS = ['open.foia.gov', 'foia-a.cf.18f.us', 'foia-b.cf.18f.us', 'openfoia-staging.cf.18f.us']

# Force an HTTPS connection.
# When testing production mode locally, this may require using ngrok.
SECURE_SSL_REDIRECT = True

# Amazon ELBs pass on X-Forwarded-Proto.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Turn on once we're good and set.
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# In production we will have HTTPS setup.
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

AWS_STORAGE_BUCKET_NAME = os.getenv('FOIA_S3_STATIC_BUCKET_NAME')
AWS_STORAGE_DOC_BUCKET = os.getenv('FOIA_S3_DOCS_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Don't add complex authentication related query parameters for requests
AWS_QUERYSTRING_AUTH = False

try:
    from .local_settings import *
except ImportError:
    pass
