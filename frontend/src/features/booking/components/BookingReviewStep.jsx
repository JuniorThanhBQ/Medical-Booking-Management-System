import { toISODate, formatTimeDisplay } from "@/utils/booking-utils.js";

export function BookingReviewStep({
  specialtyName,
  selectedDate,
  selectedTime,
  selectedDoctorName,
  patientNotes,
  onPatientNotesChange,
  onConfirm,
  canConfirm,
  submitting = false,
  submitError = null,
}) {
  return (
    <div className="booking__confirm-layout">
      <div className="booking__step-panel">
        <h2 className="booking__panel-title">Xác nhận thông tin</h2>
        <p className="booking__panel-subtitle">
          Kiểm tra thông tin trước khi xác nhận.
        </p>

        <div className="booking__confirm">
          <div className="booking__confirm-row">
            <span className="booking__confirm-label">Chuyên khoa</span>
            <span className="booking__confirm-value">{specialtyName}</span>
          </div>

          <div className="booking__confirm-row">
            <span className="booking__confirm-label">Ngày</span>
            <span className="booking__confirm-value">
              {selectedDate ? toISODate(selectedDate) : "—"}
            </span>
          </div>

          <div className="booking__confirm-row">
            <span className="booking__confirm-label">Thời gian</span>
            <span className="booking__confirm-value">
              {selectedTime ? formatTimeDisplay(selectedTime) : "—"}
            </span>
          </div>

          <div className="booking__confirm-row">
            <span className="booking__confirm-label">Bác sĩ</span>
            <span className="booking__confirm-value">
              {selectedDoctorName || "—"}
            </span>
          </div>

          <div className="booking__notes">
            <label className="booking__notes-label" htmlFor="notes">
              Ghi chú (tùy chọn)
            </label>
            <textarea
              id="notes"
              className="booking__notes-input"
              placeholder="Bất kỳ triệu chứng, sở thích hay câu hỏi nào cho bác sĩ..."
              value={patientNotes}
              onChange={(e) => onPatientNotesChange(e.target.value)}
            />
          </div>
        </div>

        <div className="booking__confirm-actions">
          <button
            type="button"
            className="booking__primary"
            onClick={onConfirm}
            disabled={!canConfirm || submitting}
          >
            {submitting ? "Đang xử lý..." : "Xác nhận lịch hẹn"}
          </button>

          {submitError && (
            <p className="booking__error">{submitError}</p>
          )}

          <p className="booking__hint">
            Bằng việc xác nhận, bạn đồng ý thông tin trên là chính xác.
          </p>
        </div>
      </div>

      <aside className="booking__summary">
        <div className="booking__summary-card">
          <div className="booking__summary-title">Đặt lịch</div>

          <div className="booking__summary-row">
            <span className="booking__summary-label">Chuyên khoa</span>
            <span className="booking__summary-value">
              {specialtyName}
            </span>
          </div>

          <div className="booking__summary-row">
            <span className="booking__summary-label">Ngày</span>
            <span className="booking__summary-value">
              {selectedDate ? toISODate(selectedDate) : "—"}
            </span>
          </div>

          <div className="booking__summary-row">
            <span className="booking__summary-label">Thời gian</span>
            <span className="booking__summary-value">
              {selectedTime ? formatTimeDisplay(selectedTime) : "—"}
            </span>
          </div>

          <div className="booking__summary-row">
            <span className="booking__summary-label">Bác sĩ</span>
            <span className="booking__summary-value">
              {selectedDoctorName || "—"}
            </span>
          </div>

          <div className="booking__summary-foot">
            <div className="booking__summary-foot-title">
              Quy trình
            </div>
            <div className="booking__summary-foot-desc">
              Chọn ngày → thời gian → bác sĩ → xác nhận.
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
}