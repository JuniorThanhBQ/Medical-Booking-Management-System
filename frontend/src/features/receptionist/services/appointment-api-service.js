import { endpoints } from "@/configs/apis";

export const getReceptionistAppointments = async (api) => {
  const res = await api.get(endpoints.appointment_by_receptionist);
  return res.data;
};

export const createReceptionistAppointment = async (api, payload) => {
  const res = await api.post(endpoints.appointment_by_receptionist, payload);
  return res.data;
};

export const getAllAppointments = async (api, params = {}) => {
  const res = await api.get(endpoints.appointments, { params });
  return res.data;
};

export const getAppointmentDetail = async (api, appointmentId) => {
  const res = await api.get(endpoints.appointment_detail(appointmentId));
  return res.data;
};

export const updateAppointment = async (api, appointmentId, payload) => {
  const res = await api.patch(
    endpoints.appointment_detail(appointmentId),
    payload,
  );
  return res.data;
};

export const deleteAppointment = async (api, appointmentId) => {
  const res = await api.delete(endpoints.appointment_detail(appointmentId));
  return res.data;
};
