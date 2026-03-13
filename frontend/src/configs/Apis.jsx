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
