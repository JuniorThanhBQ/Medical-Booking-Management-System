import "@css/doctor/patient-tab.css";

import { useTodayPatientsPage } from "@features/doctor/hooks/use-today-patients-page";
import Navbar from "@features/users/components/Navbar";

import { APPOINTMENT_STATUS } from "@/configs/const";

import PatientCard from "../components/PatientCard";

const FILTER_TABS = [
  { key: "all", label: "Tất cả" },
  { key: APPOINTMENT_STATUS.CONFIRMED, label: "Chờ khám" },
  { key: APPOINTMENT_STATUS.IN_PROGRESS, label: "Đang khám" },
  { key: APPOINTMENT_STATUS.COMPLETED, label: "Đã khám" },
];

export default function TodayPatientsPage() {
  const {
    activeFilter,
    setActiveFilter,
    loading,
    error,
    filtered,
    processedAppointments,
    getPatientHistory,
  } = useTodayPatientsPage();

  return (
    <>
      <Navbar />

      <main className="today-patients">
        <header className="today-patients__header">
          <p className="today-patients__eyebrow">Bệnh nhân hôm nay</p>
          <h1 className="today-patients__title">Danh sách khám</h1>
          <p className="today-patients__subtitle">
            {processedAppointments.length} bệnh nhân &#183;{" "}
            {new Date().toLocaleDateString("vi-VN")}
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
          {loading && (
            <p className="today-patients__empty">
              Đang tải danh sách bệnh nhân...
            </p>
          )}

          {!loading && error && (
            <p className="today-patients__empty">{error}</p>
          )}

          {!loading && !error && filtered.length === 0 && (
            <p className="today-patients__empty">
              Không có bệnh nhân nào trong mục này.
            </p>
          )}

          {!loading &&
            !error &&
            filtered.map((appointment) => {
              const patient = {
                id: appointment.patientId,
                dateOfBirth: appointment.dateOfBirth,
                gender: appointment.gender,
              };
              const history = getPatientHistory(appointment.patientId);
              const lastRecord =
                history.length > 0 ? history[history.length - 1] : null;
              const now = new Date();

              const [datePart, timePart] =
                appointment.appointmentDate.split("T");
              const [year, month, day] = datePart.split("-").map(Number);
              const [hour, minute] = timePart.split(":").map(Number);
              const appointmentTime = new Date(
                year,
                month - 1,
                day,
                hour,
                minute,
              );

              const canExamine = now >= appointmentTime;

              return (
                <PatientCard
                  key={appointment.id}
                  appointment={appointment}
                  patient={patient}
                  lastRecord={lastRecord}
                  canExamine={canExamine}
                />
              );
            })}
        </div>
      </main>
    </>
  );
}
