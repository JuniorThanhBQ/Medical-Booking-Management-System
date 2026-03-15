import axios from "axios";

export const BASE_URL = "";

export const endpoints = {
  login: "/o/token/",
  users: "/users/",
  users_detail: (user_id) => `/users/${user_id}/`,
  current_user: "/users/current-user/",
  auth_check_email: "/auth/check-email/",
  auth_login_password: "/auth/login-with-password/",
  auth_register: "/auth/register-with-profile/",
  // checking for available time slots by using derived query params: ?doctor_id=1&date=2024-06-30 / month=2024-06
  // if date is not provided, it will return all available time slots in that month,
  // appointments_available_slots: "/appointments/available-slots/",
  // appointments: "/appointments/",
};

const Apis = axios.create({
  baseURL: BASE_URL,
});

export const AuthApis = (token) =>
  axios.create({
    baseURL: BASE_URL,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

export default Apis;
