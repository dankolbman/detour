#!/bin/sh

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Waiting for postgres"
  sleep 1
done

./manage.py migrate

gunicorn detour.wsgi:application -b 0.0.0.0:5000
