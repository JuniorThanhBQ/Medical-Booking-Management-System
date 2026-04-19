import { endpoints } from "@/configs/apis";

export async function fetchMySchedule(api) {
  const res = await api.get(endpoints.doctor_schedule);
  return res.data;
}

export async function submitScheduleRequest(api, payload) {
  console.log("submit Schedule payload", payload);
  const res = await api.post(endpoints.doctor_schedule_request, payload);
  return res.data;
}
