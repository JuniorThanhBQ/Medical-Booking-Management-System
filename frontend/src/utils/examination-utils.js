import { getAge } from "@/utils/Utils.js";

export const EMPTY_FORM = {
  diagnosis: "",
  notes: "",
  prescriptionText: "",
  treatmentOrders: "",
};

const GENDER_LABELS = {
  MALE: "Nam",
  FEMALE: "Nữ",
  OTHER: "Khác",
};

export function toExamFormData(record) {
  if (!record) {
    return EMPTY_FORM;
  }

  return {
    diagnosis: record.diagnosis || "",
    notes: record.notes || "",
    prescriptionText: record.prescriptionText || "",
    treatmentOrders: record.treatmentOrders || "",
  };
}

export function toPatient(appointmentDetail, profile, fallbackAppointmentId) {
  const fullName =
    profile?.fullName ||
    [profile?.lastName, profile?.firstName].filter(Boolean).join(" ").trim() ||
    appointmentDetail?.patientName ||
    "—";

  return {
    id:
      profile?.id ||
      appointmentDetail?.patientId ||
      appointmentDetail?.id ||
      fallbackAppointmentId,
    name: fullName,
    age: getAge(profile?.dateOfBirth) ?? "—",
    gender: GENDER_LABELS[profile?.gender] || "—",
    phone: profile?.phone || "—",
  };
}

export function toRecordHistory(record) {
  if (!record?.id) {
    return [];
  }

  return [
    {
      id: record.id,
      createdAt:
        record.createdAt || record.updatedAt || new Date().toISOString(),
      diagnosis: record.diagnosis || "Chưa có chẩn đoán",
      notes: record.notes || "",
      prescriptionText: record.prescriptionText || "",
      treatmentOrders: record.treatmentOrders || "",
    },
  ];
}

export function toMedicalRecordPayload(formData, status) {
  return {
    diagnosis: formData.diagnosis?.trim() || "",
    notes: formData.notes?.trim() || "",
    prescriptionText: formData.prescriptionText?.trim() || "",
    treatmentOrders: formData.treatmentOrders?.trim() || "",
    status,
  };
}

export function normalizeMedicalRecord(payload) {
  return {
    id: payload?.id ?? null,
    diagnosis: payload?.diagnosis || "",
    notes: payload?.notes || "",
    prescriptionText: payload?.prescriptionText || "",
    treatmentOrders: payload?.treatmentOrders || "",
    status: payload?.status || "",
    createdAt: payload?.createdAt || null,
    updatedAt: payload?.updatedAt || null,
  };
}
