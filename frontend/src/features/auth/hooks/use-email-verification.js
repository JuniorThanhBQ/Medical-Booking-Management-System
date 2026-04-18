import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { toast } from "sonner";

import { verifyEmailToken } from "../services/auth-service";

export function useEmailVerification() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const navigate = useNavigate();

  const [status, setStatus] = useState(() => (token ? "loading" : "error"));
  const [message, setMessage] = useState(() =>
    token
      ? "Đang xác thực tài khoản của bạn..."
      : "Token không hợp lệ hoặc không được cung cấp.",
  );

  useEffect(() => {
    if (!token) return;

    let isMounted = true;

    const verifyAccount = async () => {
      try {
        const response = await verifyEmailToken(token);
        if (isMounted) {
          setStatus("success");
          setMessage(
            response.message ||
              "Tài khoản đã được kích hoạt thành công. Bạn có thể đăng nhập.",
          );
          toast.success("Xác thực tài khoản thành công!");
        }
      } catch (error) {
        if (isMounted) {
          setStatus("error");
          setMessage(
            error?.response?.data?.message ||
              "Liên kết xác thực không hợp lệ hoặc đã hết hạn.",
          );
          toast.error("Xác thực thất bại!");
        }
      }
    };

    verifyAccount();

    return () => {
      isMounted = false;
    };
  }, [token]);

  const handleNavigateLogin = () => navigate("/auth");
  const handleNavigateHome = () => navigate("/");

  return {
    status,
    message,
    handleNavigateLogin,
    handleNavigateHome,
  };
}
