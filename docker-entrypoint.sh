#!/bin/sh
cd appserver/
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uvicorn app.main:app --host=0.0.0.0 --port="${PORT:-5000}"
