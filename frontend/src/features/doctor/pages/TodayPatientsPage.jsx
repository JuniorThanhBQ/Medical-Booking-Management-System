import "@css/doctor/patient-tab.css";

import Navbar from "@features/users/components/Navbar";
import { useEffect, useMemo, useState } from "react";

import { APPOINTMENT_STATUS } from "@/configs/const";
import useAuth from "@/contexts/auth/AuthContext";

import PatientCard from "../components/PatientCard";
import { useExamStore } from "../hooks/use-exam-store";
import { fetchDoctorTodayPatients } from "../services/appointments-api.js";

const FILTER_TABS = [
  { key: "all", label: "Tất cả" },
  { key: APPOINTMENT_STATUS.CONFIRMED, label: "Chờ khám" },
  { key: APPOINTMENT_STATUS.IN_PROGRESS, label: "Đang khám" },
  { key: APPOINTMENT_STATUS.COMPLETED, label: "Đã khám" },
];

export default function TodayPatientsPage() {
  const { api, accessToken } = useAuth();
  const [activeFilter, setActiveFilter] = useState("all");
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [currentTime, setCurrentTime] = useState(new Date().getTime());

  const getPatientHistory = useExamStore((s) => s.getPatientHistory);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().getTime());
    }, 60000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    let mounted = true;

    const loadTodayPatients = async () => {
      if (!accessToken) {
        if (!mounted) return;
        setAppointments([]);
        setError("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.");
        setLoading(false);
        return;
      }

      setLoading(true);
      try {
        const result = await fetchDoctorTodayPatients(api);

        if (!mounted) return;
        setAppointments(Array.isArray(result) ? result : []);
        setError("");
      } catch {
        if (!mounted) return;
        setAppointments([]);
        setError("Không thể tải danh sách bệnh nhân hôm nay.");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadTodayPatients();

    return () => {
      mounted = false;
    };
  }, [api, accessToken]);

  const processedAppointments = useMemo(() => {
    return appointments
      .filter(
        (a) =>
          a.status !== APPOINTMENT_STATUS.PENDING && a.status !== "CANCELLED",
      )
      .map((app) => {
        const appTime = new Date(app.appointmentDate).getTime();
        const isReady = currentTime >= appTime;

        let tabStatus = app.status;

        if (app.status !== APPOINTMENT_STATUS.COMPLETED) {
          tabStatus = isReady
            ? APPOINTMENT_STATUS.IN_PROGRESS
            : APPOINTMENT_STATUS.CONFIRMED;
        }

        return {
          ...app,
          tabStatus,
          canExamine: isReady,
        };
      });
  }, [appointments, currentTime]);

  const filtered = useMemo(() => {
    if (activeFilter === "all") return processedAppointments;
    return processedAppointments.filter((a) => a.tabStatus === activeFilter);
  }, [activeFilter, processedAppointments]);

  return (
    <>
      <Navbar />

      <main className="today-patients">
        <header className="today-patients__header">
          <p className="today-patients__eyebrow">Bệnh nhân hôm nay</p>
          <h1 className="today-patients__title">Danh sách khám</h1>
          <p className="today-patients__subtitle">
            {processedAppointments.length} bệnh nhân ·{" "}
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
