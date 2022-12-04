#!/bin/bash
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python shredhub.py create_db
flask db upgrade

exec gunicorn -b :8000 --access-logfile - --error-logfile - shredhub:app \
    --worker-class gevent --timeout 120 --workers=3 --threads=3 --worker-connections=1000