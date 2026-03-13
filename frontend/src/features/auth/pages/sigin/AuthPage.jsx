import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../hooks/useAuthStore";
import EmailAuthorizationPage from "./EmailAuthorizationPage";
import "../../../../css/auth-page.css";

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

  const { setRole } = useAuthStore.getState();
  const [selected, setSelected] = useState(null);

  const handleAuthenticated = (user) => {
    console.log(user);
    localStorage.setItem("token", user.token);
    navigate("/dashboard");
  };

  if (selected) {
    return <EmailAuthorizationPage onAuthenticated={handleAuthenticated} />;
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
              className={`signin-card${selected === option.id ? " signin-card--selected" : ""}`}
              onClick={() => {
                setSelected(option.id);
                setRole(option.id);
              }}
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
