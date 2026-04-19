import { useEffect, useMemo } from "react";

import useAuth from "@/contexts/auth/AuthContext";

import { useScheduleStore } from "./use-schedule-store";

const DAY_MAP = {
  MONDAY: "Thứ 2",
  TUESDAY: "Thứ 3",
  WEDNESDAY: "Thứ 4",
  THURSDAY: "Thứ 5",
  FRIDAY: "Thứ 6",
  SATURDAY: "Thứ 7",
  SUNDAY: "Chủ nhật",
};

export const useSchedulePage = () => {
  const { api } = useAuth();
  const {
    workDate,
    startTime,
    endTime,
    timeOptions,
    appointments,
    toggleWorking,
    setTime,
    isLoading,
    scheduleError,
    saveSuccess,
    loadSchedule,
    saveSchedule,
    clearScheduleError,
  } = useScheduleStore((state) => state);

  useEffect(() => {
    if (!api) return;
    loadSchedule(api);
  }, [loadSchedule, api]);

  useEffect(() => {
    if (!saveSuccess) return;
    const timer = setTimeout(() => clearScheduleError(), 3000);
    return () => clearTimeout(timer);
  }, [saveSuccess, clearScheduleError]);

  const handleSave = (reason) => {
    const actualReason = typeof reason === "string" ? reason : "";
    if (api) {
      saveSchedule(api, actualReason);
    }
  };

  const hasSchedule = useMemo(
    () => workDate && workDate.length > 0,
    [workDate],
  );

  const upcomingAppointmentsCount = useMemo(() => {
    if (!appointments || appointments.length === 0) return 0;
    const now = new Date();
    const next30Days = new Date();
    next30Days.setDate(now.getDate() + 30);

    return appointments.filter((app) => {
      const appDate = new Date(app.appointmentDate);
      return (
        appDate >= now &&
        appDate <= next30Days &&
        app.status !== "CANCELLED" &&
        app.status !== "REJECTED"
      );
    }).length;
  }, [appointments]);

  const workingDaysText = useMemo(() => {
    if (!hasSchedule) return "Chưa thiết lập";
    return workDate.map((d) => DAY_MAP[d] || d).join(", ");
  }, [workDate, hasSchedule]);

  const hasUpcoming = upcomingAppointmentsCount > 0;

  return {
    workDate,
    startTime,
    endTime,
    timeOptions,
    toggleWorking,
    setTime,
    isLoading,
    scheduleError,
    saveSuccess,
    clearScheduleError,
    handleSave,
    hasSchedule,
    upcomingAppointmentsCount,
    workingDaysText,
    hasUpcoming,
  };
};
