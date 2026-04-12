import { ROLE, APPOINTMENT_STATUS } from '@/configs/const';
import {
  getAppointments,
  getAppointmentDetail,
  getMedicalRecordDetail,
} from '../services/appointment-api-service';
import { fetchDoctorAppointments } from '@/features/doctor/api/appointments-api';

const ACTIVITY_FILTERS = [
  { key: 'all', label: 'Tất cả' },
  { key: 'appointments', label: 'Lịch hẹn' },
  { key: 'medical_records', label: 'Hồ sơ bệnh án' },
];

const UPCOMING_STATUSES = new Set([
  APPOINTMENT_STATUS.PENDING,
  APPOINTMENT_STATUS.APPROVED,
  APPOINTMENT_STATUS.CONFIRMED,
]);

const STATUS_TO_UI = {
  [APPOINTMENT_STATUS.PENDING]: 'PENDING',
  [APPOINTMENT_STATUS.APPROVED]: 'APPROVED',
  [APPOINTMENT_STATUS.CONFIRMED]: 'APPROVED',
  [APPOINTMENT_STATUS.COMPLETED]: 'COMPLETED',
  [APPOINTMENT_STATUS.CANCEL]: 'CANCEL',
  [APPOINTMENT_STATUS.CANCELLED]: 'CANCEL',
};

const EMPTY_ACTIVITY_CONFIG = {
  filters: [],
  items: [],
  upcomingItems: [],
};

const toDisplayDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleDateString('vi-VN');
};

const toDisplayTime = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
};

const toUiStatus = (status) => STATUS_TO_UI[status] || status || '';

const isUpcomingAppointment = (appointmentDate, status) => {
  if (!appointmentDate || !status) return false;
  const date = new Date(appointmentDate);
  if (Number.isNaN(date.getTime())) return false;
  return date.getTime() >= Date.now() && UPCOMING_STATUSES.has(status);
};

const buildAppointmentActivity = (appointment) => ({
  id: `appointment-${appointment.id}`,
  type: 'appointments',
  status: toUiStatus(appointment.status),
  title: appointment.doctorName || appointment.name || 'Lịch hẹn',
  meta: [toDisplayDate(appointment.appointmentDate), toDisplayTime(appointment.appointmentDate)]
    .filter(Boolean)
    .join(' '),
  date: toDisplayDate(appointment.appointmentDate),
  startTime: toDisplayTime(appointment.appointmentDate),
  dateTimeLabel: [toDisplayDate(appointment.appointmentDate), toDisplayTime(appointment.appointmentDate)]
    .filter(Boolean)
    .join(' '),
  doctorName: appointment.doctorName,
  specialty: appointment.specialty,
  appointmentId: appointment.id,
  hero: null,
});

const buildMedicalRecordActivity = (appointmentDetail, medicalRecordDetail) => {
  const recordDate = medicalRecordDetail?.createdAt || appointmentDetail?.appointmentDate;
  return {
    id: `medical-record-${medicalRecordDetail?.id || appointmentDetail?.medicalRecordId}`,
    type: 'medical_records',
    recordId: medicalRecordDetail?.id || appointmentDetail?.medicalRecordId || null,
    status: toUiStatus(medicalRecordDetail?.status || appointmentDetail?.status),
    title: medicalRecordDetail?.diagnosis || 'Hồ sơ bệnh án',
    meta: [medicalRecordDetail?.doctorName || appointmentDetail?.doctorName, medicalRecordDetail?.specialty || appointmentDetail?.specialty]
      .filter(Boolean)
      .join(' · '),
    dateTimeLabel: toDisplayDate(recordDate),
    doctorName: medicalRecordDetail?.doctorName || appointmentDetail?.doctorName || '',
    specialty: medicalRecordDetail?.specialty || appointmentDetail?.specialty || '',
    diagnosis: medicalRecordDetail?.diagnosis || '',
    notes: medicalRecordDetail?.notes || '',
    prescriptionText: medicalRecordDetail?.prescriptionText || '',
    treatmentOrders: medicalRecordDetail?.treatmentOrders || '',
    createdAt: medicalRecordDetail?.createdAt || null,
  };
};

