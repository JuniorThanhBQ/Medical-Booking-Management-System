import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { Navigate, Outlet } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";

export default function RoleRoute({ allowedRoles = [] }) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  if (!allowedRoles.includes(user?.role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
