#!/bin/bash
if [ $1 == "up" ]; then
	echo "==========server=started========="
	if [ ${2-"none"} == "build" ]; then 
		docker-compose up -d --build
	else 
		docker-compose up -d
	fi
	echo "http://localhost:3000"
	echo "================================="
fi

if [ $1 == "down" ]; then
	echo "===========server=down==========="
	if [ ${2-"none"} == "volume" ]; then
		docker-compose down --volume
	else
		docker-compose down
	fi
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
	echo "run bin/server.sh stop to stop"
	echo "================================="
fi