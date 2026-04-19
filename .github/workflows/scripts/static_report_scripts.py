import os
import subprocess
import sys


class ComprehensiveReport:
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

    def run_pipeline(self):
        all_files = self.fetch_git_files()
        target_files = [f for f in all_files if any(f.endswith(ext) for ext in self.extensions)]

        for filepath in target_files:
            if not os.path.exists(filepath):
                continue
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                count = len(f.readlines())
                self.total_lines += count
                self.file_stats.append((filepath, count))

        self.file_stats.sort(key=lambda x: x[1], reverse=True)

        repo = os.environ.get("GITHUB_REPOSITORY", "Repo không tồn tại")
        run_id = os.environ.get("GITHUB_RUN_ID", "Mã id không hợp lệ")
        url = f"https://github.com/{repo}/actions/runs/{run_id}"

        def format_status(status):
            if status == "success": return "**Thành công**"
            if status == "failure": return "**Thất bại**"
            if status == "cancelled": return "**Đã hủy**"
            if status == "skipped": return "**Đã bỏ qua**"
            return "**Chưa chạy**"

        checks = {
            "Kiểm tra format Backend": os.environ.get("BACKEND_LINT"),
            "Kiểm tra format Frontend": os.environ.get("FRONTEND_LINT"),
            "Kiểm tra bảo mật Backend": os.environ.get("BACKEND_SECURITY"),
            "Kiểm tra bảo mật Frontend": os.environ.get("FRONTEND_SECURITY"),
            "Đánh giá Docker Static": os.environ.get("DOCKER_STATIC"),
            "Kiểm tra Pytest": os.environ.get("PYTEST_TEST"),
            "Build Integration Test": os.environ.get("TEST_BUILD"),
            "Build & Deploy Backend": os.environ.get("DEPLOY_BACKEND"),
            "Build & Deploy Frontend": os.environ.get("DEPLOY_FRONTEND"),
            "Kiểm tra Img Deploy": os.environ.get("CHECK_IMAGES")
        }

        md_content = f"## Báo Cáo CI/CD Tổng Hợp\n\n### 1. Trạng thái Pipeline\n| Hạng mục | Kết quả |\n|---|---|\n"
        for name, env_var in checks.items():
            md_content += f"| {name} | {format_status(env_var)} |\n"

        md_content += f"\n*(Xem log chi tiết tại: [Action Run]({url}))*\n\n---\n\n### 2. Thống kê Code\n"
        md_content += f"- **Tổng số file phân tích:** `{len(self.file_stats)}` files\n"
        md_content += f"- **Tổng số dòng code:** `{self.total_lines}` dòng\n\n"
        md_content += "| Tên File | Số dòng |\n|---|---|\n"

        for filepath, count in self.file_stats:
            prefix = "Cần xem lại: " if count > 500 else ""
            md_content += f"| {prefix}`{filepath}` | **{count}** |\n"

        with open("issue.md", "w", encoding="utf-8") as f:
            f.write(md_content)

if __name__ == "__main__":
    ComprehensiveReport().run_pipeline()
    