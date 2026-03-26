import { AuthApis, endpoints } from "@/configs/Apis";

export const createAppointment = async (token, payload) => {
  console.log("token", token);
  const res = await AuthApis(token).post(endpoints.appointments, payload);
  return res.data;
};
