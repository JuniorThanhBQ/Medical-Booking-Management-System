export default function PasswordStep({
  email,
  mode,
  password,
  loading,
  error,
  onPasswordChange,
  onChangeEmail,
  onSubmit,
}) {
  return (
    <form className="auth-form" onSubmit={onSubmit} noValidate>
      <div className="auth-field">
        <label className="auth-field__label">Email</label>
        <div>
          <div style={{ fontSize: "0.9rem", marginBottom: 4 }}>{email}</div>
          <button
            type="button"
            onClick={onChangeEmail}
            style={{
              border: "none",
              background: "transparent",
              padding: 0,
              fontSize: "0.8rem",
              color: "#4f46e5",
              cursor: "pointer",
            }}
          >
            Thay đổi email
          </button>
        </div>
      </div>

      <div className="auth-field">
        <label className="auth-field__label">
          {mode === "login" ? "Mật khẩu" : "Tạo mật khẩu"}
        </label>
        <input
          className="auth-field__input"
          type="password"
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          value={password}
          onChange={onPasswordChange}
          required
        />
        {mode !== "login" && (
          <p
            className="auth-field__hint"
            style={{ fontSize: "0.75rem", color: "#6b7280", marginTop: 4 }}
          >
            Tối thiểu 9 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt
          </p>
        )}
      </div>

      {error && (
        <p className="auth-field__error" role="alert">
          {error}
        </p>
      )}

      <button className="auth-form__submit" type="submit" disabled={loading}>
        {loading
          ? "Đang xử lý..."
          : mode === "login"
            ? "Đăng nhập"
            : "Tạo tài khoản"}
      </button>
    </form>
  );
}
