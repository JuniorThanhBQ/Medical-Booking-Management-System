import Apis, { endpoints } from "@/configs/Apis";

export const getSpecialties = async (params = {}) => {
  const res = await Apis.get(endpoints.public_specialties, { params });
  return res.data.data.items ?? [];
};

export const getDoctors = async (params = {}) => {
  const res = await Apis.get(endpoints.public_doctors, { params });
  console.log("GET DOCTOR", res)
  return res.data.data.items ?? [];
};

export const getSpecialtyDetail = async (specialtyId) => {
  const res = await Apis.get(endpoints.public_specialty_detail(specialtyId));
  console.log("specialty detail url: ", endpoints.public_specialty_detail(specialtyId))
  return res.data;
};

export const getDoctorDetail = async (doctorId) => {
  const res = await Apis.get(endpoints.public_doctor_detail(doctorId));
  console.log("doctor detail url: ", endpoints.public_doctor_detail(doctorId))
  return res.data;
};

export const getMedicalServices = async (params = {}) => {
  const res = await Apis.get(endpoints.public_medical_services, { params });
  return res.data.data.items ?? [];
};

export const getMedicalServiceDetail = async (serviceId) => {
  const res = await Apis.get(endpoints.public_medical_service_detail(serviceId));
  return res.data;
};

export const getTimeSlots = async (doctorId, date, serviceId) => {
  const res = await Apis.get(endpoints.public_doctor_time_slots(doctorId), {
    params: { date, serviceId },
  });
  return res.data ?? [];
};
