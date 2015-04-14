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

DEFAULT_DATA_REPO = "https://github.com/18F/foia.git"

DATABASES = {}
HAYSTACK_CONNECTIONS = {'default': {}}

# ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosecure',
    'corsheaders',
    'haystack',
    'storages',
    'foia_hub',
    'contact_updater',
    'docusearch',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
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

# # JINJA SETTINGS
TEMPLATE_LOADERS = (
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)


# We have to add the default processors
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "foia_hub.context_processors.google_analytics.google_analytics")

INSTALLED_APPS += ('django_jinja',)
DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.html'

# Enable bytecode cache (default: False)
# JINJA2_BYTECODE_CACHE_ENABLE = False

# Cache backend name for bytecode cache (default: "default")
# JINJA2_BYTECODE_CACHE_NAME = "default"

# Specify custom bytecode cache subclass (default: None)
# JINJA2_BYTECODE_CACHE_BACKEND = "path.to.you.cache.class"
# #/ END JINJA SETTINGS

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
STATIC_ROOT = 'staticfiles'

# turn on CORS for everything (will be locked down later)
CORS_ORIGIN_ALLOW_ALL = True

ANALYTICS_ID = ""

# Don't add complex authentication related query parameters for requests
AWS_QUERYSTRING_AUTH = False

# Don't allow client-side JS to access CSRF cookie
CSRF_COOKIE_HTTPONLY = True
