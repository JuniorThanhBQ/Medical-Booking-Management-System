#!/bin/bash

if [ -z "$WEB_CONCURRENCY" ]; then
    cores=$(nproc)
    export WEB_CONCURRENCY=$((cores * 2 + 1))
fi

if [ "$1" = "gunicorn" ]; then
    flask --app src.index:app db upgrade
    python src/fixtures/fixtures.py
fi

exec "$@"