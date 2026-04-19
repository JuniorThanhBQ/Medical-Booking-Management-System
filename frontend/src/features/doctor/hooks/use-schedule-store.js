import { generateTimeOptions } from "@utils/Utils.js";
import { toast } from "sonner";
import { create } from "zustand";

import { apis as api } from "@/configs/apis";

import {
  fetchMySchedule,
  submitScheduleRequest,
} from "../services/schedule-api-service.js";

const DEFAULT_WORK_DATE = [
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
];
const SUGGESTED_START = "09:00";
const SUGGESTED_END = "16:00";

const initialState = {
  workDate: DEFAULT_WORK_DATE,
  startTime: "",
  endTime: "",
  timeOptions: generateTimeOptions(),
  appointments: [],
  isLoading: false,
  scheduleError: null,
  saveSuccess: false,
};

export const useScheduleStore = create((set, get) => ({
  ...initialState,

  loadSchedule: async () => {
    set({ isLoading: true, scheduleError: null });
    try {
      const data = await fetchMySchedule(api);
      const ws = data.workSchedule;

      set({
        workDate: ws ? ws.workDate.map((d) => d.toUpperCase()) : [],
        startTime: ws?.startTime ? ws.startTime.slice(0, 5) : "",
        endTime: ws?.endTime ? ws.endTime.slice(0, 5) : "",
        appointments: data.appointments ?? [],
        isLoading: false,
      });
    } catch (error) {
      console.error("Failed to load schedule:", error);
      toast.error("Không thể tải lịch làm việc.");
      set({
        isLoading: false,
        scheduleError: "Không thể tải lịch làm việc.",
      });
    }
  },

  saveSchedule: async (token, reason = "") => {
    const { workDate, startTime, endTime } = get();
    if (workDate.length === 0) {
      const errorMsg = "Vui lòng chọn ít nhất một ngày làm việc.";
      toast.warning(errorMsg);
      set({ scheduleError: errorMsg });
      throw new Error(errorMsg);
    }
    set({ isLoading: true, scheduleError: null, saveSuccess: false });
    try {
      await submitScheduleRequest(token, {
        newWorkSchedule: {
          title: "Lịch làm việc",
          description: "Lịch khám bệnh hàng tuần",
          start_time: `${startTime || SUGGESTED_START}:00`,
          end_time: `${endTime || SUGGESTED_END}:00`,
          work_date: workDate,
        },
        reason,
      });

      toast.success("Lưu lịch làm việc thành công!");
      set({ saveSuccess: true, isLoading: false });

      try {
        const data = await fetchMySchedule(token);
        const ws = data.workSchedule;
        if (ws) {
          set({
            workDate: ws.workDate.map((d) => d.toUpperCase()),
            startTime: ws.startTime
              ? ws.startTime.slice(0, 5)
              : SUGGESTED_START,
            endTime: ws.endTime ? ws.endTime.slice(0, 5) : SUGGESTED_END,
            appointments: data.appointments ?? [],
          });
        }
      } catch {
        toast.error("Không thể tải lịch làm việc sau khi lưu.");
      }
    } catch (error) {
      const status = error?.response?.status;
      const msg =
        status === 403
          ? "Không thể thay đổi lịch vì có lịch hẹn trong 30 ngày tới."
          : status === 401
            ? "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."
            : "Lưu lịch thất bại. Vui lòng thử lại.";
      console.error("Failed to save schedule:", error);
      toast.error(msg);
      set({ isLoading: false, scheduleError: msg });
      throw new Error(msg);
    }
  },

  clearScheduleError: () => set({ scheduleError: null, saveSuccess: false }),

  toggleWorking: (day) =>
    set((state) => ({
      workDate: state.workDate.includes(day)
        ? state.workDate.filter((d) => d !== day)
        : [...state.workDate, day],
    })),

  setTime: (field, value) => set({ [field]: value }),
}));
