#!/bin/bash

ISSUE_FILE="issue.md"

if [[ ! -f "$ISSUE_FILE" ]]; then
  echo "Không tìm thấy file $ISSUE_FILE."
  exit 1
fi

PR_NUM=${PR_NUMBER:-"Local"}

gh issue create \
  --title "Báo cáo kiểm tra tĩnh cho pull request $PR_NUM" \
  --body-file "$ISSUE_FILE" \
  --assignee "$ACTOR" \
  --label "Documentation"
