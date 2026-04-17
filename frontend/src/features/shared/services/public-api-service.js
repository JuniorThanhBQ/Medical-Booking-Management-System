import apis, { endpoints } from "@/configs/apis";

export const getSpecialties = async (params = {}) => {
  const res = await apis.get(endpoints.public_specialties, { params });
  return res.data.data;
};

export const getDoctors = async (params = {}) => {
  const res = await apis.get(endpoints.public_doctors, { params });
  return res.data.data;
};

export const getSpecialtyDetail = async (specialtyId) => {
  const res = await apis.get(endpoints.public_specialty_detail(specialtyId));
  return res.data;
};

export const getDoctorDetail = async (doctorId) => {
  const res = await apis.get(endpoints.public_doctor_detail(doctorId));
  return res.data;
};

export const getMedicalServices = async (params = {}) => {
  const res = await apis.get(endpoints.public_medical_services, { params });
  return res.data.data.items ?? [];
};

export const getMedicalServiceDetail = async (serviceId) => {
  const res = await apis.get(
    endpoints.public_medical_service_detail(serviceId),
  );
  return res.data;
};

export const getTimeSlots = async (doctorId, date, serviceId) => {
  const res = await apis.get(endpoints.public_doctor_time_slots(doctorId), {
    params: { date, serviceId },
  });
  return res.data ?? [];
};
