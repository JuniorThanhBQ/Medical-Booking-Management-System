import { BookingPanelHeader } from "./BookingPanelHeader";

export function BookingServiceStep({
  medicalServices,
  selectedMedicalServiceId,
  onSelectService,
  onNext,
}) {
  return (
    <div className="booking__step-panel">
      <BookingPanelHeader onNext={onNext} title="Chọn dịch vụ" />
      <p className="booking__panel-subtitle">Chọn dịch vụ y tế bạn cần.</p>
      <div className="booking__services">
        {medicalServices.length === 0 ? (
          <div className="booking__empty">
            Không có dịch vụ nào có sẵn cho chuyên khoa này.
          </div>
        ) : (
          medicalServices.map((s) => {
            const isSelected = selectedMedicalServiceId === s.id;
            return (
              <button
                key={s.id}
                type="button"
                className={`booking__service${
                  isSelected ? " booking__service--selected" : ""
                }`}
                onClick={() => onSelectService(s.id)}
              >
                <div className="booking__service-name">{s.name}</div>
                {s.price && (
                  <div className="booking__service-price">
                    {new Intl.NumberFormat("vi-VN", {
                      style: "currency",
                      currency: "VND",
                    }).format(s.price)}
                  </div>
                )}
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}
