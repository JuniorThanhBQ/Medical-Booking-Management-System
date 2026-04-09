#!/bin/bash

if [ -z "$WEB_CONCURRENCY" ]; then
    cores=$(nproc)
    export WEB_CONCURRENCY=$((cores * 2 + 1))
fi

exec "$@"