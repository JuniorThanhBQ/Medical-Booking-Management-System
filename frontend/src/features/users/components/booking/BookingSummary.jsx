import { toISODate, formatTimeDisplay } from "../../utils/booking-utils";

export function BookingSummary({
  specialtyName,
  selectedDate,
  selectedTime,
  selectedDoctorName,
}) {
  return (
    <aside className="booking__summary">
      <div className="booking__summary-card">
        <div className="booking__summary-title">Đặt lịch</div>
        <div className="booking__summary-row">
          <span className="booking__summary-label">Chuyên khoa</span>
          <span className="booking__summary-value">{specialtyName}</span>
        </div>
        <div className="booking__summary-row">
          <span className="booking__summary-label">Ngày</span>
          <span className="booking__summary-value">
            {selectedDate ? toISODate(selectedDate) : "—"}
          </span>
        </div>
        <div className="booking__summary-row">
          <span className="booking__summary-label">Thời gian</span>
          <span className="booking__summary-value">{selectedTime ? formatTimeDisplay(selectedTime) : "—"}</span>
        </div>
        <div className="booking__summary-row">
          <span className="booking__summary-label">Bác sĩ</span>
          <span className="booking__summary-value">
            {selectedDoctorName || "—"}
          </span>
        </div>
        <div className="booking__summary-foot">
          <div className="booking__summary-foot-title">Quy trình</div>
          <div className="booking__summary-foot-desc">
            Chọn ngày → thời gian → bác sĩ → xác nhận.
          </div>
        </div>
      </div>
    </aside>
  );
}
