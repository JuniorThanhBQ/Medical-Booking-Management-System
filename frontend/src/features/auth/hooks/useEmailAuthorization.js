import { useEffect } from "react";

import { useAuthFlow } from "./useAuthFlow";

const getAuthPageMeta = (authStep, mode, role) => {
  const roleMap = {
    doctor: "bác sĩ",
    patient: "bệnh nhân",
  };

  const roleLabel = roleMap[role] || "lễ tân";

  if (authStep === "email") {
    return {
      title: "Xác thực",
      subtitle: role
        ? `Tiếp tục với vai trò ${roleLabel}. Nhập email để tiếp tục.`
        : "Nhập email để tiếp tục.",
    };
  }
  if (mode === "login") {
    return {
      title: "Chào mừng trở lại",
      subtitle: "Nhập mật khẩu để tiếp tục.",
    };
  }
  return {
    title: "Hoàn tất hồ sơ của bạn",
    subtitle: "Thêm một vài thông tin để tạo tài khoản mới.",
  };
};

export function useEmailAuthorization(props) {
  const authState = useAuthFlow(props);
  const { resetAuthFlow } = authState;

  useEffect(() => {
    resetAuthFlow();
  }, [resetAuthFlow]);

  const { title, subtitle } = getAuthPageMeta(
    authState.authStep,
    authState.mode,
    props.role,
  );

  return {
    ...authState,
    title,
    subtitle,
  };
}
