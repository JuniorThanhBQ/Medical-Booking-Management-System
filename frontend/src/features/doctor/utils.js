import { APPOINTMENT_STATUS, OPEN_HOURS } from "@/configs/const";

export function buildDefaultDaySchedule(day) {
  const defaultRange = {
    id: `${day}-range-1`,
    start: `${String(OPEN_HOURS.start).padStart(2, "0")}:00`,
    end: `${String(OPEN_HOURS.end).padStart(2, "0")}:00`,
  };

  const isWeekend = day === "Sat" || day === "Sun";

  return {
    day,
    isWorking: !isWeekend,
    ranges: [defaultRange],
  };
}

export function generateTimeOptions() {
  const options = [];
  for (let hour = OPEN_HOURS.start; hour <= OPEN_HOURS.end; hour += 1) {
    options.push(`${String(hour).padStart(2, "0")}:00`);
    options.push(`${String(hour).padStart(2, "0")}:30`);
  }
  return options;
}