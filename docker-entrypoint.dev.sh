#!/bin/sh
cd appserver/ 
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8080
