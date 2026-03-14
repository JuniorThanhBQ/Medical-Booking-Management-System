import { toISODate } from "../../utils/booking-utils";
import { BookingPanelHeader } from "./booking-panel-header";

export function BookingTimeStep({
  timeSlots,
  selectedDate,
  selectedTime,
  onSelectTime,
  onNext,
}) {
  return (
    <div className="booking__step-panel">
      <BookingPanelHeader onNext={onNext} title="Chọn thời gian" />
      <p className="booking__panel-subtitle">
        {selectedDate
          ? `Thời gian có sẵn cho ${toISODate(selectedDate)}`
          : "Vui lòng chọn ngày trước."}
      </p>
      <div className="booking__times">
        {timeSlots.map((t) => {
          const isSelected = selectedTime === t;
          return (
            <button
              key={t}
              type="button"
              className={`booking__time${
                isSelected ? " booking__time--selected" : ""
              }`}
              onClick={() => onSelectTime(t)}
            >
              {t}
            </button>
          );
        })}
      </div>
    </div>
  );
}
