import { getAppointmentDetail } from "@features/users/services/appointment-api-service";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

export const useAppointmentDetail = () => {
  const { appointmentId: id } = useParams();
  const navigate = useNavigate();
  const { user: contextUser, api } = useAuth();

  const [appointment, setAppointment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const fetchDetail = async () => {
      if (!api || !id) return;

      setLoading(true);
      try {
        const data = await getAppointmentDetail(api, id);
        if (!mounted) return;
        setAppointment(data);
        setError("");
      } catch (err) {
        if (!mounted) return;
        const errorMessage =
          err.response?.data?.message || "Không thể tải thông vị lịch hẹn.";
        setError(errorMessage);
        toast.error(errorMessage);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchDetail();

    return () => {
      mounted = false;
    };
  }, [id, api]);

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

  const getStatusDisplay = (status) => {
    const statusMap = {
      APPROVED: { text: "Đã xác nhận", className: "ad-badge--green" },
      PENDING: { text: "Chờ xác nhận", className: "ad-badge--yellow" },
      CANCELLED: { text: "Đã hủy", className: "ad-badge--red" },
      COMPLETED: { text: "Đã hoàn thành", className: "ad-badge--blue" },
    };
    return statusMap[status] || { text: status, className: "ad-badge--gray" };
  };

  const formatDate = (dateString) => {
    if (!dateString) return "—";
    try {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      }).format(date);
    } catch {
      return dateString;
    }
  };

  const statusInfo = getStatusDisplay(appointment?.status);
  const handleGoBack = () => navigate(-1);
  const handleViewPatientProfile = () =>
    navigate(`appointments/${id}/patient-profile`);
  const handleRetry = () => window.location.reload();

  return {
    appointment,
    loading,
    error,
    contextUser,
    displayName,
    statusInfo,
    formatDate,
    handleGoBack,
    handleViewPatientProfile,
    handleRetry,
    id,
  };
};
