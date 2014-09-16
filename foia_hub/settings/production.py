from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['foia.18f.us']

try:
    from .local_settings import *
except ImportError:
    pass
