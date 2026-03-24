import axios from "axios";

export const BASE_URL = "http://localhost:8000";

export const endpoints = {
  auth_login: "/api/v1/auth/login",
  auth_register: "/api/v1/auth/register",
  auth_google_login: "/api/v1/auth/google-login",
  auth_current_user: "/api/v1/auth/current-user",
  auth_email_validator: "/api/v1/auth/email-validator",
  public_specialties: "/api/v1/public/specialties",
  public_doctors: "/api/v1/public/doctors",
  public_doctor_detail: (id) => `/api/v1/public/doctors/${id}`,
  public_doctor_time_slots: (id) => `/api/v1/public/doctors/${id}/time-slots`,
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
