import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../hooks/use-auth-store";
import EmailStep from "../../components/EmailStep";
import ProfileStep from "../../components/ProfileStep";
import PasswordStep from "../../components/PasswordStep";
import "@/assets/css/auth/email-authorization.css";
import { isValidEmail } from "../../utils/validation";
import users from "@/data/mocks/users";


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

  const matchedUserRef = useRef(null);

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
      const matchedUser = users.find(u => u.email.toLowerCase() === email.trim().toLowerCase());
      matchedUserRef.current = matchedUser;
      const exists = !!matchedUser;

      const nextMode = exists ? "login" : "register";
      setMode(nextMode);
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

    if (!password.trim()) {
      setError("Vui lòng nhập mật khẩu.");
      return;
    }

    try {
      setLoading(true);

      let result;
      if (mode === "login") {
        const matchedUser = matchedUserRef.current;
        if (!matchedUser || matchedUser.password !== password) {
          setError("Email hoặc mật khẩu không đúng.");
          return;
        }
        if (matchedUser.role.toLowerCase() !== role) {
          setError("Tài khoản không được đăng ký với role này.");
          return;
        }
        result = { token: "TOKEN AFTER LOGIN", user: matchedUser };
      } else {
        result = {
          token: "TOKEN AFTER REGISTER",
          user: {
            id: `usr_${Date.now()}`,
            firstName: profile.firstName,
            lastName: profile.lastName,
            name: `${profile.lastName} ${profile.firstName}`,
            email,
            phone: profile.phone,
            role: role === "patient" ? "Patient" : "Doctor",
            password,
          },
        };
      }
      onAuthenticated?.(result);
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

  const handleBack = () => {
    if (authStep === "email") return navigate("/auth");
    if (authStep === "profile") return handleChangeEmail();
    if (authStep === "password" && mode === "register") {
      setAuthStep("profile");
      setError("");
      return;
    }
    handleChangeEmail();
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
          onClick={handleBack}
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
