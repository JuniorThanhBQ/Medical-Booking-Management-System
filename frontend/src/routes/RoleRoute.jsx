import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

export default function RoleRoute({ allowedRoles = [] }) {
  const { user, isAuthenticated, isLoading } = useAuth();


  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        toast.info("Vui lòng đăng nhập để tiếp tục.");
      }
      else if (!allowedRoles.includes(user?.role)) {
        toast.error("Bạn không có quyền truy cập trang này.");
      }
    }
  }, [isLoading, isAuthenticated, user?.role, allowedRoles]);


  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner fullPage label="Đang tải trang..." />
      </div>
    );
  }


  if (!allowedRoles.includes(user?.role)) {
    return <Navigate to="/" replace />;
  }


  return <Outlet />;
}
