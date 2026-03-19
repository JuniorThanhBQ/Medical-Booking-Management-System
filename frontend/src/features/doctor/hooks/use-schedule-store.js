import { create } from "zustand";
import { OPEN_HOURS, INITIAL_DAYS } from "@/configs/const";
import { buildDefaultDaySchedule, generateTimeOptions } from "../utils";

const defaultWeeklySchedule = INITIAL_DAYS.map(buildDefaultDaySchedule);

const defaultNewRequest = {
  type: "time_off",
};

const defaultTimeOptions = generateTimeOptions();

const initialState = {
  weeklySchedule: defaultWeeklySchedule,
  leaveRequests: [],
  newRequest: defaultNewRequest,
  timeOptions: defaultTimeOptions,
};

export const useScheduleStore = create((set, get) => ({
  ...initialState,

  toggleWorking: (day) =>
    set((state) => {
      console.log("day: ", day)
      console.log("weekly schedule: ", state.weeklySchedule)
      return {
      weeklySchedule: state.weeklySchedule.map((entry) =>
        entry.day === day
          ? {
              ...entry,
              isWorking: !entry.isWorking,
              ranges: entry.isWorking
                ? []
                : entry.ranges.length
                  ? entry.ranges
                  : [buildDefaultDaySchedule(day).ranges[0]],
            }
          : entry,
      ),
    }}),

  changeRange: ({ day, rangeId, field, value }) =>
    set((state) => ({
      weeklySchedule: state.weeklySchedule.map((entry) =>
        entry.day === day
          ? {
              ...entry,
              ranges: entry.ranges.map((range) =>
                range.id === rangeId
                  ? {
                      ...range,
                      [field]: value,
                    }
                  : range,
              ),
            }
          : entry,
      ),
    })),

  updateNewRequest: (patch) =>
    set((state) => ({
      newRequest: {
        ...state.newRequest,
        ...patch,
      },
    })),

  addLeaveRequest: () => {
    const { newRequest, leaveRequests } = get();

    if (
      !newRequest.fromDate ||
      !newRequest.toDate ||
      !newRequest.type
    ) {
      return;
    }

    const id = `req-${Date.now()}`;
    const request = {
      id,
      type: newRequest.type,
      fromDate: newRequest.fromDate,
      toDate: newRequest.toDate,
      reason: newRequest.reason,
      status: "pending",
    };

    const resetDraft = {
      type: newRequest.type,
      fromDate: undefined,
      toDate: undefined,
      reason: "",
    };

    set({
      leaveRequests: [request, ...leaveRequests],
      newRequest: resetDraft,
    });
  },
}));