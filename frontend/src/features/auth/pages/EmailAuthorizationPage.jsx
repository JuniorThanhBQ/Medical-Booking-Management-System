import "@/assets/css/auth/email-auth.css";

import EmailStep from "../components/EmailStep.jsx";
import PasswordStep from "../components/PasswordStep.jsx";
import ProfileStep from "../components/ProfileStep.jsx";
import { useEmailAuthorization } from "../hooks/useEmailAuthorization";

export default function EmailAuthorizationPage({
  role,
  onAuthenticated,
  onBackToRoleSelect,
}) {
  const {
    email,
    setEmail,
    authStep,
    mode,
    profile,
    setProfile,
    password,
    setPassword,
    loading,
    error,
    touchedEmail,
    setTouchedEmail,
    handleEmailSubmit,
    handleProfileSubmit,
    handlePasswordSubmit,
    handleChangeEmail,
    handleBack,
    title,
    subtitle,
  } = useEmailAuthorization({ role, onAuthenticated, onBackToRoleSelect });

  const stepForms = {
    profile: (
      <ProfileStep
        email={email}
        profile={profile}
        loading={loading}
        error={error}
        onProfileChange={(field, value) =>
          setProfile((prev) => ({ ...prev, [field]: value }))
        }
        onSubmit={handleProfileSubmit}
      />
    ),
    password: (
      <PasswordStep
        email={email}
        mode={mode}
        password={password}
        loading={loading}
        error={error}
        onPasswordChange={(e) => setPassword(e.target.value)}
        onChangeEmail={handleChangeEmail}
        onSubmit={handlePasswordSubmit}
      />
    ),
    email: (
      <EmailStep
        email={email}
        touchedEmail={touchedEmail}
        loading={loading}
        error={error}
        onEmailChange={(e) => {
          setEmail(e.target.value);
          setTouchedEmail(true);
        }}
        onBlur={() => setTouchedEmail(true)}
        onSubmit={handleEmailSubmit}
      />
    ),
  };

  return (
    <div className="auth-page">
      <header className="auth-page__header">
        <button type="button" className="auth-page__back" onClick={handleBack}>
          <span className="auth-page__back-icon">&#8592;</span>
        </button>
      </header>

      <main className="auth-page__main">
        <h1 className="auth-page__title">{title}</h1>
        <p className="auth-page__subtitle">{subtitle}</p>

        {stepForms[authStep] || stepForms.email}
      </main>
    </div>
  );
}
