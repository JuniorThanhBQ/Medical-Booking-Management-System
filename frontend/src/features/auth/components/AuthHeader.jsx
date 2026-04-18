export function AuthHeader({ onBack }) {
  return (
    <header className="signin-page__header">
      <button type="button" className="signin-page__back" onClick={onBack}>
        <span className="signin-page__back-icon">&#8592;</span>
        <span className="signin-page__back-text">Quay lại</span>
      </button>
    </header>
  );
}
