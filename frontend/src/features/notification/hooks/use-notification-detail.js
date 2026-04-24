import useNotification from "@contexts/notifications/NotificationContext";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";

export const useNotificationDetail = () => {
  const { notificationId } = useParams();
  const { getNotificationDetail } = useNotification();
  const { user: contextUser } = useAuth();
  const navigate = useNavigate();

  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const loadDetail = async () => {
      if (!notificationId) return;
      setLoading(true);
      try {
        const result = await getNotificationDetail(notificationId);
        if (!mounted) return;
        setNotification(result);
        setError("");
      } catch {
        if (!mounted) return;
        setError("Không thể tải chi tiết thông báo.");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadDetail();

    return () => {
      mounted = false;
    };
  }, [notificationId, getNotificationDetail]);

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

  const appointmentId = notification?.appointment_id;

  const handleViewAppointment = () => {
    if (!appointmentId) return;
    navigate(`/appointments/${appointmentId}`);
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  const formatDate = (dateString) => {
    if (!dateString) return "&#8212;";
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

  return {
    notification,
    loading,
    error,
    contextUser,
    displayName,
    appointmentId,
    handleViewAppointment,
    handleGoBack,
    formatDate,
  };
};
