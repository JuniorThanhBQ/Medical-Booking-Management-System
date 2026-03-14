import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../hooks/useAuthStore";
// import { checkEmailExists, loginWithPassword, registerWithProfile } from '../../../configs/Apis.jsx'
import EmailStep from "../../components/EmailStep";
import ProfileStep from "../../components/ProfileStep";
import PasswordStep from "../../components/PasswordStep";
import "../../../../css/email-authorization.css";
import { isValidEmail, isValidPassword } from "../../utils/validation";
import { ROLE } from "../../../../configs/const";


export default function EmailAuthorizationPage({ onAuthenticated }) {
  const navigate = useNavigate();

  const {
    role,
    email,
    authStep,
    mode,
    profile,
    password,
    loading,
    error,
    touchedEmail,
    setAuthMode,
    setEmail,
    setAuthStep,
    setMode,
    setProfile,
    setPassword,
    setError,
    setLoading,
    setTouchedEmail,
    resetAuthFlow,
  } = useAuthStore();

  useEffect(() => {
    resetAuthFlow();
  }, [resetAuthFlow]);

  const handleEmailSubmit = async (event) => {
    event.preventDefault();
    setTouchedEmail(true);
    setError("");

    if (!isValidEmail(email)) return;

    try {
      setLoading(true);
      // const result = await checkEmailExists(email)
      const exists = true;

      const nextMode = exists ? "login" : "register";
      setMode(nextMode);
      setAuthMode(nextMode);
      setEmail(email);

      setAuthStep(exists ? "password" : "profile");
    } catch (err) {
      console.error("checkEmail error", err);
      setError("Không thể kiểm tra email. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  };

  const handleProfileSubmit = (event) => {
    event.preventDefault();
    setError("");

    if (!profile.firstName || !profile.lastName || !profile.phone) {
      setError("Vui lòng điền đầy đủ thông tin bắt buộc.");
      return;
    }

    setAuthStep("password");
  };

  const handlePasswordSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!isValidPassword(password)) {
      setError("Mật khẩu cần ít nhất 6 ký tự.");
      return;
    }

    try {
      setLoading(true);

      if (mode === "login") {
        // const result = await loginWithPassword({ email, password })
        if (onAuthenticated) {
          onAuthenticated({
            token: "TOKEN AFTER LOGIN",
            user: {
              role: ROLE.Patient,
              email,
            },
          });
        }
      } else {
        const payload = {
          email,
          password,
          first_name: profile.firstName,
          last_name: profile.lastName,
          phone: profile.phone,
          date_of_birth: profile.dateOfBirth,
          gender: profile.gender,
          role,
        };
        // const result = await registerWithProfile(payload)
        if (onAuthenticated) {
          onAuthenticated({
            token: "TOKEN AFTER REGISTER",
            user: {
              role: ROLE.Patient,
              email,
            },
          });
        }
      }
    } catch (err) {
      console.error("password submit error", err);
      setError("Không thể tiếp tục. Vui lòng kiểm tra thông tin và thử lại.");
    } finally {
      setLoading(false);
    }
  };

  const handleChangeEmail = () => {
    setMode(null);
    setPassword("");
    setError("");
    setTouchedEmail(false);
    setAuthStep("email");
  };

  const title =
    authStep === "email"
      ? "Xác thực"
      : mode === "login"
        ? "Chào mừng trở lại"
        : "Hoàn tất hồ sơ của bạn";

  const subtitle =
    authStep === "email"
      ? role
        ? `Tiếp tục với vai trò ${role}. Nhập email để tiếp tục.`
        : "Nhập email để tiếp tục."
      : mode === "login"
        ? "Nhập mật khẩu để tiếp tục."
        : "Thêm một vài thông tin để tạo tài khoản mới.";

  const renderStepForm = () => {
    if (authStep === "profile") {
      return (
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
      );
    }
    if (authStep === "password") {
      return (
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
      );
    }
    return (
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
    );
  };

  return (
    <div className="auth-page">
      <header className="auth-page__header">
        <button
          type="button"
          className="auth-page__back"
          onClick={() => navigate("/auth")}
        >
          <span className="auth-page__back-icon">&#8592;</span>
        </button>
      </header>

      <main className="auth-page__main">
        <h1 className="auth-page__title">{title}</h1>
        <p className="auth-page__subtitle">{subtitle}</p>

        {renderStepForm()}
      </main>
    </div>
  );
}
