import { AuthApis, endpoints } from "@/configs/Apis";

export const createAppointment = async (token, payload) => {
  console.log("token", token);
  console.log("payload", payload);
  console.log("url", endpoints.appointments);
  const res = await AuthApis(token).post(endpoints.appointments, payload);
  return res.data;
};

export const getAppointments = async (token, params = {}) => {
  const res = await AuthApis(token).get(endpoints.appointments, { params });
  return res.data;
};

export const getAppointmentDetail = async (token, appointmentId) => {
  const res = await AuthApis(token).get(`${endpoints.appointments}/${appointmentId}`);
  return res.data;
};

export const getMedicalRecordDetail = async (token, medicalRecordId) => {
  const res = await AuthApis(token).get(`/api/v1/medical-records/${medicalRecordId}`);
  return res.data;
};
