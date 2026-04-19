import { formatDayLabel, toISODate } from "@utils/booking-utils";

import { BookingPanelHeader } from "./BookingPanelHeader";

export function BookingDayStep({
  availableDays,
  selectedDate,
  onSelectDate,
  onNext,
}) {
  return (
    <div className="booking__step-panel">
      <BookingPanelHeader
        onNext={onNext}
        title="Chọn ngày"
        disabled={!selectedDate}
      />
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
    </div>
  );
}
