import os
import subprocess
import sys


class StaticReportScripts:
    def __init__(self):
        self.extensions = [".py", ".js", ".jsx", ".sql"]
        self.total_lines = 0
        self.file_stats = []

    def fetch_git_files(self):
        try:
            git_output = subprocess.check_output(["git", "ls-files", "-z"]).decode("utf-8")
            return [f for f in git_output.split("\0") if f]
        except Exception:
            sys.exit(1)

    def filter_files(self, all_files):
        return [f for f in all_files if any(f.endswith(ext) for ext in self.extensions)]

    def generate_stats_file(self, target_files):
        with open("folder_code.txt", "w", encoding="utf-8") as out_file:
            for filepath in target_files:
                if not os.path.exists(filepath):
                    continue

                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    count = len(lines)
                    self.total_lines += count
                    self.file_stats.append((filepath, count))

                    out_file.write(f"\n\n--- Tên file: {filepath} ---\n\n")
                    out_file.writelines(lines)

        self.file_stats.sort(key=lambda x: x[1], reverse=True)

    def format_status(self, status):
        if status == "success":
            return "**Thành công**"
        if status == "failure":
            return "**Thất bại**"
        if status == "cancelled":
            return "**Đã hủy**"
        if status == "skipped":
            return "**Đã bỏ qua**"
        return f"Có lỗi xảy ra {status}"

    def create_markdown_report(self):
        repo = os.environ.get("GITHUB_REPOSITORY", "Repo không tồn tại")
        run_id = os.environ.get("GITHUB_RUN_ID", "Mã id chạy không hợp lệ")
        url = f"https://github.com/{repo}/actions/runs/{run_id}"
        backend_status = os.environ.get("BACKEND_LINT", "Không rõ")
        frontend_status = os.environ.get("FRONTEND_LINT", "Không rõ")
        backend_security_status = os.environ.get("BACKEND_SECURITY_CHECK", "Không rõ")
        frontend_security_status = os.environ.get("FRONTEND_SECURITY_CHECK", "Không rõ")
        docker_build_status = os.environ.get("DOCKER_BUILD_CHECK", "Không rõ")
        md_content = f"""## Báo cáo kiểm tra tĩnh

### 1. Trạng thái kiểm tra chung:
| Hạng mục | Kết quả |
|---|---|
| Kiểm tra format backend: | {self.format_status(backend_status)} |
| Kiểm tra format frontend: | {self.format_status(frontend_status)} |
| Kiểm tra bảo mật backend: | {self.format_status(backend_security_status)} |
| Kiểm tra bảo mật frontend: | {self.format_status(frontend_security_status)} |
| Kiểm tra build docker: | {self.format_status(docker_build_status)} |

*(Xem chi tiết: [link]({url}))*

---

### 2. Thống kê mã nguồn:
- **Tổng số file:** `{len(self.file_stats)}` files
- **Tổng số dòng code:** `{self.total_lines}` dòng

| Tên File | Số dòng |
|---|---|
"""

        for filepath, count in self.file_stats:
            if count > 500:
                md_content += f"| Cần xem lại: `{filepath}` | **{count}** |\n"
            else:
                md_content += f"| `{filepath}` | {count} |\n"

        with open("issue.md", "w", encoding="utf-8") as f:
            f.write(md_content)

    def run_pipeline(self):
        all_files = self.fetch_git_files()
        target_files = self.filter_files(all_files)
        self.generate_stats_file(target_files)
        self.create_markdown_report()

if __name__ == "__main__":
    static_report_scripts = StaticReportScripts()
    static_report_scripts.run_pipeline()