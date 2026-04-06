import { toISODate, formatTimeDisplay } from "../../utils/booking-utils";
import { BookingPanelHeader } from "./BookingPanelHeader";

export function BookingTimeStep({
  timeSlots,
  selectedDate,
  selectedTime,
  onSelectTime,
  onNext,
  loading = false,
}) {
  return (
    <div className="booking__step-panel">
      <BookingPanelHeader onNext={onNext} title="Chọn thời gian" />
      <p className="booking__panel-subtitle">
        {selectedDate
          ? `Thời gian có sẵn cho ${toISODate(selectedDate)}`
          : "Vui lòng chọn ngày trước."}
      </p>
      {loading ? (
        <p className="booking__loading-text">Đang tải khung giờ...</p>
      ) : timeSlots.length === 0 ? (
        <p className="booking__empty-text">Không có khung giờ trống. Vui lòng chọn bác sĩ hoặc ngày khác.</p>
      ) : (
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
                {formatTimeDisplay(t)}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
