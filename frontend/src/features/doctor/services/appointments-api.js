import { apis, endpoints } from "@/configs/apis";
import {
  EMPTY_PATIENT,
  isTodayAppointment,
  normalizeDoctorAppointment,
} from "@/utils/appointments-utils.js";

export async function fetchAppointmentsInDay({ date }) {
  if (!date) return [];

  try {
    const response = await apis.get(endpoints["appointments"], {
      params: { date },
    });

    const payload = response?.data;
    if (Array.isArray(payload)) return payload;
    if (Array.isArray(payload?.appointments)) return payload.appointments;

    return [];
  } catch (error) {
    console.error("Error fetching appointments in day:", error);
  }
}

export async function fetchDoctorAppointments(api) {
  const client = api;
  const response = await client.get(endpoints.appointments);
  return Array.isArray(response?.data?.items) ? response.data.items : [];
}

export async function fetchDoctorTodayPatients(api) {
  if (!api) return [];

  try {
    const response = await api.get(endpoints.appointments);

    const appointments = Array.isArray(response?.data?.items)
      ? response.data.items
      : [];

    const todayAppointments = appointments.filter((appointment) =>
      isTodayAppointment(appointment?.appointmentDate),
    );

    if (todayAppointments.length === 0) return [];

    const normalizedAppointments = await Promise.all(
      todayAppointments.map(async (appointment) => {
        let patientProfile = EMPTY_PATIENT;

        try {
          const patientRes = await api.get(
            endpoints.appointment_patient_profile(appointment.id),
          );

          if (patientRes?.data) {
            patientProfile = {
              dateOfBirth: patientRes.data.dateOfBirth ?? null,
              gender: patientRes.data.gender ?? null,
            };
          }
        } catch (error) {
          console.warn(`Không thể lấy profile của lịch hẹn ${appointment.id}`);
        }

        return normalizeDoctorAppointment(appointment, patientProfile);
      }),
    );

    return normalizedAppointments;
  } catch (error) {
    console.error("Lỗi khi tải danh sách lịch hẹn:", error);
    throw error;
  }
}
