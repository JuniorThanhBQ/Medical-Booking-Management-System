import { DEFAULT_MENU_ITEMS, DEFAULT_AUTH_MENU_ITEMS, DEFAULT_AUTH_NAV_LINKS, DEFAULT_NAV_LINKS } from "../configs/const";

export const getRoleMenuItems = () => {
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const role = user?.role;

  // eslint-disable-next-line security/detect-object-injection
  return DEFAULT_AUTH_MENU_ITEMS[role] || DEFAULT_MENU_ITEMS;
};

export const getRoleNavLinks = () => {
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const role = user?.role;

  // eslint-disable-next-line security/detect-object-injection
  return DEFAULT_AUTH_NAV_LINKS[role] || DEFAULT_NAV_LINKS;
};

export const normalizeQuery = (value) => value.trim().toLowerCase();

export const getAge = (dateOfBirth) => {
  if (!dateOfBirth) return null;
  const today = new Date();
  const birth = new Date(dateOfBirth);
  let age = today.getFullYear() - birth.getFullYear();
  const beforeBirthday =
    today.getMonth() < birth.getMonth() ||
    (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate());
  if (beforeBirthday) age -= 1;
  return age;
};