from .base import *
import imp

DEBUG = True
TEMPLATE_DEBUG = True

# Flag to determine whether the FOIA request form gets shown.
SHOW_WEBFORM = False

try:
    imp.find_module('debug_toolbar')
    INSTALLED_APPS = (
        'debug_toolbar',
    ) + INSTALLED_APPS
except ImportError:
    pass

DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r"^(?!debug_toolbar/).*"

INTERNAL_IPS = ('127.0.0.1',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

try:
    from .local_settings import *
except ImportError:
    pass
