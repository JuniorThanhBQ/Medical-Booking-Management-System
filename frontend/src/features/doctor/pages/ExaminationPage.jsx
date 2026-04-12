import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "@/assets/css/users/examination.css";
import Navbar from "@features/users/components/Navbar";
import { useExamStore } from "../hooks/use-exam-store";
import PatientHistoryPanel from "../components/PatientHistoryPanel";
import ExamForm from "../components/ExamForm";
import { getStoredUser } from "@/utils/auth-helpers";

export default function ExaminationPage() {
  const { appointmentId } = useParams();
  const navigate = useNavigate();
  const examination = useExamStore((s) => s.examination);
  const setExamFormData = useExamStore((s) => s.setExamFormData);
  const loadExamination = useExamStore((s) => s.loadExamination);
  const resetExaminationState = useExamStore((s) => s.resetExaminationState);
  const saveDraftToServer = useExamStore((s) => s.saveDraftToServer);
  const completeExamToServer = useExamStore((s) => s.completeExamToServer);

  const user = getStoredUser();
  const doctorName = user?.name || "Bác sĩ";

  useEffect(() => {
    loadExamination(appointmentId);

    return () => {
      resetExaminationState();
    };
  }, [appointmentId, loadExamination, resetExaminationState]);

  function handleSaveDraft() {
    saveDraftToServer(appointmentId, doctorName);
  }

  function handleComplete() {
    completeExamToServer(appointmentId, doctorName);
  }

  const hasNotFound = !examination.loading && !examination.error && !examination.appointment;

  return (
    <>
      <Navbar />

      <main className="exam-page">
        <button
          type="button"
          className="exam-page__back"
          onClick={() => navigate("/doctor/today")}
        >
          ← Quay lại
        </button>

        <h1 className="exam-page__title">Phiếu khám bệnh</h1>

        {examination.loading && <p className="exam-page__error">Đang tải dữ liệu khám bệnh...</p>}
        {!examination.loading && examination.error && (
          <p className="exam-page__error">{examination.error}</p>
        )}
        {hasNotFound && (
          <p className="exam-page__error">
            Không tìm thấy lịch hẹn. <a href="/doctor/today">Quay lại</a>
          </p>
        )}

        {!examination.loading && !examination.error && examination.appointment && (
          <div className="exam-page__layout">
            <PatientHistoryPanel
              patient={examination.patient}
              notes={examination.appointment.notes}
              history={examination.history}
            />

            <div>
              {examination.actionError && (
                <p className="exam-page__error">{examination.actionError}</p>
              )}
              <ExamForm
                formData={examination.formData}
                onChange={setExamFormData}
                onSaveDraft={handleSaveDraft}
                onComplete={handleComplete}
                isCompleted={examination.isCompleted}
              />
            </div>
          </div>
        )}
      </main>
    </>
  );
}
