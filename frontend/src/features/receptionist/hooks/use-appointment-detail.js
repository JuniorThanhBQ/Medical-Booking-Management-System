import { useReceptionistStore } from "@features/receptionist/hooks/use-receptionist-store";
import { useEffect, useState } from "react";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

export const useAppointmentDetailPage = (appointmentId) => {
  const { api } = useAuth();
  const {
    setApi,
    fetchAppointmentDetail,
    clearAppointmentDetail,
    appointmentDetail,
    loading,
    error,
    updateAppointmentStatus,
  } = useReceptionistStore();

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({ status: "", note: "" });

  useEffect(() => {
    if (api) setApi(api);
  }, [api, setApi]);

  useEffect(() => {
    if (!appointmentId || !api) return;
    fetchAppointmentDetail(appointmentId);
    return () => clearAppointmentDetail();
  }, [appointmentId, api, fetchAppointmentDetail, clearAppointmentDetail]);

  const handleSave = async () => {
    if (!api) return;
    try {
      await updateAppointmentStatus(appointmentId, formData);
      toast.success("Cập nhật thành công!");
      setIsEditing(false);
      fetchAppointmentDetail(appointmentId);
    } catch (err) {
      toast.error("Cập nhật thất bại: " + err.message);
    }
  };

  const handleEdit = () => {
    setFormData({
      status: appointmentDetail?.status || "PENDING",
      note: appointmentDetail?.note || "",
    });
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  return {
    appointmentDetail,
    loading,
    error,
    isEditing,
    formData,
    setFormData,
    handleSave,
    handleEdit,
    handleCancel,
  };
};
