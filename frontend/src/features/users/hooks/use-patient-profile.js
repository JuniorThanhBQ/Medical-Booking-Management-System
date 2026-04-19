import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "sonner";

import { endpoints } from "@/configs/apis";
import useAuth from "@/contexts/auth/AuthContext";

export const usePatientProfile = () => {
  const { appointmentId } = useParams();
  const navigate = useNavigate();
  const { user: contextUser, api } = useAuth();

  const [patientProfile, setPatientProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const fetchPatientData = async () => {
      if (!api || !appointmentId) return;

      setLoading(true);
      try {
        const response = await api.get(
          endpoints.appointment_patient_profile(appointmentId),
        );
        if (!mounted) return;
        setPatientProfile(response.data);
        setError("");
      } catch (err) {
        if (!mounted) return;
        const errorMessage =
          err.response?.data?.message || "Không thể tải hồ sơ bệnh nhân.";
        setError(errorMessage);
        toast.error(errorMessage);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchPatientData();

    return () => {
      mounted = false;
    };
  }, [appointmentId, api]);

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

  const formatDate = (dateString) => {
    if (!dateString) return "Chưa cập nhật";
    try {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat("vi-VN").format(date);
    } catch {
      return dateString;
    }
  };

  const getGenderText = (gender) => {
    if (gender === "MALE") return "Nam";
    if (gender === "FEMALE") return "Nữ";
    return "Khác";
  };

  const handleGoBack = () => navigate(-1);
  const handleRetry = () => window.location.reload();

  return {
    patientProfile,
    loading,
    error,
    contextUser,
    displayName,
    formatDate,
    getGenderText,
    handleGoBack,
    handleRetry,
  };
};
