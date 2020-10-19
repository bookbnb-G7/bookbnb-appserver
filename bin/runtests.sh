#!/bin/sh

docker-compose up -d
docker exec bookbnb-userserver_web bash -c 'while !</dev/tcp/db/5432; do sleep 1; done;'
docker exec bookbnb-appserver_web pytest --cov=appserver --color=yes
docker exec bookbnb-appserver_web pylint appserver
docker-compose down
