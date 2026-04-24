import {
  containsXss,
  getPasswordErrors,
  isValidDateOfBirth,
  isValidEmail,
  isValidGender,
  isValidName,
  isValidPhone,
} from "@utils/validation.js";
import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

import { verifyEmailStatus } from "../services/auth-service";

const validateProfile = (profile) => {
  if (!isValidName(profile.firstName))
    return containsXss(profile.firstName)
      ? "Tên chứa ký tự không hợp lệ."
      : "Tên phải có ít nhất 2 ký tự.";
  if (!isValidName(profile.lastName))
    return containsXss(profile.lastName)
      ? "Họ chứa ký tự không hợp lệ."
      : "Họ phải có ít nhất 2 ký tự.";
  if (!isValidPhone(profile.phone))
    return containsXss(profile.phone)
      ? "Số điện thoại chứa ký tự không hợp lệ."
      : "Số điện thoại phải có ít nhất 10 ký tự.";
  if (!isValidDateOfBirth(profile.dateOfBirth))
    return "Vui lòng chọn ngày sinh hợp lệ.";
  if (!isValidGender(profile.gender)) return "Vui lòng chọn giới tính.";

  return null;
};

const validatePassword = (mode, password) => {
  if (mode === "register") {
    const passwordErrors = getPasswordErrors(password);
    return passwordErrors.length > 0
      ? `Mật khẩu không hợp lệ: ${passwordErrors.join(", ")}`
      : null;
  }
  return !password.trim() ? "Vui lòng nhập mật khẩu." : null;
};

const handleAuth = async ({
  mode,
  email,
  password,
  profile,
  role,
  login,
  register,
}) => {
  let result;

  if (mode === "register") {
    result = await register(
      email,
      password,
      profile.firstName,
      profile.lastName,
      profile.phone,
      profile.dateOfBirth,
      profile.gender,
    );
    if (!result.success) throw new Error(result.message);
    return result;
  }

  result = await login(email, password, role);
  if (!result.success) throw new Error(result.message);

  return result;
};

const processEmailCheck = async (email, role) => {
  if (!isValidEmail(email)) return null;

  const { data } = await verifyEmailStatus(email);
  const isStaffRole = role === "doctor" || role === "receptionist";
  if (isStaffRole) {
    if (!data) {
      throw new Error("Email không tồn tại. Vui lòng kiểm tra lại.");
    }
    if (data?.role !== role.toUpperCase()) {
      throw new Error("Vui lòng sử dụng tài khoản được cung cấp bởi admin.");
    }
  } else {
    if (data?.isExisted && data?.role !== role.toUpperCase()) {
      throw new Error("Tài khoản không hợp lệ");
    }
  }

  return {
    nextMode: data?.isExisted ? "login" : "register",
    nextStep: data?.isExisted ? "password" : "profile",
  };
};

const resolveErrorMessage = (err) => {
  return (
    err?.response?.data?.message ||
    err.message ||
    "Đã xảy ra lỗi. Vui lòng thử lại."
  );
};

export function useAuthFlow({ role, onAuthenticated, onBackToRoleSelect }) {
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const [email, setEmail] = useState("");
  const [authStep, setAuthStep] = useState("email");
  const [mode, setMode] = useState(null);
  const [profile, setProfile] = useState({
    firstName: "",
    lastName: "",
    phone: "",
    dateOfBirth: "",
    gender: "",
  });
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [touchedEmail, setTouchedEmail] = useState(false);

  const resetAuthFlow = useCallback(() => {
    setEmail("");
    setAuthStep("email");
    setMode(null);
    setProfile({
      firstName: "",
      lastName: "",
      phone: "",
      dateOfBirth: "",
      gender: "",
    });
    setPassword("");
    setLoading(false);
    setError("");
    setTouchedEmail(false);
  }, []);

  const handleChangeEmail = () => {
    setMode(null);
    setPassword("");
    setError("");
    setTouchedEmail(false);
    setAuthStep("email");
  };

  const handleEmailSubmit = async (event) => {
    event.preventDefault();
    setTouchedEmail(true);
    setError("");

    try {
      setLoading(true);
      const result = await processEmailCheck(email, role);
      if (result) {
        setMode(result.nextMode);
        setAuthStep(result.nextStep);
        toast.success(
          `Vui lòng thực hiện ${
            result.nextMode === "login" ? "đăng nhập" : "đăng ký"
          }.`,
        );
      }
    } catch (err) {
      const message =
        err.message || "Không thể kiểm tra email. Vui lòng thử lại.";
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const handleProfileSubmit = (event) => {
    event.preventDefault();
    const validationError = validateProfile(profile);
    setError(validationError || "");
    if (validationError) {
      toast.error(validationError);
      return;
    }

    toast.success("Thông tin hồ sơ hợp lệ. Tiếp tục tạo mật khẩu.");
    setAuthStep("password");
  };

  const handlePasswordSubmit = async (event) => {
    event.preventDefault();
    const passwordError = validatePassword(mode, password);
    if (passwordError) {
      toast.error(passwordError);
      return setError(passwordError);
    }

    try {
      setLoading(true);
      const result = await handleAuth({
        mode,
        email,
        password,
        profile,
        role,
        login,
        register,
      });

      if (mode === "register") {
        toast.success(
          "Đăng ký thành công! Vui lòng kiểm tra mail để xác thực tài khoản.",
        );
        resetAuthFlow();
        return;
      }

      toast.success("Đăng nhập thành công!");
      onAuthenticated?.({ token: null, user: result?.user ?? null });
    } catch (err) {
      const message = resolveErrorMessage(err);
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    const goBackToRole = onBackToRoleSelect || (() => navigate("/auth"));
    const goToProfile = () => {
      setAuthStep("profile");
      setError("");
    };

    const backActions = {
      email: goBackToRole,
      profile: handleChangeEmail,
      password: mode === "register" ? goToProfile : handleChangeEmail,
    };

    const action = backActions[authStep];
    if (action) action();
  };

  return {
    email,
    setEmail,
    authStep,
    setAuthStep,
    mode,
    profile,
    setProfile,
    password,
    setPassword,
    loading,
    error,
    touchedEmail,
    setTouchedEmail,
    resetAuthFlow,
    handleEmailSubmit,
    handleProfileSubmit,
    handlePasswordSubmit,
    handleChangeEmail,
    handleBack,
  };
}
