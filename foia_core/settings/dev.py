from foia_core.settings.default import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#-nl=1b8yr*zr&6dmnv8rj5(f8w7^lv6lyd)7eyjg_xqk$zhe$'


INSTALLED_APPS = (
    'debug_toolbar',
) + INSTALLED_APPS


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'foia',
        'USER': 'foia',
        'PASSWORD': 'foia',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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