const getPatientActivityConfig = async (token) => {
  const listResponse = await getAppointments(token);
  const appointments = Array.isArray(listResponse?.items) ? listResponse.items : [];
  if (!appointments.length) {
    return { filters: ACTIVITY_FILTERS, items: [], upcomingItems: [] };
  }

  const uniqueAppointments = [...new Map(appointments.map((a) => [a.id, a])).values()];
  const detailResponses = await Promise.all(
    uniqueAppointments.map(async (appointment) => {
      try {
        const detail = await getAppointmentDetail(token, appointment.id);
        return {
          ...appointment,
          doctorName: detail?.doctorName || appointment.doctorName,
          specialty: detail?.specialty || '',
          status: detail?.status || appointment.status,
          appointmentDate: detail?.appointmentDate || appointment.appointmentDate,
          medicalRecordId: detail?.medicalRecordId || null,
        };
      } catch {
        return {
          ...appointment,
          specialty: '',
          medicalRecordId: null,
        };
      }
    })
  );

  const upcomingItems = [];
  const pastItems = [];

  const medicalRecordCandidates = detailResponses.filter((item) => item.medicalRecordId);
  const medicalRecordMap = new Map();
  if (medicalRecordCandidates.length) {
    const medicalRecordResponses = await Promise.all(
      medicalRecordCandidates.map(async (item) => {
        try {
          const record = await getMedicalRecordDetail(token, item.medicalRecordId);
          return [item.medicalRecordId, record];
        } catch {
          return [item.medicalRecordId, null];
        }
      })
    );

    for (const [recordId, record] of medicalRecordResponses) {
      medicalRecordMap.set(recordId, record);
    }
  }

  for (const detail of detailResponses) {
    if (isUpcomingAppointment(detail.appointmentDate, detail.status)) {
      upcomingItems.push(buildAppointmentActivity(detail));
      continue;
    }

    if (detail.medicalRecordId) {
      const recordDetail = medicalRecordMap.get(detail.medicalRecordId);
      pastItems.push(buildMedicalRecordActivity(detail, recordDetail));
      continue;
    }

    pastItems.push(buildAppointmentActivity(detail));
  }

  return {
    filters: ACTIVITY_FILTERS,
    items: pastItems,
    upcomingItems,
  };
};

const buildDoctorAppointmentActivity = (appointment) => ({
  ...buildAppointmentActivity(appointment),
  title: appointment.patientName || appointment.patient_name || 'Lịch hẹn',
});

const buildDoctorMedicalRecordActivity = (appointmentDetail, medicalRecordDetail) => ({
  ...buildMedicalRecordActivity(appointmentDetail, medicalRecordDetail),
  title: appointmentDetail.patientName || appointmentDetail.patient_name || medicalRecordDetail?.diagnosis || 'Hồ sơ bệnh án',
});

const getDoctorActivityConfig = async (token) => {
  const appointments = await fetchDoctorAppointments(token);
  if (!appointments.length) {
    return { filters: ACTIVITY_FILTERS, items: [], upcomingItems: [] };
  }

  const uniqueAppointments = [...new Map(appointments.map((a) => [a.id, a])).values()];
  const detailResponses = await Promise.all(
    uniqueAppointments.map(async (appointment) => {
      try {
        const detail = await getAppointmentDetail(token, appointment.id);
        return {
          ...appointment,
          specialty: detail?.specialty || '',
          status: detail?.status || appointment.status,
          appointmentDate: detail?.appointmentDate || appointment.appointmentDate,
          medicalRecordId: detail?.medicalRecordId || null,
        };
      } catch {
        return { ...appointment, specialty: '', medicalRecordId: null };
      }
    })
  );

  const medicalRecordCandidates = detailResponses.filter((item) => item.medicalRecordId);
  const medicalRecordMap = new Map();
  if (medicalRecordCandidates.length) {
    const records = await Promise.all(
      medicalRecordCandidates.map(async (item) => {
        try {
          const record = await getMedicalRecordDetail(token, item.medicalRecordId);
          return [item.medicalRecordId, record];
        } catch {
          return [item.medicalRecordId, null];
        }
      })
    );
    for (const [id, record] of records) medicalRecordMap.set(id, record);
  }

  const startOfTomorrow = new Date();
  startOfTomorrow.setDate(startOfTomorrow.getDate() + 1);
  startOfTomorrow.setHours(0, 0, 0, 0);

  const pastItems = [];
  const upcomingItems = [];

  for (const detail of detailResponses) {
    const date = new Date(detail.appointmentDate);
    const isUpcoming = UPCOMING_STATUSES.has(detail.status) && date >= startOfTomorrow;
    if (isUpcoming) {
      upcomingItems.push(buildDoctorAppointmentActivity(detail));
    } else if (detail.medicalRecordId) {
      pastItems.push(buildDoctorMedicalRecordActivity(detail, medicalRecordMap.get(detail.medicalRecordId)));
    } else {
      pastItems.push(buildDoctorAppointmentActivity(detail));
    }
  }

  return { filters: ACTIVITY_FILTERS, items: pastItems, upcomingItems };
};

export async function getActivityConfig(role, token) {
  if (!token) return EMPTY_ACTIVITY_CONFIG;

  if (role === ROLE.Patient) {
    try { return await getPatientActivityConfig(token); }
    catch { return { filters: ACTIVITY_FILTERS, items: [], upcomingItems: [] }; }
  }

  if (role === ROLE.Doctor) {
    try { return await getDoctorActivityConfig(token); }
    catch { return { filters: ACTIVITY_FILTERS, items: [], upcomingItems: [] }; }
  }

  return EMPTY_ACTIVITY_CONFIG;
}
