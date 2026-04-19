import "@css/receptionist/appointment-page.css";

import AppointmentCard from "@features/receptionist/components/AppointmentCard";
import { useAppointmentsPage } from "@features/receptionist/hooks/use-appointment-page";
import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import Navbar from "@features/users/components/Navbar";
import { useNavigate } from "react-router-dom";

const AppointmentsPage = () => {
  const navigate = useNavigate();
  const {
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
  } = useAppointmentsPage();

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
