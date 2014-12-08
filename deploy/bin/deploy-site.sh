#!/bin/bash

source /home/foia/.bashrc
cd /home/foia/hub/current
workon fab
fab -H localhost deploy
