#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/backend/src

python -m pytest -v --cov=. --cov-report=term-missing > pytest_log.txt 2>&1 || exit_code=$?
exit_code=${exit_code:-0}

if [ $exit_code -eq 5 ]; then
  exit 0
elif [ $exit_code -ne 0 ]; then
  cat pytest_log.txt
  exit $exit_code
else
  cat pytest_log.txt | grep -E "Name|Stmts|Miss|Cover|TOTAL"
  exit 0
fi
