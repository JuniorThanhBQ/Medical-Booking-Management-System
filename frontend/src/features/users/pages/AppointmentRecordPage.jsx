import { useParams, useNavigate } from "react-router-dom";
import "@/assets/css/users/appointment-record.css";
import Navbar from "../components/Navbar";
import { useExamStore } from "../../doctor/hooks/use-exam-store";

export default function AppointmentRecordPage() {
  const { appointmentId } = useParams();
  const navigate = useNavigate();
  const getRecord = useExamStore((s) => s.getRecord);

  const record = getRecord(appointmentId);

  return (
    <>
      <Navbar />

      <main className="record-page">
        <button
          type="button"
          className="record-page__back"
          onClick={() => navigate(-1)}
        >
          ← Quay lại
        </button>

        {!record ? (
          <p className="record-page__empty">
            Chưa có kết quả khám cho lịch hẹn này.
          </p>
        ) : (
          <div className="record-page__card">
            <header className="record-page__card-header">
              <h1 className="record-page__card-title">Kết quả khám bệnh</h1>
              <p className="record-page__card-meta">
                Bác sĩ: {record.doctorName || "—"} ·{" "}
                {new Date(record.createdAt).toLocaleDateString("vi-VN")}
              </p>
            </header>

            <section className="record-page__section">
              <h2 className="record-page__section-title">Chẩn đoán</h2>
              <p className="record-page__section-content">
                {record.diagnosis || "—"}
              </p>
            </section>

            <section className="record-page__section">
              <h2 className="record-page__section-title">Ghi chú</h2>
              <p className="record-page__section-content">
                {record.notes || "—"}
              </p>
            </section>

            <section className="record-page__section">
              <h2 className="record-page__section-title">Đơn thuốc</h2>
              <p className="record-page__section-content" style={{ whiteSpace: "pre-line" }}>
                {record.prescriptionText || "—"}
              </p>
            </section>

            {record.treatmentOrders && (
              <section className="record-page__section">
                <h2 className="record-page__section-title">
                  Chỉ định xét nghiệm / điều trị
                </h2>
                <p className="record-page__section-content">
                  {record.treatmentOrders}
                </p>
              </section>
            )}
          </div>
        )}
      </main>
    </>
  );
}
