import { AuthApis, endpoints } from "@/configs/Apis";
import { getToken } from "@/repository/local-storage-repository";

export async function fetchMySchedule() {
  const token = getToken();
  const res = await AuthApis(token).get(endpoints.doctor_my_schedule);
  console.log("fetchMySchedule res", res.data)
  return res.data;
}

export async function submitScheduleRequest(payload) {
  console.log("submit Schedule payload", payload)
  console.log("token", getToken())
  const token = getToken();
  const res = await AuthApis(token).post(endpoints.doctor_schedule_request, payload);
  return res.data;
}
