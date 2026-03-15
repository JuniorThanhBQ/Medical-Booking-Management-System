import { DEFAULT_MENU_ITEMS, DEFAULT_AUTH_MENU_ITEMS } from "../configs/const";

export const getRoleMenuItems = () => {
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const role = user?.role;
  console.log("role", role);

  // Lỗi eslint được đánh dấu ngày 15/03/2026
  // eslint-disable-next-line security/detect-object-injection
  return DEFAULT_AUTH_MENU_ITEMS[role] || DEFAULT_MENU_ITEMS;
};
