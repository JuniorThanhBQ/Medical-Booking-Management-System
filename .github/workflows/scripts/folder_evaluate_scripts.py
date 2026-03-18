import os
import subprocess
import sys

extensions = ['.py', '.js', '.jsx', '.sql']

try:
    git_output = subprocess.check_output(['git', 'ls-files', '-z']).decode('utf-8')
    all_files = [f for f in git_output.split('\0') if f]
except Exception:
    sys.exit(1)

target_files = [f for f in all_files if any(f.endswith(ext) for ext in extensions)]
total_lines = 0
file_stats = []

with open('folder_code.txt', 'w', encoding='utf-8') as out_file:
    for filepath in target_files:
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            count = len(lines)
            total_lines += count
            file_stats.append((filepath, count))

            out_file.write(f"\n\n--- Tên file: {filepath} ---\n\n")
            out_file.writelines(lines)

file_stats.sort(key=lambda x: x[1], reverse=True)

repo = os.environ.get('GITHUB_REPOSITORY', 'unknown-repo')
run_id = os.environ.get('GITHUB_RUN_ID', 'unknown-run')
run_url = f"https://github.com/{repo}/actions/runs/{run_id}"

backend_status = os.environ.get('BACKEND_LINT', 'unknown')
frontend_status = os.environ.get('FRONTEND_LINT', 'unknown')
security_status = os.environ.get('SECURITY_CHECK', 'unknown')

def format_status(status):
    if status == 'success': return '**Thành công**'
    if status == 'failure': return '**Thất bại**'
    if status == 'cancelled': return '**Đã hủy**'
    if status == 'skipped': return '**Đã bỏ qua**'
    return f'❓ {status}'

md_content = "## Báo cáo kiểm tra tĩnh cho pull request \n\n"

md_content += "### 1. Trạng thái các jobs:\n"
md_content += "| Hạng mục  | Kết quả |\n|---|---|\n"
md_content += f"| **Kiểm tra backend: ** | {format_status(backend_status)} |\n"
md_content += f"| **Kiểm tra format frontend: ** {format_status(frontend_status)} |\n"
md_content += f"| **Kiểm tra bảo mật: ** | {format_status(security_status)} |\n\n"
md_content += f"*(Xem chi tiết: [Action]({run_url}))*\n\n"
md_content += "---\n\n"

md_content += "### 2. Thống kê về mã nguồn:\n"
md_content += f"- **Tổng số file hợp lệ:** `{len(file_stats)}` files\n"
md_content += f"- **Tổng số dòng code:** `{total_lines}` dòng\n\n"

md_content += "| Tên File | Số dòng |\n|---|---|\n"
for filepath, count in file_stats:
    if count > 250:
        md_content += f"| Cần xem lại: `{filepath}` | **{count}** |\n"
    else:
        md_content += f"| `{filepath}` | {count} |\n"

md_content += "\n---\n"

with open('issue.md', 'w', encoding='utf-8') as f:
    f.write(md_content)