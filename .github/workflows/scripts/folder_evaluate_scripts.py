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

md_content = "## Báo cáo thông tin file\n\n"
md_content += f"- **Tổng số file hợp lệ:** `{len(file_stats)}` files\n"
md_content += f"- **Tổng số dòng:** `{total_lines}` dòng\n\n"
md_content += "### Chi tiết:\n"
md_content += "| Tên File | Số dòng |\n|---|---|\n"

for filepath, count in file_stats:
    if count > 300:
        md_content += f"| `{filepath}` | **{count}** |\n"
    else:
        md_content += f"| `{filepath}` | {count} |\n"

md_content += "\n---\n"
md_content += f"**Tải file code tổng hợp:** [folder_code.txt]({run_url})\n"

with open('issue.md', 'w', encoding='utf-8') as f:
    f.write(md_content)