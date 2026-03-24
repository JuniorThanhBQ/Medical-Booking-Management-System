import Apis, { endpoints } from "@/configs/Apis";

export const getSpecialties = async (params = {}) => {
  const res = await Apis.get(endpoints.public_specialties, { params });
  return res.data.items ?? [];
};

export const getDoctors = async (params = {}) => {
  const res = await Apis.get(endpoints.public_doctors, { params });
  return res.data.items ?? [];
};

export const getDoctorDetail = async (doctorId) => {
  const res = await Apis.get(endpoints.public_doctor_detail(doctorId));
  return res.data;
};

export const getTimeSlots = async (doctorId, date) => {
  const res = await Apis.get(endpoints.public_doctor_time_slots(doctorId), {
    params: { date },
  });
  return res.data.items ?? [];
};
