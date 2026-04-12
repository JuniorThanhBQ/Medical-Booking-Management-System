import { getStoredUserRole } from "./auth-helpers";
import { DEFAULT_MENU_ITEMS, DEFAULT_AUTH_MENU_ITEMS, 
  DEFAULT_AUTH_NAV_LINKS, DEFAULT_NAV_LINKS, OPEN_HOURS } from "@configs/const";

export function generateTimeOptions() {
  const options = [];
  for (let hour = OPEN_HOURS.start; hour <= OPEN_HOURS.end; hour += 1) {
    options.push(`${String(hour).padStart(2, "0")}:00`);
    options.push(`${String(hour).padStart(2, "0")}:30`);
  }
  return options;
}

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
  if (!dateOfBirth) 
    return null;

  const today = new Date();
  const birth = new Date(dateOfBirth);
  const beforeBirthday = today.getMonth() < birth.getMonth() ||
    (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate());
  let age = today.getFullYear() - birth.getFullYear();
  if (beforeBirthday) 
    age -= 1;

  return age;
};