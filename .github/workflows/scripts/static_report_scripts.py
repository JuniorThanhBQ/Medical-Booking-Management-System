import os
import subprocess
import sys

extensions = [".py", ".js", ".jsx", ".sql"]

try:
    git_output = subprocess.check_output(["git", "ls-files", "-z"]).decode("utf-8")
    all_files = [f for f in git_output.split("\0") if f]
except Exception:
    sys.exit(1)

target_files = [f for f in all_files if any(f.endswith(ext) for ext in extensions)]
total_lines = 0
file_stats = []

with open("folder_code.txt", "w", encoding="utf-8") as out_file:
    for filepath in target_files:
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            count = len(lines)
            total_lines += count
            file_stats.append((filepath, count))

            out_file.write(f"\n\n--- Tên file: {filepath} ---\n\n")
            out_file.writelines(lines)

file_stats.sort(key=lambda x: x[1], reverse=True)

repo = os.environ.get("GITHUB_REPOSITORY", "Repo không tồn tại")
run_id = os.environ.get("GITHUB_RUN_ID", "Mã id chạy không hợp lệ")
url = f"https://github.com/{repo}/actions/runs/{run_id}"
backend_status = os.environ.get("BACKEND_LINT", "Không rõ")
frontend_status = os.environ.get("FRONTEND_LINT", "Không rõ")
backend_security_status = os.environ.get("BACKEND_SECURITY_CHECK", "Không rõ")
frontend_security_status = os.environ.get("FRONTEND_SECURITY_CHECK", "Không rõ")
docker_build_status = os.environ.get("DOCKER_BUILD_CHECK", "Không rõ")

def format_status(status):
    if status == "success":
        return "**Thành công**"
    if status == "failure":
        return "**Thất bại**"
    if status == "cancelled":
        return "**Đã hủy**"
    if status == "skipped":
        return "**Đã bỏ qua**"
    return f"Có lỗi xảy ra {status}"

md_content = f"""## Báo cáo kiểm tra tĩnh

### 1. Trạng thái kiểm tra chung:
| Hạng mục | Kết quả |
|---|---|
| Kiểm tra format backend: | {format_status(backend_status)} |
| Kiểm tra format frontend: | {format_status(frontend_status)} |
| Kiểm tra bảo mật backend: | {format_status(backend_security_status)} |
| Kiểm tra bảo mật frontend: | {format_status(frontend_security_status)} |
| Kiểm tra build docker: | {format_status(docker_build_status)} |

*(Xem chi tiết: [link]({url}))*

---

### 2. Thống kê mã nguồn:
- **Tổng số file:** `{len(file_stats)}` files
- **Tổng số dòng code:** `{total_lines}` dòng

| Tên File | Số dòng |
|---|---|
"""

for filepath, count in file_stats:
    if count > 500:
        md_content += f"| Cần xem lại: `{filepath}` | **{count}** |\n"
    else:
        md_content += f"| `{filepath}` | {count} |\n"

with open("issue.md", "w", encoding="utf-8") as f:
    f.write(md_content)
