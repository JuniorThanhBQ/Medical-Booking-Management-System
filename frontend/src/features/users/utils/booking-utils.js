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

export function buildTimeSlots() {
  const slots = [];
  for (let hour = OPEN_HOURS.start; hour <= OPEN_HOURS.end; hour += 1) {
    slots.push(`${String(hour).padStart(2, "0")}:00`);
    slots.push(`${String(hour).padStart(2, "0")}:30`);
  }
  return slots;
}

// use api instead of local storage
// export function loadAppointments() {
//   try {
//     const raw = localStorage.getItem("appointments");
//     const parsed = raw ? JSON.parse(raw) : [];
//     return Array.isArray(parsed) ? parsed : [];
//   } catch {
//     return [];
//   }
// }

// export function saveAppointment(appointment) {
//   const current = loadAppointments();
//   localStorage.setItem("appointments", JSON.stringify([appointment, ...current]));
// }
