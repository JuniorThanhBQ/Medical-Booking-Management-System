#!/bin/bash

LOG_FILE="pytest_log.txt"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "Có lỗi khi tạo $LOG_FILE"
  exit 1
fi

FINAL_SUMMARY=$(tail -n 1 "$LOG_FILE")
FAILED_CASES=$(grep "^FAILED" "$LOG_FILE" || echo "Lỗi ngoài phạm vi kiểm thử.")
ISSUE_BODY_FILE="issue_body.md"

cat << EOF > "$ISSUE_BODY_FILE"
## Có lỗi trong Pytest

**Tổng quan:**
\`\`\`text
$FINAL_SUMMARY
\`\`\`

**Các Test Case thất bại:**
\`\`\`text
$FAILED_CASES
\`\`\`

---
### Thông tin liên quan:
- **Mã commit:** \`$COMMIT_SHA\`
- **Người cần xem lại:** @$ACTOR
- **Link action:** [Xem log chi tiết tại đây](https://github.com/$REPO/actions/runs/$RUN_ID)
EOF

gh issue create \
  --title "Lỗi Pytest trên PR #${PR_NUMBER}" \
  --body-file "$ISSUE_BODY_FILE" \
  --assignee "$ACTOR" \
  --label "bug"

rm "$ISSUE_BODY_FILE"
