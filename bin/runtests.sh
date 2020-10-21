#!/bin/bash

docker-compose up -d
docker exec bookbnb-appserver_web bash -c 'while !</dev/tcp/db/5432; do sleep 1; done;'
docker exec bookbnb-appserver_web pytest --cov=appserver --color=yes

if [ ${1-"none"} == "no-lint" ]; then
	docker-compose down
else
	docker exec bookbnb-appserver_web pylint appserver
	docker-compose down
fi

