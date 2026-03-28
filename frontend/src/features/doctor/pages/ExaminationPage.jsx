import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "@/assets/css/users/examination.css";
import Navbar from "../../users/components/Navbar";
import { EXAM_STATUS } from "@/configs/const";
import { mockTodayAppointments } from "@/data/mocks/doctor-schedule";
import { mockPatients } from "@/data/mocks/patients";
import { useExamStore } from "../hooks/use-exam-store";
import PatientHistoryPanel from "../components/PatientHistoryPanel";
import ExamForm from "../components/ExamForm";
import { getStoredUser } from "@/utils/auth-helpers";

const EMPTY_FORM = {
  diagnosis: "",
  notes: "",
  prescriptionText: "",
  treatmentOrders: "",
};

export default function ExaminationPage() {
  const { appointmentId } = useParams();
  const navigate = useNavigate();
  const saveRecord = useExamStore((s) => s.saveRecord);
  const getRecord = useExamStore((s) => s.getRecord);
  const getPatientHistory = useExamStore((s) => s.getPatientHistory);
  const completeExam = useExamStore((s) => s.completeExam);

  const appointment = mockTodayAppointments.find((a) => a.id === appointmentId);
  const patient = appointment
    ? mockPatients.find((p) => p.id === appointment.patientId)
    : null;

  const user = getStoredUser();
  const doctorName = user?.name || "Bác sĩ";

  const [formData, setFormData] = useState(EMPTY_FORM);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    const existing = getRecord(appointmentId);
    if (existing) {
      setFormData({
        diagnosis: existing.diagnosis || "",
        notes: existing.notes || "",
        prescriptionText: existing.prescriptionText || "",
        treatmentOrders: existing.treatmentOrders || "",
      });
      setIsCompleted(existing.status === EXAM_STATUS.COMPLETED);
    }
  }, [appointmentId]);

  if (!appointment) {
    return (
      <>
        <Navbar />
        <main className="exam-page">
          <p className="exam-page__error">
            Không tìm thấy lịch hẹn. <a href="/doctor/today">Quay lại</a>
          </p>
        </main>
      </>
    );
  }

  const history = getPatientHistory(appointment.patientId);

  function handleSaveDraft() {
    saveRecord(appointmentId, {
      ...formData,
      patientId: appointment.patientId,
      doctorName,
    });
  }

  function handleComplete() {
    completeExam(appointmentId, {
      ...formData,
      patientId: appointment.patientId,
      doctorName,
    });
    setIsCompleted(true);
  }

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

        <div className="exam-page__layout">
          <PatientHistoryPanel
            patient={patient}
            notes={appointment.notes}
            history={history}
          />

          <ExamForm
            formData={formData}
            onChange={setFormData}
            onSaveDraft={handleSaveDraft}
            onComplete={handleComplete}
            isCompleted={isCompleted}
          />
        </div>
      </main>
    </>
  );
}
