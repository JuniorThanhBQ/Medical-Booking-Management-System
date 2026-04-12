import { AuthApis, endpoints } from "@/configs/Apis";
import {
  normalizeMedicalRecord,
} from "@/utils/examination-utils.js";

export async function getAppointmentDetail(token, appointmentId) {
  const response = await AuthApis(token).get(endpoints.appointment_detail(appointmentId));
  return response?.data ?? null;
}

export async function getAppointmentPatientProfile(token, appointmentId) {
  const response = await AuthApis(token).get(
    endpoints.appointment_patient_profile(appointmentId)
  );
  return response?.data ?? null;
}

export async function getMedicalRecordDetail(token, medicalRecordId) {
  const response = await AuthApis(token).get(
    endpoints.medical_record_detail(medicalRecordId)
  );
  return normalizeMedicalRecord(response?.data);
}

export async function createMedicalRecordForAppointment(token, appointmentId, payload) {
  const response = await AuthApis(token).post(
    endpoints.medical_record_by_appointment(appointmentId),
    payload
  );
  return normalizeMedicalRecord(response?.data);
}

export async function updateMedicalRecord(token, medicalRecordId, payload) {
  const response = await AuthApis(token).patch(
    endpoints.medical_record_detail(medicalRecordId),
    payload
  );
  return normalizeMedicalRecord(response?.data);
}
