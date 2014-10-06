#!/bin/bash
FOIA_DIR=${1:-"../foia"}

pushd $FOIA_DIR
git fetch
if [[ `git log HEAD..origin/master --oneline` ]]; then
  git pull origin master
  popd
  python manage.py load_agency_contacts ${FOIA_DIR}/contacts/data
fi
