import "@css/doctor/examination.css";

import { useExaminationPage } from "@features/doctor/hooks/use-examination-page";
import Navbar from "@features/users/components/Navbar";

import ExamForm from "../components/ExamForm";
import PatientHistoryPanel from "../components/PatientHistoryPanel";

export default function ExaminationPage() {
  const {
    navigate,
    examination,
    setExamFormData,
    handleSaveDraft,
    handleComplete,
    hasNotFound,
  } = useExaminationPage();

  return (
    <>
      <Navbar />

      <main className="exam-page">
        <button
          type="button"
          className="exam-page__back"
          onClick={() => navigate("/doctor/today")}
        >
          &#8592; Quay lại
        </button>

        <h1 className="exam-page__title">Phiếu khám bệnh</h1>

        {examination.loading && (
          <p className="exam-page__error">Đang tải dữ liệu khám bệnh...</p>
        )}
        {!examination.loading && examination.error && (
          <p className="exam-page__error">{examination.error}</p>
        )}
        {hasNotFound && (
          <p className="exam-page__error">
            Không tìm thấy lịch hẹn. <a href="/doctor/today">Quay lại</a>
          </p>
        )}

        {!examination.loading &&
          !examination.error &&
          examination.appointment && (
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
