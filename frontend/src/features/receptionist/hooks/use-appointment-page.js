import { useReceptionistStore } from "@features/receptionist/hooks/use-receptionist-store";
import { useEffect, useMemo, useState } from "react";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

export const useAppointmentsPage = () => {
  const { api } = useAuth();
  const {
    allAppointments,
    pagination,
    loading,
    fetchAllAppointments,
    updateAppointmentStatus,
    deleteAppointmentById,
    setApi,
  } = useReceptionistStore();

  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  useEffect(() => {
    if (api) {
      setApi(api);
    }
  }, [api, setApi]);

  useEffect(() => {
    if (api) {
      fetchAllAppointments({ page: currentPage, limit: 10 });
    }
  }, [currentPage, fetchAllAppointments, api]);

  const filteredAppointments = useMemo(() => {
    if (!allAppointments) return [];

    return allAppointments.filter((apt) => {
      const matchesStatus = statusFilter === "" || apt.status === statusFilter;

      const searchLower = searchTerm.toLowerCase();
      const matchesSearch =
        searchTerm === "" ||
        apt.patientName?.toLowerCase().includes(searchLower) ||
        apt.doctorName?.toLowerCase().includes(searchLower) ||
        apt.name?.toLowerCase().includes(searchLower);

      return matchesStatus && matchesSearch;
    });
  }, [allAppointments, searchTerm, statusFilter]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleUpdateStatus = async (appointmentId, status, note) => {
    if (!api) return;
    try {
      await updateAppointmentStatus(appointmentId, { status, note });
      toast.success("Cập nhật trạng thái thành công!");
      fetchAllAppointments({ page: currentPage, limit: 10 });
    } catch (err) {
      toast.error("Cập nhật thất bại: " + err.message);
    }
  };

  const handleDelete = async (appointmentId) => {
    if (!api) return;
    if (window.confirm("Bạn có chắc muốn xóa lịch hẹn này?")) {
      try {
        await deleteAppointmentById(appointmentId);
        toast.success("Xóa lịch hẹn thành công!");
        fetchAllAppointments({ page: currentPage, limit: 10 });
      } catch (err) {
        toast.error("Xóa thất bại: " + err.message);
      }
    }
  };

  return {
    allAppointments,
    pagination,
    loading,
    currentPage,
    searchTerm,
    setSearchTerm,
    statusFilter,
    setStatusFilter,
    filteredAppointments,
    handlePageChange,
    handleUpdateStatus,
    handleDelete,
  };
};
