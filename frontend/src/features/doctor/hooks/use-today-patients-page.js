import { useEffect, useMemo, useState } from "react";

import { APPOINTMENT_STATUS } from "@/configs/const";
import useAuth from "@/contexts/auth/AuthContext";

import { fetchDoctorTodayPatients } from "../services/appointments-api.js";
import { useExamStore } from "./use-exam-store.js";

export const useTodayPatientsPage = () => {
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

  return {
    activeFilter,
    setActiveFilter,
    loading,
    error,
    filtered,
    processedAppointments,
    getPatientHistory,
  };
};
