import Apis from "../../../configs/Apis";

// export async function checkEmailExists(email) {
//   const response = await Apis.post(endpoints.auth_check_email, { email });
//   return response.data;
// }

// export async function loginWithPassword({ email, password }) {
//   const response = await Apis.post(endpoints.auth_login_password, {
//     email,
//     password,
//   });
//   return response.data;
// }

// export async function registerWithProfile(payload) {
//   const response = await Apis.post(endpoints.auth_register, payload);
//   return response.data;
// }

export function handleLogout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "/";
}