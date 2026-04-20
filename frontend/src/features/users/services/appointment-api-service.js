import { endpoints } from "@/configs/apis";

export const getAppointments = async (api, params = {}) => {
  const res = await api.get(endpoints.appointments, { params });
  return res.data;
};

export const getAppointmentDetail = async (api, appointmentId) => {
  const res = await api.get(`${endpoints.appointments}/${appointmentId}`);
  return res.data;
};

export const getMedicalRecordDetail = async (api, medicalRecordId) => {
  const res = await api.get(endpoints.medical_record_detail(medicalRecordId));
  return res.data;
};
