import { Navigate, Outlet, useLocation } from "react-router-dom";

export default function RoleRoute({ allowedRoles }) {
  const user = localStorage.getItem("user");
  const location = useLocation();

  if (!user) {
    const returnUrl = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/auth?returnUrl=${returnUrl}`} replace />;
  }

  let role;
  try {
    role = JSON.parse(user).role;
  } catch {
    localStorage.removeItem("user");
    return <Navigate to="/auth" replace />;
  }

  if (!allowedRoles.includes(role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
