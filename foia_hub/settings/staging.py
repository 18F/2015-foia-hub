from .notdev import *

# Some possible hosts
ALLOWED_HOSTS = ['open-foia-staging.app.cloud.gov', '127.0.0.1']

try:
    from .local_settings import *
except ImportError:
    pass
