#!/bin/sh

if [ "$ENV" = "production" ]; then
    echo "Running in production mode."
    echo "Waiting for PostgreSQL to be running on: $DATABASE_HOST"

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
else
    echo "Running in development mode."
    cd server_dir
    poetry run python3 manage.py flush --no-input
    poetry run python3 manage.py migrate
    poetry run python3 manage.py makemigrations
fi

# Continue with the provided command or entry point
exec "$@"
