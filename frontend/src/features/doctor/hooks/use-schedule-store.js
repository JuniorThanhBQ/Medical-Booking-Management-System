import { create } from "zustand";
import { generateTimeOptions } from "../../../utils/Utils.js";
import { fetchMySchedule, submitScheduleRequest } from "../services/schedule-api-service.js";

const DEFAULT_WORK_DATE = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"];
const DEFAULT_START = "09:00";
const DEFAULT_END = "16:00";

const initialState = {
  workDate: DEFAULT_WORK_DATE,
  startTime: DEFAULT_START,
  endTime: DEFAULT_END,
  leaveRequests: [],
  newRequest: { type: "time_off" },
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
      const data = await fetchMySchedule();
      const ws = data.workSchedule;
      set({
        workDate: ws ? ws.workDate.map((d) => d.toUpperCase()) : DEFAULT_WORK_DATE,
        startTime: ws?.startTime ? ws.startTime.slice(0, 5) : DEFAULT_START,
        endTime: ws?.endTime ? ws.endTime.slice(0, 5) : DEFAULT_END,
        appointments: data.appointments ?? [],
        isLoading: false,
      });
    } catch (error) {
      console.error("Failed to load schedule:", error);
      const msg = error?.response?.status === 401
        ? "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."
        : "Không thể tải lịch làm việc. Vui lòng thử lại.";
      set({ isLoading: false, scheduleError: msg });
    }
  },

  saveSchedule: async (reason = "") => {
    const { workDate, startTime, endTime } = get();
    if (workDate.length === 0) {
      set({ scheduleError: "Vui lòng chọn ít nhất một ngày làm việc." });
      return;
    }
    set({ isLoading: true, scheduleError: null, saveSuccess: false });
    try {
      await submitScheduleRequest({
        newWorkSchedule: {
          title: "Lịch làm việc",
          description: "Lịch khám bệnh hàng tuần",
          start_time: `${startTime}:00`,
          end_time: `${endTime}:00`,
          work_date: workDate,
        },
        reason,
      });
      set({ saveSuccess: true, isLoading: false });
      try {
        const data = await fetchMySchedule();
        const ws = data.workSchedule;
        if (ws) {
          set({
            workDate: ws.workDate.map((d) => d.toUpperCase()),
            startTime: ws.startTime ? ws.startTime.slice(0, 5) : DEFAULT_START,
            endTime: ws.endTime ? ws.endTime.slice(0, 5) : DEFAULT_END,
            appointments: data.appointments ?? [],
          });
        }
      } catch {
      }
    } catch (error) {
      const status = error?.response?.status;
      const msg = status === 403
        ? "Không thể thay đổi lịch vì có lịch hẹn trong 7 ngày tới."
        : status === 401
          ? "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."
          : "Lưu lịch thất bại. Vui lòng thử lại.";
      console.error("Failed to save schedule:", error);
      set({ isLoading: false, scheduleError: msg });
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

  updateNewRequest: (patch) =>
    set((state) => ({
      newRequest: { ...state.newRequest, ...patch },
    })),

  addLeaveRequest: () => {
    const { newRequest, leaveRequests } = get();
    if (!newRequest.fromDate || !newRequest.toDate || !newRequest.type) return;

    const id = `req-${Date.now()}`;
    const request = {
      id,
      type: newRequest.type,
      fromDate: newRequest.fromDate,
      toDate: newRequest.toDate,
      reason: newRequest.reason,
      status: "pending",
    };
    set({
      leaveRequests: [request, ...leaveRequests],
      newRequest: { type: newRequest.type, fromDate: undefined, toDate: undefined, reason: "" },
    });
  },
}));
