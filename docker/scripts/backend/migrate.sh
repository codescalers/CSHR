#!/bin/sh

if [ "$ENV" = "production" ]
then
    echo "Runing on production mode."
    echo "Waiting for postgres to be running on: $DATABASE_HOST"

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd server_dir
poetry run python3 manage.py flush --no-input
poetry run python3 manage.py migrate

exec "$@"
