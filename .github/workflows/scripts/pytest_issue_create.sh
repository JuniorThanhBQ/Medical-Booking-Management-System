#!/bin/bash

set -o pipefail

FINAL_SUMMARY=$(tail -n 1 pytest_log.txt)

FAILED_CASES=$(grep "^FAILED" pytest_log.txt || echo "Không phát sinh lỗi trong test case.")

ISSUE_BODY="Pytest cảnh báo vấn đề phát sinh.

**Tổng quan:**
\`\`\`text
$FINAL_SUMMARY
\`\`\`

**Các Test Case thất bại (Nếu có):**
\`\`\`text
$FAILED_CASES
\`\`\`

---
*Thông tin chung:*
- **Commit:** $COMMIT_SHA
- **Người cần review lại:** @$ACTOR
- **Chi tiết hành động:** [Xem chi tiết](https://github.com/$REPO/actions/runs/$RUN_ID)"

gh issue create \
  --title "Lỗi Pytest trên PR #$PR_NUMBER" \
  --body "$ISSUE_BODY" \
  --assignee "$ACTOR" \
  --label "bug"
