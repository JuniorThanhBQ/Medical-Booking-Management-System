import { fetchDoctorAppointments } from "@features/doctor/services/appointments-api.js";
import {
  getAppointmentDetail,
  getAppointments,
  getMedicalRecordDetail,
} from "@features/users/services/appointment-api-service.js";

import { APPOINTMENT_STATUS, ROLE } from "@/configs/const";

const ACTIVITY_FILTERS = [
  { key: "all", label: "Tất cả" },
  { key: "appointments", label: "Lịch hẹn" },
  { key: "medical_records", label: "Hồ sơ bệnh án" },
];

const UPCOMING_STATUSES = new Set([
  APPOINTMENT_STATUS.PENDING,
  APPOINTMENT_STATUS.APPROVED,
  APPOINTMENT_STATUS.CONFIRMED,
]);

const STATUS_TO_UI = {
  [APPOINTMENT_STATUS.PENDING]: "PENDING",
  [APPOINTMENT_STATUS.APPROVED]: "APPROVED",
  [APPOINTMENT_STATUS.CONFIRMED]: "APPROVED",
  [APPOINTMENT_STATUS.COMPLETED]: "COMPLETED",
  [APPOINTMENT_STATUS.CANCEL]: "CANCEL",
  [APPOINTMENT_STATUS.CANCELLED]: "CANCEL",
};

const EMPTY_ACTIVITY_CONFIG = {
  filters: [],
  items: [],
  upcomingItems: [],
};

const toDisplayDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return Number.isNaN(date.getTime()) ? "" : date.toLocaleDateString("vi-VN");
};

const toDisplayTime = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
};

const toUiStatus = (status) => STATUS_TO_UI[status] || status || "";

const isUpcomingAppointment = (
  appointmentDate,
  status,
  startFrom = Date.now(),
) => {
  if (!appointmentDate || !status) return false;
  const date = new Date(appointmentDate);
  return (
    !Number.isNaN(date.getTime()) &&
    date.getTime() >= startFrom &&
    UPCOMING_STATUSES.has(status)
  );
};

const buildAppointmentActivity = (appointment) => ({
  id: `appointment-${appointment.id}`,
  type: "appointments",
  status: toUiStatus(appointment.status),
  title: appointment.doctorName || appointment.name || "Lịch hẹn",
  meta: [
    toDisplayDate(appointment.appointmentDate),
    toDisplayTime(appointment.appointmentDate),
  ]
    .filter(Boolean)
    .join(" "),
  date: toDisplayDate(appointment.appointmentDate),
  startTime: toDisplayTime(appointment.appointmentDate),
  dateTimeLabel: [
    toDisplayDate(appointment.appointmentDate),
    toDisplayTime(appointment.appointmentDate),
  ]
    .filter(Boolean)
    .join(" "),
  doctorName: appointment.doctorName,
  specialty: appointment.specialty,
  appointmentId: appointment.id,
  hero: null,
});

const buildMedicalRecordActivity = (
  appointmentDetail = {},
  medicalRecordDetail = {},
) => {
  const {
    id: recordIdFromDetail,
    status: recordStatus,
    diagnosis,
    doctorName: recordDoctor,
    specialty: recordSpecialty,
    notes,
    prescriptionText,
    treatmentOrders,
    createdAt: recordCreated,
  } = medicalRecordDetail || {};

  const {
    appointmentDate,
    medicalRecordId: appointmentRecordId,
    status: appointmentStatus,
    doctorName: appointmentDoctor,
    specialty: appointmentSpecialty,
  } = appointmentDetail || {};

  const finalRecordId = recordIdFromDetail || appointmentRecordId;
  const finalDoctor = recordDoctor || appointmentDoctor || "";
  const finalSpecialty = recordSpecialty || appointmentSpecialty || "";
  const finalStatus = toUiStatus(recordStatus || appointmentStatus);

  return {
    id: `medical-record-${finalRecordId}`,
    type: "medical_records",
    recordId: finalRecordId || null,
    status: finalStatus,
    title: diagnosis || "Hồ sơ bệnh án",
    meta: [finalDoctor, finalSpecialty].filter(Boolean).join(" · "),
    dateTimeLabel: toDisplayDate(recordCreated || appointmentDate),
    doctorName: finalDoctor,
    specialty: finalSpecialty,
    diagnosis: diagnosis || "",
    notes: notes || "",
    prescriptionText: prescriptionText || "",
    treatmentOrders: treatmentOrders || "",
    createdAt: recordCreated || null,
  };
};

const buildDoctorAppointmentActivity = (appointment) => ({
  ...buildAppointmentActivity(appointment),
  title: appointment.patientName || appointment.patient_name || "Lịch hẹn",
});

