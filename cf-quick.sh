#!/bin/bash

echo "------ Create database tables ------"

python manage.py migrate --noinput
waitress-serve --port=$VCAP_APP_PORT foia_hub.wsgi:application
