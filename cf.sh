#!/bin/bash
echo "------ Starting APP ------"
gunicorn foia_hub.wsgi:application --log-file -
