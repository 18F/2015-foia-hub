from .notdev import *

# Some possible hosts
ALLOWED_HOSTS = [
    'open.foia.gov', 'foia-a.cf.18f.us', 'foia-b.cf.18f.us',
    'openfoia-staging.cf.18f.us'
]

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
