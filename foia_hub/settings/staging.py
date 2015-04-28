from .notdev import *

# Some possible hosts
ALLOWED_HOSTS = ['openfoia-staging.cf.18f.us', '127.0.0.1']

try:
    from .local_settings import *
except ImportError:
    pass
