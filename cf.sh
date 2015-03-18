#!/bin/bash

echo "------ Create database tables ------"

python manage.py migrate --noinput
python manage.py load_agency_contacts
waitress-serve --port=$VCAP_APP_PORT foia_hub.wsgi:application
