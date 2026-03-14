import { toISODate } from "../../utils/booking-utils";
import { BookingPanelHeader } from "./booking-panel-header";

export function BookingDoctorStep({
  doctorsForSpecialty,
  selectedDate,
  selectedTime,
  selectedDoctorId,
  onSelectDoctor,
  onNext,
}) {
  return (
    <div className="booking__step-panel">
      <BookingPanelHeader onNext={onNext} title="Chọn bác sĩ" />
      <p className="booking__panel-subtitle">Chọn bác sĩ bạn muốn gặp.</p>
      <div className="booking__doctors">
        {doctorsForSpecialty.length === 0 ? (
          <div className="booking__empty">
            Không có bác sĩ nào có sẵn cho chuyên khoa này.
          </div>
        ) : (
          doctorsForSpecialty.map((d) => {
            const isSelected = selectedDoctorId === d.id;
            return (
              <button
                key={d.id}
                type="button"
                className={`booking__doctor${
                  isSelected ? " booking__doctor--selected" : ""
                }`}
                onClick={() => onSelectDoctor(d.id)}
              >
                <div className="booking__doctor-head">
                  <div className="booking__avatar" aria-hidden="true">
                    {d.name
                      .split(" ")
                      .slice(0, 2)
                      .map((x) => x[0])
                      .join("")
                      .toUpperCase()}
                  </div>
                  <div>
                    <div className="booking__doctor-name">{d.name}</div>
                    <div className="booking__doctor-title">
                      {d.title} · {d.location}
                    </div>
                  </div>
                </div>
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}
