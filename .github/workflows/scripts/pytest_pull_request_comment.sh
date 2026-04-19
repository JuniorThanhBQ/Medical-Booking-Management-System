#!/bin/bash

LOG_FILE="pytest_log.txt"
FINAL_SUMMARY=$(tail -n 1 "$LOG_FILE")
FAILED_CASES=$(grep "^FAILED" "$LOG_FILE" || echo "Lỗi nằm ngoài phạm vi bao phủ.")
COMMENT_BODY_FILE="comment_body.md"

cat << EOF > "$COMMENT_BODY_FILE"
## Phát hiện lỗi trong quá trình kiểm thử

**Tổng quan:**
\`\`\`text
$FINAL_SUMMARY
\`\`\`

**Các Test Case thất bại:**
\`\`\`text
$FAILED_CASES
\`\`\`

---
*Người thực hiện:* @$ACTOR
*Chi tiết:* [xem tại log Github Actions](https://github.com/$REPO/actions/runs/$RUN_ID). 
EOF

if [ "$PR_NUMBER" != "Local" ] && [ -n "$PR_NUMBER" ]; then
  gh pr comment "$PR_NUMBER" --body-file "$COMMENT_BODY_FILE"
fi

rm "$COMMENT_BODY_FILE"
