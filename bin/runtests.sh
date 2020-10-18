#!/bin/sh

docker-compose up -d
docker exec bookbnb-appserver_web pytest --cov=appserver --color=yes
docker-compose down
