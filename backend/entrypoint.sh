#!/bin/bash

if [ -z "$WEB_CONCURRENCY" ]; then
    cores=$(nproc)
    export WEB_CONCURRENCY=$((cores * 2 + 1))
fi

flask --app src.index:app db upgrade

if [ "$FLASK_MODE" = "development" ]; then
    python src/fixtures/fixtures.py
fi

exec "$@"