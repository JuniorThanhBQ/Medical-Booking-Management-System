import {
  formatDayLabel,
  formatTimeDisplay,
  toISODate,
} from "@/utils/booking-utils.js";

import { BookingPanelHeader } from "./BookingPanelHeader";

export function BookingDateTimeStep({
  availableDays,
  selectedDate,
  onSelectDate,
  timeSlots,
  selectedTime,
  onSelectTime,
  onNext,
  loading = false,
}) {
  return (
    <div className="booking__step-panel">
      <BookingPanelHeader onNext={onNext} title="Chọn ngày & thời gian" />

      <p className="booking__panel-subtitle">
        Chọn một trong {availableDays.length} ngày tiếp theo.
      </p>

      <div className="booking__choice-grid">
        {availableDays.map((d) => {
          const isSelected =
            selectedDate && toISODate(selectedDate) === toISODate(d);

          return (
            <button
              key={toISODate(d)}
              type="button"
              className={`booking__choice${
                isSelected ? " booking__choice--selected" : ""
              }`}
              onClick={() => onSelectDate(d)}
            >
              <div className="booking__choice-title">{formatDayLabel(d)}</div>
              <div className="booking__choice-meta">{toISODate(d)}</div>
            </button>
          );
        })}
      </div>

      <p className="booking__panel-subtitle" style={{ marginTop: "16px" }}>
        {selectedDate
          ? `Thời gian có sẵn cho ${toISODate(selectedDate)}`
          : "Vui lòng chọn ngày trước."}
      </p>

      {loading ? (
        <p className="booking__loading-text">Đang tải khung giờ...</p>
      ) : !selectedDate ? null : timeSlots.length === 0 ? (
        <p className="booking__empty-text">
          Không có khung giờ trống. Vui lòng chọn ngày khác.
        </p>
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
