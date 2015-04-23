#!/bin/bash
echo "------ Starting APP ------"
waitress-serve --port=$VCAP_APP_PORT foia_hub.wsgi:application
