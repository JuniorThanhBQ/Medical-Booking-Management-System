import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { useEffect } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

export default function PrivateRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      toast.info("Vui lòng đăng nhập để truy cập trang này.");
    }
  }, [isLoading, isAuthenticated]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner fullPage label="Đang tải trang..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    const returnUrl = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/auth?returnUrl=${returnUrl}`} replace />;
  }

  return <Outlet />;
}
