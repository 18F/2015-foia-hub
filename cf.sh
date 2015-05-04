#!/bin/bash
echo "------ Starting APP ------"
if [ $CF_INSTANCE_INDEX = "0" ]; then
    echo "----- Migrating Database -----"
    python manage.py migrate --noinput
    echo "----- Loading Agency Contacts -----"
    python manage.py load_agency_contacts
fi
gunicorn foia_hub.wsgi:application --log-file -
