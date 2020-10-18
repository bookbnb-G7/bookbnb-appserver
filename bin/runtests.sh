#!/bin/sh

docker-compose up -d
docker exec bookbnb-appserver_web pytest --cov=appserver --color=yes
docker exec bookbnb-appserver_web pylint appserver
docker-compose down
