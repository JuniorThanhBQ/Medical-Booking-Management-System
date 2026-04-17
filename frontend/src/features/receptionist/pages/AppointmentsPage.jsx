import "@css/receptionist/appointment-page.css";

import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import Navbar from "@features/users/components/Navbar";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

import AppointmentCard from "../components/AppointmentCard";
import { useReceptionistStore } from "../hooks/use-receptionist-store";

const AppointmentsPage = () => {
  const navigate = useNavigate();
  const { api } = useAuth();
  const {
    allAppointments,
    pagination,
    loading,
    error,
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

  if (loading && allAppointments.length === 0) {
    return (
      <>
        <Navbar />
        <main className="dashboard">
          <LoadingSpinner fullPage label="Đang tải..." />
        </main>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="dashboard">
        <section className="dashboard__specialties-section">
          <div className="dashboard__specialties-inner">
            <div className="dashboard__specialties-header">
              <div>
                <h2 className="dashboard__specialties-title">
                  Quản lý lịch hẹn
                </h2>
                <p className="dashboard__specialties-subtitle">
                  Hiển thị {filteredAppointments.length} kết quả phù hợp.
                </p>
              </div>

              <div className="dashboard__filters">
                <div className="filter-group">
                  <input
                    type="text"
                    className="filter-input"
                    placeholder="Tìm tên bệnh nhân, bác sĩ..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
                <div className="filter-group">
                  <select
                    className="filter-select"
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                  >
                    <option value="">Tất cả trạng thái</option>
                    <option value="PENDING">PENDING</option>
                    <option value="APPROVED">APPROVED</option>
                    <option value="COMPLETED">COMPLETED</option>
                    <option value="CANCEL">CANCEL</option>
                  </select>
                </div>
              </div>
            </div>

            {filteredAppointments.length > 0 ? (
              <div className="dashboard__specialties-grid">
                {filteredAppointments.map((appointment) => (
                  <AppointmentCard
                    key={appointment.id}
                    appointment={appointment}
                    onUpdateStatus={handleUpdateStatus}
                    onDelete={handleDelete}
                    onViewDetail={() =>
                      navigate(`/appointments/${appointment.id}`)
                    }
                  />
                ))}
              </div>
            ) : (
              <div className="dashboard__search-empty">
                Không tìm thấy lịch hẹn nào khớp với điều kiện lọc.
              </div>
            )}

            {pagination &&
              pagination.pages > 1 &&
              !searchTerm &&
              !statusFilter && (
                <div className="pagination">
                  <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={!pagination.hasPrev}
                  >
                    Trước
                  </button>
                  <span>
                    Trang {pagination.currentPage} / {pagination.pages}
                  </span>
                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={!pagination.hasNext}
                  >
                    Sau
                  </button>
                </div>
              )}
          </div>
        </section>
      </main>
    </>
  );
};

export default AppointmentsPage;
