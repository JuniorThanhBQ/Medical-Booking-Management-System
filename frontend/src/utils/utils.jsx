import { DEFAULT_MENU_ITEMS, DEFAULT_AUTH_MENU_ITEMS, DEFAULT_AUTH_NAV_LINKS, DEFAULT_NAV_LINKS } from "../configs/const";
import { getStoredUserRole } from "./auth-helpers";

export const getRoleMenuItems = () => {
  const role = getStoredUserRole();

  return DEFAULT_AUTH_MENU_ITEMS[role] || DEFAULT_MENU_ITEMS;
};

export const getRoleNavLinks = () => {
  const role = getStoredUserRole();

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