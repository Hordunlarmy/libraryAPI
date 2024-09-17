#!/bin/bash

set -e

# Wait for MariaDB to start
sleep 10

# Create the database if it doesn't already exist
mariadb -u horduntech -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Run the SQL scripts in order
for script in /opt/init-backend_db.sql /opt/init-backend_data.sql; do
	if [ -f "$script" ]; then
		echo "Running $script..."
		mariadb -u horduntech -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" <"$script"
	else
		echo "Warning: $script not found, skipping."
	fi
done

# Execute the original MariaDB entrypoint
exec docker-entrypoint.sh "$@"
