import "@/assets/css/auth/auth-page.css";

import { OPTIONS } from "@configs/const";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { AuthFooter } from "../components/AuthFooter";
import { AuthHeader } from "../components/AuthHeader";
import { RoleCard } from "../components/RoleCard";
import { useAuthRedirect } from "../hooks/use-auth-redirect";
import { useRoleSelection } from "../hooks/use-role-selection";
import EmailAuthorizationPage from "./EmailAuthorizationPage.jsx";

export default function AuthPage() {
  const navigate = useNavigate();
  const { role, setRole, resetRole } = useRoleSelection();
  const { handleAuthenticated } = useAuthRedirect();

  const handleRoleSelect = (selectedRole) => {
    const selectedOption = OPTIONS.find((option) => option.id === selectedRole);
    toast.success(`${selectedOption?.title || selectedRole} đã được chọn.`);
    setRole(selectedRole);
  };

  if (role) {
    return (
      <EmailAuthorizationPage
        role={role}
        onAuthenticated={handleAuthenticated}
        onBackToRoleSelect={resetRole}
      />
    );
  }

  return (
    <div className="signin-page">
      <AuthHeader onBack={() => navigate("/")} />

      <main className="signin-page__main">
        <h1 className="signin-page__title">Đăng nhập và đăng ký</h1>
        <div className="signin-page__cards">
          {OPTIONS.map((option) => (
            <RoleCard
              key={option.id}
              option={option}
              isSelected={role === option.id}
              onSelect={handleRoleSelect}
            />
          ))}
        </div>
      </main>

      <AuthFooter />
    </div>
  );
}
