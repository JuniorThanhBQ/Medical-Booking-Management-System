import { OPEN_HOURS } from "@/configs/const";

export const STEPS = [
  { id: "day", label: "Ngày" },
  { id: "time", label: "Thời gian" },
  { id: "doctor", label: "Bác sĩ" },
  { id: "confirm", label: "Xác nhận" },
];

export function formatDayLabel(date) {
  const weekday = date.toLocaleDateString("vi-VN", { weekday: "short" });
  const month = date.toLocaleDateString("vi-VN", { month: "short" });
  const day = date.toLocaleDateString("vi-VN", { day: "2-digit" });

  return `${weekday}, ${day} ${month}`;
}

export function toISODate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function buildTimeSlots(referenceDate) {
  const slots = [];
  const dateStr = referenceDate ? toISODate(referenceDate) : toISODate(new Date());
  for (let hour = OPEN_HOURS.start; hour <= OPEN_HOURS.end; hour += 1) {
    slots.push(`${dateStr}T${String(hour).padStart(2, "0")}:00:00Z`);
    slots.push(`${dateStr}T${String(hour).padStart(2, "0")}:30:00Z`);
  }
  return slots;
}

export function formatTimeDisplay(isoString) {
  if (!isoString) return "";
  const d = new Date(isoString);
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

