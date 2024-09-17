#!/bin/bash

set -e

wait_for_mongodb() {
	echo "Waiting for MongoDB to start..."
	while ! mongosh --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --eval 'db.runCommand({ ping: 1 })' --quiet; do
		sleep 1
	done
	echo "MongoDB is up and running."
}

wait_for_mongodb

mongosh --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD /docker-entrypoint-initdb.d/init-frontend_data.js
