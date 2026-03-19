import { medicalRecords, appointments } from '@/data/mocks/users';
import { DOCTORS } from '@/data/mocks/doctors';
import { normalizeActivity } from './profile-utils';
import { ROLE } from '@/configs/const';

const PATIENT_FILTERS = [
  { key: 'all', label: 'Tất cả' },
  { key: 'appointments', label: 'Lịch hẹn' },
  { key: 'medical_records', label: 'Hồ sơ bệnh án' },
];

const doctorMap = Object.fromEntries(DOCTORS.map((d) => [d.id, d]));
const PATIENT_ITEMS = [...medicalRecords, ...appointments].map((it) =>
  normalizeActivity(it, doctorMap)
);

export function getActivityConfig(role) {
  if (role === ROLE.Patient) return { filters: PATIENT_FILTERS, items: PATIENT_ITEMS };
  return { filters: [], items: [] };
}
