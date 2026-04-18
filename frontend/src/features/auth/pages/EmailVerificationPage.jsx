import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { verifyEmailToken } from "../services/auth-service"; 
export default function EmailVerificationPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const navigate = useNavigate();
  
  const [status, setStatus] = useState("loading"); // 'loading' | 'success' | 'error'
  const [message, setMessage] = useState("Đang tiến hành xác thực tài khoản của bạn...");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Token không hợp lệ hoặc không được cung cấp.");
      return;
    }

    const verifyAccount = async () => {
      try {
        // Gọi API xuống backend
        const response = await verifyEmailToken(token);
        
        setStatus("success");
        setMessage(response.message || "Tài khoản đã được kích hoạt thành công. Bạn có thể đăng nhập.");
        toast.success("Xác thực tài khoản thành công!");
        
      } catch (error) {
        setStatus("error");
        setMessage(
          error?.response?.data?.message ||
          "Liên kết xác thực không hợp lệ hoặc đã hết hạn."
        );
        toast.error("Xác thực thất bại!");
      }
    };

    verifyAccount();
  }, [token]);

  return (
    <div className="auth-page" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
      <div className="auth-page__main" style={{ textAlign: 'center', padding: '40px', maxWidth: '500px' }}>
        <h1 className="auth-page__title">Xác thực Email</h1>
        
        {status === "loading" && (
          <p className="auth-page__subtitle">{message}</p>
        )}
        
        {status === "success" && (
          <>
            <p style={{ color: 'green', marginBottom: '20px' }}>{message}</p>
            <button 
              className="btn-primary" // Tùy chỉnh class theo CSS của bạn
              onClick={() => navigate("/auth")}
            >
              Đến trang đăng nhập
            </button>
          </>
        )}
        
        {status === "error" && (
          <>
            <p style={{ color: 'red', marginBottom: '20px' }}>{message}</p>
            <button 
              className="btn-secondary" // Tùy chỉnh class theo CSS của bạn
              onClick={() => navigate("/")}
            >
              Về trang chủ
            </button>
          </>
        )}
      </div>
    </div>
  );
}