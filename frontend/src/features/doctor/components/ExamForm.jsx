import TreatmentOrderForm from "./TreatmentOrderForm";
import { toast } from "sonner";

export default function ExamForm({
  formData,
  onChange,
  onSaveDraft,
  onComplete,
  isCompleted,
}) {
  function handleChange(field) {
    return (e) => onChange({ ...formData, [field]: e.target.value });
  }

  function handleTreatmentChange(value) {
    onChange({ ...formData, treatmentOrders: value });
  }

  return (
    <div className="exam__form">
      <div className="exam__form-group">
        <label className="exam__label" htmlFor="diagnosis">
          Chẩn đoán
        </label>
        <textarea
          id="diagnosis"
          className="exam__textarea"
          placeholder="Nhập chẩn đoán..."
          rows={3}
          value={formData.diagnosis}
          onChange={handleChange("diagnosis")}
          disabled={isCompleted}
        />
      </div>

      <div className="exam__form-group">
        <label className="exam__label" htmlFor="notes">
          Ghi chú
        </label>
        <textarea
          id="notes"
          className="exam__textarea"
          placeholder="Triệu chứng, quan sát lâm sàng..."
          rows={3}
          value={formData.notes}
          onChange={handleChange("notes")}
          disabled={isCompleted}
        />
      </div>

      <div className="exam__form-group">
        <label className="exam__label" htmlFor="prescription">
          Đơn thuốc
        </label>
        <textarea
          id="prescription"
          className="exam__textarea"
          placeholder={
            "Mỗi thuốc một dòng. Ví dụ:\nParacetamol 500mg (2 lần/ngày)"
          }
          rows={3}
          value={formData.prescriptionText}
          onChange={handleChange("prescriptionText")}
          disabled={isCompleted}
        />
      </div>

      <TreatmentOrderForm
        value={formData.treatmentOrders}
        onChange={handleTreatmentChange}
        disabled={isCompleted}
      />

      {!isCompleted && (
        <div className="exam__actions">
          <button
            type="button"
            className="exam__btn exam__btn--secondary"
            onClick={onSaveDraft}
          >
            Lưu nháp
          </button>
          <button
            type="button"
            className="exam__btn exam__btn--primary"
            onClick={() => {
              if (!formData.diagnosis.trim()) {
                toast.error("Vui lòng nhập chẩn đoán trước khi hoàn tất.");
                return;
              }
              if (
                window.confirm(
                  "Xác nhận hoàn tất khám? Không thể chỉnh sửa sau khi hoàn tất.",
                )
              ) {
                onComplete();
              }
            }}
          >
            Hoàn tất khám
          </button>
        </div>
      )}

      {isCompleted && <p className="exam__completed-badge">Đã hoàn tất khám</p>}
    </div>
  );
}
