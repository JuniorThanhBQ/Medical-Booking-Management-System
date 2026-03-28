import { useState, useMemo } from "react";
import "@/assets/css/users/today-patients.css";
import Navbar from "../../users/components/Navbar";
import { APPOINTMENT_STATUS } from "@/configs/const";
import { mockTodayAppointments } from "@/data/mocks/doctor-schedule";
import { mockPatients } from "@/data/mocks/patients";
import { useExamStore } from "../hooks/use-exam-store";
import PatientCard from "../components/PatientCard";

const FILTER_TABS = [
  { key: "all", label: "Tất cả" },
  { key: APPOINTMENT_STATUS.CONFIRMED, label: "Chờ khám" },
  { key: APPOINTMENT_STATUS.IN_PROGRESS, label: "Đang khám" },
  { key: APPOINTMENT_STATUS.COMPLETED, label: "Đã khám" },
];

export default function TodayPatientsPage() {
  const [activeFilter, setActiveFilter] = useState("all");
  const getPatientHistory = useExamStore((s) => s.getPatientHistory);

  const visibleAppointments = useMemo(
    () => mockTodayAppointments.filter((a) => a.status !== APPOINTMENT_STATUS.PENDING),
    []
  );

  const filtered = useMemo(() => {
    if (activeFilter === "all") return visibleAppointments;
    return visibleAppointments.filter((a) => a.status === activeFilter);
  }, [activeFilter, visibleAppointments]);

  return (
    <>
      <Navbar />

      <main className="today-patients">
        <header className="today-patients__header">
          <p className="today-patients__eyebrow">Bệnh nhân hôm nay</p>
          <h1 className="today-patients__title">Danh sách khám</h1>
          <p className="today-patients__subtitle">
            {visibleAppointments.length} bệnh nhân · {new Date().toLocaleDateString("vi-VN")}
          </p>
        </header>

        <div className="today-patients__filters">
          {FILTER_TABS.map((tab) => (
            <button
              key={tab.key}
              type="button"
              className={`today-patients__filter-tab${activeFilter === tab.key ? " today-patients__filter-tab--active" : ""}`}
              onClick={() => setActiveFilter(tab.key)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="today-patients__list">
          {filtered.length === 0 && (
            <p className="today-patients__empty">Không có bệnh nhân nào.</p>
          )}
          {filtered.map((appointment) => {
            const patient = mockPatients.find((p) => p.id === appointment.patientId);
            const history = getPatientHistory(appointment.patientId);
            const lastRecord = history.length > 0 ? history[history.length - 1] : null;

            return (
              <PatientCard
                key={appointment.id}
                appointment={appointment}
                patient={patient}
                lastRecord={lastRecord}
              />
            );
          })}
        </div>
      </main>
    </>
  );
}
