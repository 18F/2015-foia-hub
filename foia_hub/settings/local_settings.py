from .base import *
import os
import dj_database_url

# See env.example for an explanation of these settings.

SECRET_KEY = os.getenv("FOIA_SECRET_SESSION_KEY")
DATABASES = {'default': dj_database_url.parse(os.getenv("FOIA_DB"))}
SHOW_WEBFORM = (os.getenv("FOIA_SHOW_WEBFORM") == "true")
ANALYTICS_ID = os.getenv("FOIA_ANALYTICS_ID")
