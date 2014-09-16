"""
Django settings for foia_hub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


DATABASES = {}

# ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'foia_hub',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'foia_hub.urls'
WSGI_APPLICATION = 'foia_hub.wsgi.application'

## JINJA SETTINGS
TEMPLATE_LOADERS = (
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)

INSTALLED_APPS += ('django_jinja',)

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.html'

# Enable bytecode cache (default: False)
#JINJA2_BYTECODE_CACHE_ENABLE = False

# Cache backend name for bytecode cache (default: "default")
#JINJA2_BYTECODE_CACHE_NAME = "default"

# Specify custom bytecode cache subclass (default: None)
#JINJA2_BYTECODE_CACHE_BACKEND = "path.to.you.cache.class"
##/ END JINJA SETTINGS

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# turn on CORS for everything (will be locked down later)
CORS_ORIGIN_ALLOW_ALL = True
