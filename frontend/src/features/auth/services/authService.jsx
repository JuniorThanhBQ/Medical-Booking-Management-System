import Apis, { AuthApis, endpoints } from "@/configs/Apis";
import { clearAuth } from "@/repository/local-storage-repository";

export async function checkEmailExists(email) {
  try {
    await Apis.post(endpoints.auth_email_validator, { email });
    return false;
  } catch (err) {
    if (err.response?.status === 400) {
      return true;
    }
    throw err;
  }
}

export async function loginUser({ email, password, role }) {
  const res = await Apis.post(endpoints.auth_login, { email, password, role });
  return res.data;
}

export async function registerUser({ email, password, firstName, lastName, phone, dateOfBirth, gender }) {
  const payload = {
    email,
    password,
    firstName,
    lastName,
    phone,
    dayOfBirth: dateOfBirth,
    gender: gender ? gender.toUpperCase() : "",
  };
  const res = await Apis.post(endpoints.auth_register, payload);
  return res.data;
}

export async function getCurrentUser(token) {
  const res = await AuthApis(token).get(endpoints.auth_current_user);
  return res.data;
}

export async function loginWithGoogle(googleToken) {
  const res = await Apis.post(endpoints.auth_google_login, { google_token: googleToken });
  return res.data;
}

export function handleLogout() {
  clearAuth();
  window.location.href = "/";
}
