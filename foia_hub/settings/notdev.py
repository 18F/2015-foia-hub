from .base import *
import os

# There are common settings between staging and production. This puts them
# all in one place.

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.getenv('TMPDIR', '/tmp'),
        'TIMEOUT': 1440,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        },
    }
}
