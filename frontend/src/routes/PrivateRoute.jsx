import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { Navigate, Outlet, useLocation } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";

export default function PrivateRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  if (!isAuthenticated) {
    const returnUrl = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/auth?returnUrl=${returnUrl}`} replace />;
  }

  return <Outlet />;
}
