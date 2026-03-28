import { medicalRecords, appointments } from '@/data/mocks/users';
import { DOCTORS } from '@/data/mocks/doctors';
import { normalizeActivity } from './profile-utils';
import { ROLE, APPOINTMENT_STATUS } from '@/configs/const';

const PATIENT_FILTERS = [
  { key: 'all', label: 'Tất cả' },
  { key: 'appointments', label: 'Lịch hẹn' },
  { key: 'medical_records', label: 'Hồ sơ bệnh án' },
];

const doctorMap = Object.fromEntries(DOCTORS.map((d) => [d.id, d]));

const UPCOMING_STATUSES = [APPOINTMENT_STATUS.PENDING, APPOINTMENT_STATUS.CONFIRMED];

const today = new Date().toISOString().slice(0, 10);
const upcomingAppointments = appointments.filter(
  (a) => a.date >= today && UPCOMING_STATUSES.includes(a.status)
);
const pastAppointments = appointments.filter(
  (a) => !(a.date >= today && UPCOMING_STATUSES.includes(a.status))
);

const PATIENT_ITEMS = [...medicalRecords, ...pastAppointments].map((it) =>
  normalizeActivity(it, doctorMap)
);
const PATIENT_UPCOMING = upcomingAppointments.map((it) =>
  normalizeActivity(it, doctorMap)
);

export function getActivityConfig(role) {
  if (role === ROLE.Patient) {
    return { filters: PATIENT_FILTERS, items: PATIENT_ITEMS, upcomingItems: PATIENT_UPCOMING };
  }
  return { filters: [], items: [], upcomingItems: [] };
}
