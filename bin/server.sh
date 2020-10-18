#!/bin/bash
echo "entre"

if [ $1 == "up" ]; then
	echo "==========server=started========="
	docker-compose up -d
	echo "http://localhost:3000"
	echo "================================="
fi

if [ $1 == "down" ]; then
	echo "===========server=down==========="
	docker-compose down
	echo "================================="
fi

if [ $1 == "stop" ]; then
	echo "=========server=stopped=========="
	docker-compose stop
	echo "run bin/server.sh start to resume"
	echo "================================="
fi

if [ $1 == "start" ]; then
	echo "=========server=started=========="
	docker-compose start
	echo "run bin/server.sh strp to stop"
	echo "================================="
fi