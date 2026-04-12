import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../hooks/use-auth-store.js";
import { setToken, setUser, getUser } from "@/repository/local-storage-repository";
import EmailAuthorizationPage from "./EmailAuthorizationPage.jsx";
import "@/assets/css/auth/auth-page.css";

const OPTIONS = [
  {
    id: "patient",
    title: "Dành cho bệnh nhân",
    description: "Đặt lịch hẹn và tra cứu hồ sơ y tế",
  },
  {
    id: "doctor",
    title: "Dành cho bác sĩ",
    description: "Đăng ký và tra cứu hồ sơ y tế",
  },
];

export default function AuthPage() {
  const navigate = useNavigate();

  const { role, setRole } = useAuthStore();

  const handleAuthenticated = (data) => {
    setToken(data.token);
    setUser(data.user.user);

    const user = getUser();

    const searchParams = new URLSearchParams(window.location.search);
    const returnUrl = searchParams.get("returnUrl");

    if (returnUrl && returnUrl.startsWith("/") && !returnUrl.startsWith("//")) {
      navigate(returnUrl, { replace: true });
    } else {
      const isDoctor = user.role === "DOCTOR";
      navigate(isDoctor ? "/doctor/today" : "/dashboard", { replace: true });
    }
  };

  if (role) {
    return (
      <EmailAuthorizationPage
        onAuthenticated={handleAuthenticated}
        onBackToRoleSelect={() => setRole(null)}
      />
    );
  }

  return (
    <div className="signin-page">
      <header className="signin-page__header">
        <button
          type="button"
          className="signin-page__back"
          onClick={() => navigate("/")}
        >
          <span className="signin-page__back-icon">&#8592;</span>
        </button>
      </header>

      <main className="signin-page__main">
        <h1 className="signin-page__title">Đăng ký/đăng nhập</h1>

        <div className="signin-page__cards">
          {OPTIONS.map((option) => (
            <button
              key={option.id}
              type="button"
              className={`signin-card${role === option.id ? " signin-card--selected" : ""}`}
              onClick={() => setRole(option.id)}
            >
              <div className="signin-card__text">
                <div className="signin-card__title">{option.title}</div>
                <div className="signin-card__description">
                  {option.description}
                </div>
              </div>
              <span className="signin-card__chevron">→</span>
            </button>
          ))}
        </div>
      </main>

      <footer className="signin-page__footer">
        <button type="button" className="signin-footer__link">
          <span className="signin-footer__icon">?</span>
          Trợ giúp và hỗ trợ
        </button>
      </footer>
    </div>
  );
}
