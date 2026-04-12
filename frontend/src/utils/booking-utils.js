export const STEPS = [
  { id: "service", label: "Dịch vụ" },
  { id: "doctor", label: "Bác sĩ" },
  { id: "day", label: "Ngày" },
  { id: "time", label: "Thời gian" },
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

export function formatTimeDisplay(isoString) {
  if (!isoString) return "";
  if (isoString.includes("T")) {
    return isoString.split("T")[1].substring(0, 5);
  }
  return isoString;
}
