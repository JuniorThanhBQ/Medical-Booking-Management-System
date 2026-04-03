import { useEffect, useMemo, useState } from "react";
import "@/assets/css/users/today-patients.css";
import Navbar from "../../users/components/Navbar";
import { APPOINTMENT_STATUS } from "@/configs/const";
import { useExamStore } from "../hooks/use-exam-store";
import PatientCard from "../components/PatientCard";
import { fetchDoctorTodayPatients } from "../api/appointments-api";
import { getUserToken } from "@/utils/auth-helpers";

const FILTER_TABS = [
  { key: "all", label: "Tất cả" },
  { key: APPOINTMENT_STATUS.CONFIRMED, label: "Chờ khám" },
  { key: APPOINTMENT_STATUS.IN_PROGRESS, label: "Đang khám" },
  { key: APPOINTMENT_STATUS.COMPLETED, label: "Đã khám" },
];

export default function TodayPatientsPage() {
  const [activeFilter, setActiveFilter] = useState("all");
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const getPatientHistory = useExamStore((s) => s.getPatientHistory);

  useEffect(() => {
    let mounted = true;

    const loadTodayPatients = async () => {
      const token = getUserToken();
      if (!token) {
        if (!mounted) return;
        setAppointments([]);
        setError("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.");
        setLoading(false);
        return;
      }

      setLoading(true);
      try {
        const result = await fetchDoctorTodayPatients(token);
        if (!mounted) return;
        setAppointments(Array.isArray(result) ? result : []);
        setError("");
      } catch {
        if (!mounted) return;
        setAppointments([]);
        setError("Không thể tải danh sách bệnh nhân hôm nay.");
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadTodayPatients();

    return () => {
      mounted = false;
    };
  }, []);

  const visibleAppointments = useMemo(
    () => appointments.filter((a) => a.status !== APPOINTMENT_STATUS.PENDING),
    [appointments]
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
          {loading && (
            <p className="today-patients__empty">Đang tải danh sách bệnh nhân...</p>
          )}

          {!loading && error && (
            <p className="today-patients__empty">{error}</p>
          )}

          {!loading && !error && filtered.length === 0 && (
            <p className="today-patients__empty">Hôm nay chưa có bệnh nhân nào.</p>
          )}

          {!loading && !error && filtered.map((appointment) => {
            const patient = {
              id: appointment.patientId,
              dateOfBirth: appointment.dateOfBirth,
              gender: appointment.gender,
            };
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
