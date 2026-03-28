import { Navigate, Outlet, useLocation } from "react-router-dom";
import { getStoredUser } from "@/utils/auth-helpers";

export default function RoleRoute({ allowedRoles }) {
  const user = getStoredUser();
  const location = useLocation();

  if (!user) {
    const returnUrl = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/auth?returnUrl=${returnUrl}`} replace />;
  }

  if (!allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
