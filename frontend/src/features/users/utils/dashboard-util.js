import { AVAILABLE_BOOKING_DAYS } from "@/configs/const";
export function validateAppointmentDate(date) {
  if (!date) return { isValid: false, error: "Vui lòng chọn ngày khám." };

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const max = new Date(today);
  max.setDate(max.getDate() + AVAILABLE_BOOKING_DAYS);

  const selected = new Date(date);
  selected.setHours(0, 0, 0, 0);

  if (Number.isNaN(selected.getTime()) || selected < today || selected > max) {
    return {
      isValid: false,
      error: `Ngày khám không hợp lệ. Vui lòng chọn trong ${AVAILABLE_BOOKING_DAYS} ngày tới.`,
    };
  }

  return { isValid: true, error: "" };
}
