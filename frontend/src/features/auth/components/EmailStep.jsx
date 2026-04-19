import { isValidEmail } from "@utils/validation";

export default function EmailStep({
  email,
  touchedEmail,
  loading,
  error,
  onEmailChange,
  onBlur,
  onSubmit,
}) {
  const showError = touchedEmail && !isValidEmail(email);

  return (
    <form className="auth-form" onSubmit={onSubmit} noValidate>
      <div className="auth-field">
        <label className="auth-field__label" htmlFor="email_input">
          Email
        </label>
        <input
          id="email_input"
          className={`auth-field__input${showError ? " auth-field__input--error" : ""}`}
          type="email"
          inputMode="email"
          autoComplete="email"
          name="email"
          placeholder="name@example.com"
          value={email}
          onChange={onEmailChange}
          onBlur={onBlur}
          required
        />
        {showError && (
          <p className="auth-field__error" role="alert">
            Vui lòng nhập email hợp lệ.
          </p>
        )}
      </div>

      {error && (
        <p className="auth-field__error" role="alert">
          {error}
        </p>
      )}

      <button
        className="auth-form__submit"
        type="submit"
        disabled={loading || !email}
      >
        {loading ? "Đang kiểm tra..." : "Tiếp tục"}
      </button>
    </form>
  );
}
