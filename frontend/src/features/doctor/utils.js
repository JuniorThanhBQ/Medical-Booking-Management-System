import { OPEN_HOURS } from "@/configs/const";

export function generateTimeOptions() {
  const options = [];
  for (let hour = OPEN_HOURS.start; hour <= OPEN_HOURS.end; hour += 1) {
    options.push(`${String(hour).padStart(2, "0")}:00`);
    options.push(`${String(hour).padStart(2, "0")}:30`);
  }
  return options;
}
