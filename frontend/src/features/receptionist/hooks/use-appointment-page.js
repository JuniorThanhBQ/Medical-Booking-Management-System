import { useReceptionistStore } from "@features/receptionist/hooks/use-receptionist-store";
import { useEffect, useMemo, useState } from "react";
import { toast } from "sonner";

import { endpoints } from "@/configs/apis";
import useAuth from "@/contexts/auth/AuthContext";
import { getDoctorAvailableDays, toISODate } from "@/utils/booking-utils";

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
  const [isTimeModalOpen, setIsTimeModalOpen] = useState(false);
  const [editingAppointment, setEditingAppointment] = useState(null);
  const [timeStepIndex, setTimeStepIndex] = useState(0);
  const [availableDays, setAvailableDays] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [timeSlots, setTimeSlots] = useState([]);
  const [selectedTime, setSelectedTime] = useState(null);
  const [loadingSlots, setLoadingSlots] = useState(false);

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

  const handleOpenTimeModal = async (appointment) => {
    setEditingAppointment(appointment);
    setIsTimeModalOpen(true);
    setTimeStepIndex(0);
    setSelectedDate(null);
    setSelectedTime(null);
    setTimeSlots([]);

    const base = new Date();
    base.setHours(0, 0, 0, 0);
    const fallbackDays = [];
    for (let i = 1; i <= 30; i++) {
      const d = new Date(base);
      d.setDate(base.getDate() + i);
      fallbackDays.push(d);
    }
    setAvailableDays(fallbackDays);

    const doctorId = appointment?.doctorId || appointment?.doctor?.id;
    const medicalServiceId = appointment?.medicalServiceId || appointment?.medicalService?.id;
    if (doctorId && api) {
      try {
        const res = await api.get(endpoints.public_doctor_detail(doctorId, medicalServiceId));
        const workDate = res.data?.data?.workSchedule?.workDate || res.data?.workSchedule?.workDate;
        
        if (workDate?.length) {
          setAvailableDays(getDoctorAvailableDays(workDate, 30));
        }
      } catch (err) {
        console.error("Không tải được lịch làm việc chi tiết của bác sĩ:", err);
      }
    }
  };

  const handleCloseTimeModal = () => {
    setIsTimeModalOpen(false);
    setEditingAppointment(null);
  };

  const handleSelectDate = async (date) => {
    setSelectedDate(date);
    setSelectedTime(null);

    const doctorId = editingAppointment?.doctorId || editingAppointment?.doctor?.id;
    const serviceId = editingAppointment?.medicalServiceId || editingAppointment?.medicalService?.id;

    if (!doctorId || !api) return;

    setLoadingSlots(true);
    try {
      const dateStr = toISODate(date); 
      
      const res = await api.get(endpoints.public_doctor_time_slots(doctorId), {
        params: { 
          date: dateStr,
          serviceId: serviceId
        },
      });

      const data = res.data?.data || res.data;
      const slots = Array.isArray(data) 
        ? data[0]?.availableTimeSlots 
        : data?.availableTimeSlots;
        
      setTimeSlots(slots || []);
    } catch {
      toast.error("Không tải được khung giờ làm việc của bác sĩ!");
      setTimeSlots([]);
    } finally {
      setLoadingSlots(false);
    }
  };

  const handleSaveTimeChange = async () => {
    if (!selectedTime || !editingAppointment || !api) return;
    try {
      await updateAppointmentStatus(editingAppointment.id, {
        status: editingAppointment.status,
        note: editingAppointment.note || "",
        appointmentDate: selectedTime,
      });
      toast.success("Cập nhật thời gian hẹn thành công!");
      handleCloseTimeModal();
      fetchAllAppointments({ page: currentPage, limit: 10 });
    } catch (err) {
      toast.error("Cập nhật thời gian thất bại: " + err.message);
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
    isTimeModalOpen,
    timeStepIndex,
    setTimeStepIndex,
    availableDays,
    selectedDate,
    selectedTime,
    setSelectedTime,
    timeSlots,
    loadingSlots,
    handleOpenTimeModal,
    handleCloseTimeModal,
    handleSelectDate,
    handleSaveTimeChange,
  };
};
