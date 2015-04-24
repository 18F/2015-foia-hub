#!/bin/bash

###
# Zero downtime deploy script for foia-hub.
#
# Deploys a new version of the foia app, then once that works,
# flips the route to point at the new version.
#
# The old version of the app stays around and can be reverted to
# by running map-route and unmap-route.
#
# Modeled after http://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html
# and https://github.com/dlapiduz/fugacious/blob/master/cf-deploy.sh
###

ROUTE="open.foia.gov"
PUSH="cf.sh"

# The first grep can't have -q or the second grep won't have anything to grep!
if $(cf app foia-a | grep "requested state" | grep -q started)
then
  OLD="foia-a"
  NEW="foia-b"
else
  OLD="foia-b"
  NEW="foia-a"
fi

echo "Pushing new app to $NEW, using $PUSH, and disabling $OLD."

cf push $NEW -c "bash $PUSH"

if [[ $? -ne 0 ]]; then
  echo "Error pushing to $NEW."
  cf stop $NEW
  exit 1
fi

echo "Re-routing $ROUTE to $NEW."
cf map-route $NEW $ROUTE
echo "Un-routing $ROUTE from $OLD."
cf unmap-route $OLD $ROUTE
cf stop $OLD

echo "Done."