const buildDoctorMedicalRecordActivity = (
  appointmentDetail,
  medicalRecordDetail,
) => ({
  ...buildMedicalRecordActivity(appointmentDetail, medicalRecordDetail),
  title:
    appointmentDetail.patientName ||
    appointmentDetail.patient_name ||
    medicalRecordDetail?.diagnosis ||
    "Hồ sơ bệnh án",
});

const fetchAppointmentDetails = async (api, appointments) => {
  const uniqueAppointments = [
    ...new Map(appointments.map((a) => [a.id, a])).values(),
  ];
  return Promise.all(
    uniqueAppointments.map(async (appointment) => {
      try {
        const detail = await getAppointmentDetail(api, appointment.id);
        return {
          ...appointment,
          doctorName: detail?.doctorName || appointment.doctorName,
          specialty: detail?.specialty || "",
          status: detail?.status || appointment.status,
          appointmentDate:
            detail?.appointmentDate || appointment.appointmentDate,
          medicalRecordId: detail?.medicalRecordId || null,
        };
      } catch {
        return { ...appointment, specialty: "", medicalRecordId: null };
      }
    }),
  );
};

const fetchMedicalRecords = async (api, details) => {
  const candidates = details.filter((item) => item.medicalRecordId);
  const recordMap = new Map();
  if (!candidates.length) return recordMap;

  const records = await Promise.all(
    candidates.map(async (item) => {
      try {
        const record = await getMedicalRecordDetail(api, item.medicalRecordId);
        return [item.medicalRecordId, record];
      } catch {
        return [item.medicalRecordId, null];
      }
    }),
  );

  records.forEach(([id, record]) => recordMap.set(id, record));
  return recordMap;
};

const processActivities = (details, recordMap, isDoctor = false) => {
  const upcomingItems = [];
  const pastItems = [];
  const startOfTomorrow = new Date();
  startOfTomorrow.setDate(startOfTomorrow.getDate() + 1);
  startOfTomorrow.setHours(0, 0, 0, 0);
  const timeThreshold = isDoctor ? startOfTomorrow.getTime() : Date.now();

  details.forEach((detail) => {
    const isUpcoming = isUpcomingAppointment(
      detail.appointmentDate,
      detail.status,
      timeThreshold,
    );

    if (isUpcoming) {
      upcomingItems.push(
        isDoctor
          ? buildDoctorAppointmentActivity(detail)
          : buildAppointmentActivity(detail),
      );
      return;
    }

    if (detail.medicalRecordId) {
      const recordDetail = recordMap.get(detail.medicalRecordId);
      pastItems.push(
        isDoctor
          ? buildDoctorMedicalRecordActivity(detail, recordDetail)
          : buildMedicalRecordActivity(detail, recordDetail),
      );
      return;
    }

    pastItems.push(
      isDoctor
        ? buildDoctorAppointmentActivity(detail)
        : buildAppointmentActivity(detail),
    );
  });

  return { upcomingItems, pastItems };
};

const getPatientActivityConfig = async (api) => {
  const listResponse = await getAppointments(api);
  const appointments = Array.isArray(listResponse?.items)
    ? listResponse.items
    : [];
  if (!appointments.length)
    return { filters: ACTIVITY_FILTERS, items: [], upcomingItems: [] };

  const details = await fetchAppointmentDetails(api, appointments);
  const recordMap = await fetchMedicalRecords(api, details);
  const { upcomingItems, pastItems } = processActivities(
    details,
    recordMap,
    false,
  );

  return { filters: ACTIVITY_FILTERS, items: pastItems, upcomingItems };
};

const getDoctorActivityConfig = async (api) => {
  const appointments = await fetchDoctorAppointments(api);
  if (!appointments.length)
    return { filters: ACTIVITY_FILTERS, items: [], upcomingItems: [] };

  const details = await fetchAppointmentDetails(api, appointments);
  const recordMap = await fetchMedicalRecords(api, details);
  const { upcomingItems, pastItems } = processActivities(
    details,
    recordMap,
    true,
  );

  return { filters: ACTIVITY_FILTERS, items: pastItems, upcomingItems };
};

export async function getActivityConfig(role, api) {
  if (!api) return EMPTY_ACTIVITY_CONFIG;

  try {
    if (role === ROLE.Patient) return await getPatientActivityConfig(api);
    if (role === ROLE.Doctor) return await getDoctorActivityConfig(api);
  } catch {
    return { filters: ACTIVITY_FILTERS, items: [], upcomingItems: [] };
  }

  return EMPTY_ACTIVITY_CONFIG;
}
