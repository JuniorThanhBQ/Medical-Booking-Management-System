import "@css/auth/email-verification.css";

import { useEmailVerification } from "@features/auth/hooks/use-email-verification";

export default function EmailVerificationPage() {
  const { status, message, handleNavigateLogin, handleNavigateHome } =
    useEmailVerification();

  return (
    <div className="verify-page-wrapper">
      <div className="verify-card">
        <div className={`verify-icon-container ${status}`}>
          {status === "loading" && <div className="verify-spinner"></div>}
          {status === "success" && (
            <span className="icon-success">&#10003;</span>
          )}
          {status === "error" && <span className="icon-error">&#10005;</span>}
        </div>

        <h1 className="verify-title">Trạng thái xác thực Email</h1>
        <p className={`verify-message ${status}`}>{message}</p>

        <div className="verify-actions">
          {status === "success" && (
            <button
              className="btn-verify-primary"
              onClick={handleNavigateLogin}
            >
              Đến trang đăng nhập
            </button>
          )}

          {status === "error" && (
            <button
              className="btn-verify-secondary"
              onClick={handleNavigateHome}
            >
              Về trang chủ
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
