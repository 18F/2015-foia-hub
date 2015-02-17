from .base import *
import os

SECRET_KEY = os.getenv("FOIA_SECRET_SESSION_KEY") or 'SET THIS PLEASE'

# If the DB engine is defined, it's assumed the rest are too.
db = os.getenv("FOIA_DB_ENGINE")
if db:
  DATABASES = {
      'default': {
          'ENGINE': db,
      }
  }

  if os.getenv("FOIA_DB_NAME"):
    DATABASES['default']['NAME'] = os.getenv("FOIA_DB_NAME")
  if os.getenv("FOIA_DB_USER"):
    DATABASES['default']['USER'] = os.getenv("FOIA_DB_USER")
  if os.getenv("FOIA_DB_PASSWORD"):
    DATABASES['default']['PASSWORD'] = os.getenv("FOIA_DB_PASSWORD")
  if os.getenv("FOIA_DB_HOST"):
    DATABASES['default']['HOST'] = os.getenv("FOIA_DB_HOST")
  if os.getenv("FOIA_DB_PORT"):
    DATABASES['default']['PORT'] = os.getenv("FOIA_DB_PORT")

# Defaults to a sqlite3 db in project root called default.db
else:
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': 'default.db'
      }
  }

webform = os.getenv("FOIA_SHOW_WEBFORM")
if webform and (webform.lower() != "false"):
  SHOW_WEBFORM = True
else:
  SHOW_WEBFORM = False

ANALYTICS_ID = os.getenv("FOIA_ANALYTICS_ID") or ""
