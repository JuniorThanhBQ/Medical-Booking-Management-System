import axios from "axios";

export const BASE_URL = import.meta.env.VITE_API_URL;

export const endpoints = {
  auth_login: "/api/v1/auth/login",
  auth_register: "/api/v1/auth/register",
  auth_refresh: "/api/v1/auth/refresh",
  auth_logout: "/api/v1/auth/logout",
  auth_current_user: "/api/v1/auth/current-user",
  auth_email_validator: "/api/v1/auth/email-validator",
  auth_email_verification: "/api/v1/auth/email-verification",
  public_specialties: "/api/v1/public/specialties",
  public_specialty_detail: (id) => `/api/v1/public/specialties/${id}`,
  public_doctors: "/api/v1/public/doctors",
  public_doctor_detail: (id) => `/api/v1/public/doctors/${id}`,
  public_doctor_time_slots: (id) => `/api/v1/public/doctors/${id}/time-slots`,
  public_medical_services: "/api/v1/public/medical-services",
  public_medical_service_detail: (id) =>
    `/api/v1/public/medical-services/${id}`,
  appointments: "/api/v1/appointments",
  appointment_detail: (id) => `/api/v1/appointments/${id}`,
  appointment_patient_profile: (id) =>
    `/api/v1/appointments/${id}/patient-profile`,
  appointment_by_receptionist: "/api/v1/appointments/receptionist-appointments",
  booking_transaction_lock: `/api/v1/appointments/transaction-locked`,
  booking_transaction_unlock: `/api/v1/appointments/transaction-unlocked`,
  medical_record: "/api/v1/medical-records",
  medical_record_detail: (id) => `/api/v1/medical-records/${id}`,
  medical_record_by_appointment: (appointmentId) =>
    `/api/v1/medical-records/appointments/${appointmentId}`,
  doctor_schedule: "/api/v1/doctors/my-schedule",
  doctor_schedule_request: "/api/v1/doctors/schedule-requests",
  doctor_registration: "/api/v1/public/doctors-registration",
  notification: "/api/v1/notifications",
  notification_detail: (id) => `/api/v1/notifications/${id}`,
};

export const apis = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});

export const AuthApis = (token) => {
  const headers = { "Content-Type": "application/json" };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return axios.create({
    baseURL: BASE_URL,
    headers,
    withCredentials: true,
  });
};

export default apis;
