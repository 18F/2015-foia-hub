from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

# Flag to determine whether the FOIA request form gets shown.
SHOW_WEBFORM = False

ALLOWED_HOSTS = ['foia.18f.us']

# if testing out production settings in development:
# ALLOWED_HOSTS = ['foia.18f.us', 'localhost']

try:
    from .local_settings import *
except ImportError:
    pass
