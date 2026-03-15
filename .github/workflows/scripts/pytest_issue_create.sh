#!/bin/bash

set -o pipefail

FINAL_SUMMARY=$(tail -n 1 pytest_log.txt)

FAILED_CASES=$(grep "^FAILED" pytest_log.txt || echo "Không có test case lỗi.")

ISSUE_BODY="Một trong các test case gặp vấn đề.

**Tổng quan:**
\`\`\`text
$FINAL_SUMMARY
\`\`\`

**Các Test Case thất bại:**
\`\`\`text
$FAILED_CASES
\`\`\`

---
*Thông tin chung:*
- **Commit:** $COMMIT_SHA
- **Người phụ trách:** @$ACTOR
- **Action Run:** [Xem chi tiết](https://github.com/$REPO/actions/runs/$RUN_ID)"

gh issue create \
  --title "Lỗi Pytest trên PR #$PR_NUMBER" \
  --body "$ISSUE_BODY" \
  --assignee "$ACTOR" \
  --label "bug"
