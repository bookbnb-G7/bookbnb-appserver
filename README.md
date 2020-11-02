# Appserver
[![Build Status](https://travis-ci.com/bookbnb-G7/bookbnb-appserver.svg?branch=master)](https://travis-ci.com/bookbnb-G7/bookbnb-appserver)
[![Coverage Status](https://coveralls.io/repos/github/bookbnb-G7/bookbnb-appserver/badge.svg?branch=master)](https://coveralls.io/github/bookbnb-G7/bookbnb-appserver?branch=master)

# Run Tests
`bin/runtest.sh`

# Start local version

## Building and running:
`bin/server.sh up build`

## Running without building:
`bin/server.sh up`

## Pause server:
`bin/server.sh stop`

## Resume server
`bin/server.sh start`

## Stop server and removing local database volume
`bin/server.sh down volume`

## Stop server without preserving local database data
`bin/server.sh down`

# Removing Images, Containes and Volumes associated
`bin/armagedon.sh`
