import axios from "axios";

export const BASE_URL = import.meta.env.VITE_API_URL;

export const endpoints = {
  auth_login: "/api/v2/auth/login",
  auth_register: "/api/v2/auth/register",
  auth_refresh: "/api/v2/auth/refresh",
  auth_logout: "/api/v2/auth/logout",
  auth_current_user: "/api/v2/auth/current-user",
  auth_email_validator: "/api/v2/auth/email-validator",
  auth_email_verification: "/api/v2/auth/email-verification",
  public_specialties: "/api/v2/public/specialties",
  public_specialty_detail: (id) => `/api/v2/public/specialties/${id}`,
  public_doctors: "/api/v2/public/doctors",
  public_doctor_detail: (id) => `/api/v2/public/doctors/${id}`,
  public_doctor_time_slots: (id) => `/api/v2/public/doctors/${id}/time-slots`,
  public_medical_services: "/api/v2/public/medical-services",
  public_medical_service_detail: (id) =>
    `/api/v2/public/medical-services/${id}`,
  doctor_registration: "/api/v2/public/doctors-registration",
  appointments: "/api/v2/appointments",
  appointment_detail: (id) => `/api/v2/appointments/${id}`,
  appointment_patient_profile: (id) =>
    `/api/v2/appointments/${id}/patient-profile`,
  appointment_by_receptionist: "/api/v2/appointments/receptionist-appointments",
  booking_transaction_lock: `/api/v2/appointments/transaction-locked`,
  booking_transaction_unlock: `/api/v2/appointments/transaction-unlocked`,
  medical_record: "/api/v2/medical-records",
  medical_record_detail: (id) => `/api/v2/medical-records/${id}`,
  medical_record_by_appointment: (appointmentId) =>
    `/api/v2/medical-records/appointments/${appointmentId}`,
  doctor_schedule: "/api/v2/doctors/my-schedule",
  doctor_schedule_request: "/api/v2/doctors/schedule-requests",
  notification: "/api/v2/notifications",
  notification_detail: (id) => `/api/v2/notifications/${id}`,
};

export const apis = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
  xsrfCookieName: 'csrf_token', 
  xsrfHeaderName: 'X-CSRFToken'
});

export default apis;
