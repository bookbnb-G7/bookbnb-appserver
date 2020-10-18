#!/bin/bash

docker-compose down --volume --rmi local --remove-orphans

echo "=====================IMAGES=========================="
docker images
echo "====================================================="

echo ""

echo "====================CONTAINERS======================="
docker ps
echo "====================================================="

echo ""

echo "=====================VOLUMES========================="
docker volume ls
echo "====================================================="