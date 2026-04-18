import { BookingPanelHeader } from "./BookingPanelHeader";

export function BookingDoctorStep({
  doctorsForSpecialty,
  selectedDoctorId,
  onSelectDoctor,
  onNext,
}) {
  return (
    <div className="booking__step-panel">
      <BookingPanelHeader onNext={onNext} title="Chọn bác sĩ" disabled={!selectedDoctorId} />
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
                    {`${d.firstName[0]}${d.lastName[0]}`.toUpperCase()}
                  </div>
                  <div>
                    <div className="booking__doctor-name">
                      {d.firstName} {d.lastName}
                    </div>
                    <div className="booking__doctor-title">{d.title}</div>
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
