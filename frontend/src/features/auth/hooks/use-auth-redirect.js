import { useNavigate } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";
export function useAuthRedirect() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleAuthenticated = () => {
    const searchParams = new URLSearchParams(window.location.search);
    const returnUrl = searchParams.get("returnUrl");

    if (returnUrl && returnUrl.startsWith("/") && !returnUrl.startsWith("//")) {
      navigate(returnUrl, { replace: true });
    } else if (user?.role === "DOCTOR") {
      navigate("/doctor/today", { replace: true });
    } else if (user?.role === "RECEPTIONIST") {
      navigate("/receptionist/appointments", { replace: true });
    } else {
      navigate("/dashboard", { replace: true });
    }
  };

  return { handleAuthenticated };
}
