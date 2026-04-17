const FIELDS = [
  { label: "Họ", key: "lastName", type: "text" },
  { label: "Tên", key: "firstName", type: "text" },
  { label: "Số điện thoại", key: "phone", type: "tel" },
  { label: "Ngày sinh", key: "dateOfBirth", type: "date" },
];

const GENDER_OPTIONS = [
  { value: "male", label: "Nam" },
  { value: "female", label: "Nữ" },
  { value: "other", label: "Khác" },
];

export default function ProfileStep({
  email,
  profile,
  loading,
  error,
  onProfileChange,
  onSubmit,
}) {
  const renderField = (field) => (
    <div className="auth-field" key={field.key}>
      <label className="auth-field__label">{field.label}</label>
      <input
        className="auth-field__input"
        type={field.type}
        value={profile[field.key]}
        onChange={(e) => onProfileChange(field.key, e.target.value)}
        required
      />
    </div>
  );

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

      {FIELDS.map(renderField)}

      <div className="auth-field">
        <label className="auth-field__label">Giới tính</label>
        <select
          className="auth-field__input"
          value={profile.gender}
          onChange={(e) => onProfileChange("gender", e.target.value)}
          required
        >
          <option value="">Chọn giới tính</option>
          {GENDER_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
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
