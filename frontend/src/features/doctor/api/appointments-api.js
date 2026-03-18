import Apis from "@/configs/Apis";
import { mockAvailableAppointmentsInLeave } from "../data";

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

