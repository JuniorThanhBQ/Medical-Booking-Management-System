import { endpoints } from "@/configs/apis";

export const createAppointment = async (
  api,
  payload,
  isReceptionist = false,
) => {
  const endpoint = isReceptionist
    ? endpoints.appointment_by_receptionist
    : endpoints.appointments;

  const res = await api.post(endpoint, payload);
  return res.data;
};
