from .base import *
import os
import re
import dj_database_url
from cfenv import AppEnv

database_url = os.getenv("DATABASE_URL")

env = AppEnv()
cf_foia_db = env.get_service(name=re.compile('foia-db'))
if cf_foia_db:
    database_url = cf_foia_db.credentials['uri']

# See env.example for an explanation of these settings.

SECRET_KEY = os.getenv("FOIA_SECRET_SESSION_KEY")
DATABASES = {'default': dj_database_url.parse(database_url)}
SHOW_WEBFORM = (os.getenv("FOIA_SHOW_WEBFORM") == "true")
ANALYTICS_ID = os.getenv("FOIA_ANALYTICS_ID")
