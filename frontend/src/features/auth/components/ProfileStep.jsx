export default function ProfileStep({
  email,
  profile,
  loading,
  error,
  onProfileChange,
  onSubmit,
}) {
  return (
    <form className="auth-form" onSubmit={onSubmit} noValidate>
      <div className="auth-field">
        <label className="auth-field__label">Email</label>
        <input
          className="auth-field__input"
          type="email"
          value={email}
          disabled
        />
      </div>

      <div className="auth-field">
        <label className="auth-field__label">Họ</label>
        <input
          className="auth-field__input"
          type="text"
          value={profile.lastName}
          onChange={(e) => onProfileChange("lastName", e.target.value)}
          required
        />
      </div>

      <div className="auth-field">
        <label className="auth-field__label">Tên</label>
        <input
          className="auth-field__input"
          type="text"
          value={profile.firstName}
          onChange={(e) => onProfileChange("firstName", e.target.value)}
          required
        />
      </div>

      <div className="auth-field">
        <label className="auth-field__label">Số điện thoại</label>
        <input
          className="auth-field__input"
          type="tel"
          value={profile.phone}
          onChange={(e) => onProfileChange("phone", e.target.value)}
          required
        />
      </div>

      <div className="auth-field">
        <label className="auth-field__label">Ngày sinh</label>
        <input
          className="auth-field__input"
          type="date"
          value={profile.dateOfBirth}
          onChange={(e) => onProfileChange("dateOfBirth", e.target.value)}
          required
        />
      </div>

      <div className="auth-field">
        <label className="auth-field__label">Giới tính</label>
        <select
          className="auth-field__input"
          value={profile.gender}
          onChange={(e) => onProfileChange("gender", e.target.value)}
          required
        >
          <option value="">Chọn giới tính</option>
          <option value="male">Nam</option>
          <option value="female">Nữ</option>
          <option value="other">Khác</option>
        </select>
      </div>

      {error && (
        <p className="auth-field__error" role="alert">
          {error}
        </p>
      )}

      <button className="auth-form__submit" type="submit" disabled={loading}>
        {loading ? "Đang xử lý..." : "Tiếp tục"}
      </button>
    </form>
  );
}
