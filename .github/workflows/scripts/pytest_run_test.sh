#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/backend/src

python -m pytest -v --cov=. --cov-report=term-missing > pytest_log.txt 2>&1 || exit_code=$?
exit_code=${exit_code:-0}

if [ $exit_code -eq 5 ]; then
  echo "Không có test case"
  exit 0
elif [ $exit_code -ne 0 ]; then
  echo "Có lỗi xảy ra trong test case: "
  cat pytest_log.txt
  exit $exit_code
else
  echo "Bảng tóm tắt độ phủ: "
  cat pytest_log.txt | grep -E "Name|Stmts|Miss|Cover|TOTAL"
  exit 0
fi