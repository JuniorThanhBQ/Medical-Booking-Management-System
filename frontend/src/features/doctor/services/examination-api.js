import { endpoints } from "@/configs/apis";
import { normalizeMedicalRecord } from "@/utils/examination-utils.js";

export async function getAppointmentDetail(api, appointmentId) {
  const response = await api.get(endpoints.appointment_detail(appointmentId));
  return response?.data ?? null;
}

export async function getAppointmentPatientProfile(api, appointmentId) {
  const response = await api.get(
    endpoints.appointment_patient_profile(appointmentId),
  );
  return response?.data ?? null;
}

export async function getMedicalRecordDetail(api, medicalRecordId) {
  const response = await api.get(
    endpoints.medical_record_detail(medicalRecordId),
  );
  return normalizeMedicalRecord(response?.data);
}

export async function createMedicalRecordForAppointment(
  api,
  appointmentId,
  payload,
) {
  const response = await api.post(
    endpoints.medical_record_by_appointment(appointmentId),
    payload,
  );
  return normalizeMedicalRecord(response?.data);
}

export async function updateMedicalRecord(api, medicalRecordId, payload) {
  const response = await api.patch(
    endpoints.medical_record_detail(medicalRecordId),
    payload,
  );
  return normalizeMedicalRecord(response?.data);
}
