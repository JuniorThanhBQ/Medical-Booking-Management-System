const APPOINTMENT_STATUS_TO_UI = {
  APPROVED: "APPROVED",
  COMPLETED: "COMPLETED",
  PENDING: "PENDING",
  CANCEL: "CANCEL",
};

export const EMPTY_PATIENT = {
  dateOfBirth: null,
  gender: null,
};

function toViTime(isoString) {
  if (!isoString) return "";
  const date = new Date(isoString);
  if (isNaN(date.getTime())) return "";

  const timePart = isoString.split("T")[1];
  return timePart ? timePart.substring(0, 5) : "";
}

function getDefaultEndTime(startTime) {
  if (!startTime) return "";

  const [hourText, minuteText] = startTime.split(":");
  const hour = Number(hourText);
  const minute = Number(minuteText);
  if (Number.isNaN(hour) || Number.isNaN(minute)) return "";

  const endHour = (hour + 1).toString().padStart(2, "0");
  return `${endHour}:${minuteText}`;
}

export function normalizeDoctorAppointment(appointment, patientProfile) {
  const appointmentDate = appointment?.appointmentDate || "";
  const startTime = appointment?.startTime || toViTime(appointmentDate);
  const endTime = appointment?.endTime || getDefaultEndTime(startTime);

  return {
    id: appointment?.id ?? "",
    patientId: appointment?.patientId || "",
    patientName: appointment?.patientName || "Không rõ bệnh nhân",
    status: appointment?.status || "",
    statusDisplay:
      APPOINTMENT_STATUS_TO_UI[appointment?.status] ||
      appointment?.status ||
      "",

    appointmentDate,
    startTime,
    endTime,
    dateOfBirth: patientProfile?.dateOfBirth ?? null,
    gender: patientProfile?.gender ?? null,
  };
}

export function isTodayAppointment(isoString) {
  if (!isoString) return false;

  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return false;

  const appointmentDateString = date.toLocaleDateString("en-CA", {
    timeZone: "Asia/Ho_Chi_Minh",
  });

  const todayString = new Date().toLocaleDateString("en-CA", {
    timeZone: "Asia/Ho_Chi_Minh",
  });

  return appointmentDateString === todayString;
}
