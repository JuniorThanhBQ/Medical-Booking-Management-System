import { AuthApis, endpoints } from "@/configs/Apis";
import { mockAvailableAppointmentsInLeave } from "@/data/mocks/doctor-schedule";
import {
  EMPTY_PATIENT,
  isTodayAppointment,
  normalizeDoctorAppointment,
} from "../utils/appointments-utils";

export async function fetchAppointmentsInDay({ date }) {
  if (!date) return [];

  // try {
  //   const response = await Apis.get("/appointments/available-in-day/", {
  //     params: { date },
  //   });

  //   const payload = response?.data;
  //   if (Array.isArray(payload)) return payload;
  //   if (Array.isArray(payload?.appointments)) return payload.appointments;

  //   return [];
  // } catch (error) {
  // }
  return mockAvailableAppointmentsInLeave;
}

export async function fetchDoctorTodayPatients(token) {
  if (!token) return [];

  const client = AuthApis(token);
  const response = await client.get(endpoints.appointments);

  const appointments = Array.isArray(response?.data?.items) ? response.data.items : [];
  const todayAppointments = appointments.filter((appointment) =>
    isTodayAppointment(appointment?.appointmentDate)
  );

  const normalizedAppointments = await Promise.all(
    todayAppointments.map(async (appointment) => {
      let patientProfile = EMPTY_PATIENT;

      try {
        const patientRes = await client.get(
          endpoints.appointment_patient_profile(appointment.id)
        );
        patientProfile = {
          dateOfBirth: patientRes?.data?.dateOfBirth ?? null,
          gender: patientRes?.data?.gender ?? null,
        };
      } catch {
        patientProfile = EMPTY_PATIENT;
      }

      return normalizeDoctorAppointment(appointment, patientProfile);
    })
  );

  return normalizedAppointments;
}
