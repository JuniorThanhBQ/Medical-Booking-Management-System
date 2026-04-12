import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../hooks/use-auth-store.js";
import EmailStep from "../components/EmailStep.jsx";
import ProfileStep from "../components/ProfileStep.jsx";
import PasswordStep from "../components/PasswordStep.jsx";
import "@/assets/css/auth/email-authorization.css";
import {
  isValidEmail, isValidName, isValidPhone,
  isValidDateOfBirth, isValidGender,
  getPasswordErrors, containsXss,
} from "../../../utils/validation.jsx";
import { checkEmailExists, loginUser, registerUser, getCurrentUser } from "../services/authService.jsx";

function getAuthPageMeta(authStep, mode, role) {
  if (authStep === "email") return {
    title: "Xác thực",
    subtitle: role ? `Tiếp tục với vai trò ${role}. Nhập email để tiếp tục.` : "Nhập email để tiếp tục.",
  };
  if (mode === "login") return { title: "Chào mừng trở lại", subtitle: "Nhập mật khẩu để tiếp tục." };
  return { title: "Hoàn tất hồ sơ của bạn", subtitle: "Thêm một vài thông tin để tạo tài khoản mới." };
}

export default function EmailAuthorizationPage({ onAuthenticated }) {
  const navigate = useNavigate();
  const { role, email, authStep, mode, profile, password, loading, error, touchedEmail, setEmail, setAuthStep,
    setMode, setProfile, setPassword, setError, setLoading, setTouchedEmail, resetAuthFlow } = useAuthStore();

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
      const exists = await checkEmailExists(email);
      if (role === "doctor" && !exists) {
        setError("Email không tồn tại. Tài khoản bác sĩ do quản trị viên cung cấp.");
        return;
      }
      setMode(exists ? "login" : "register");
      setAuthStep(exists ? "password" : "profile");
    } catch (err) {
      console.log("err", err)
      setError("Không thể kiểm tra email. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  };

  const handleProfileSubmit = (event) => {
    event.preventDefault();
    setError("");

    if (!isValidName(profile.firstName)) {
      setError(containsXss(profile.firstName) ? "Tên chứa ký tự không hợp lệ." : "Tên phải có ít nhất 2 ký tự.");
      return;
    }
    if (!isValidName(profile.lastName)) {
      setError(containsXss(profile.lastName) ? "Họ chứa ký tự không hợp lệ." : "Họ phải có ít nhất 2 ký tự.");
      return;
    }
    if (!isValidPhone(profile.phone)) {
      setError(containsXss(profile.phone) ? "Số điện thoại chứa ký tự không hợp lệ." : "Số điện thoại phải có ít nhất 10 ký tự.");
      return;
    }
    if (!isValidDateOfBirth(profile.dateOfBirth)) {
      setError("Vui lòng chọn ngày sinh hợp lệ.");
      return;
    }
    if (!isValidGender(profile.gender)) {
      setError("Vui lòng chọn giới tính.");
      return;
    }
    setAuthStep("password");
  };

  const handlePasswordSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (mode === "register") {
      const pwErrors = getPasswordErrors(password);
      if (pwErrors.length > 0) {
        setError("Mật khẩu không hợp lệ: " + pwErrors.join(", "));
        return;
      }
    } else if (!password.trim()) {
      setError("Vui lòng nhập mật khẩu.");
      return;
    }

    try {
      setLoading(true);
      if (mode !== "login") await registerUser({ email, password, ...profile });
      const loginRes = await loginUser({ email, password, role });
      const userRes = await getCurrentUser(loginRes.access_token);
      onAuthenticated?.({ token: loginRes.access_token, user: userRes });
    } catch (err) {
      console.log("err", err)
      const msg = err?.response?.data?.message;
      setError(msg || "Không thể tiếp tục. Vui lòng kiểm tra thông tin và thử lại.");
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

  const { title, subtitle } = getAuthPageMeta(authStep, mode, role);

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
