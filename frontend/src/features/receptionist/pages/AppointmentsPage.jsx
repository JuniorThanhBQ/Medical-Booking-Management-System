import "@css/receptionist/appointment-page.css";

import { BookingDayStep } from "@features/booking/components/BookingDayStep"; 
import { BookingTimeStep } from "@features/booking/components/BookingTimeStep";
import AppointmentCard from "@features/receptionist/components/AppointmentCard";
import { useAppointmentsPage } from "@features/receptionist/hooks/use-appointment-page";
import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import Navbar from "@features/users/components/Navbar";
import { useNavigate } from "react-router-dom";

import { APPOINTMENT_STATUS_LABELS } from "@/configs/const";

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
                    {Object.entries(APPOINTMENT_STATUS_LABELS).map(([value, label]) => (
                      <option key={value} value={value}>
                        {label}
                      </option>
                    ))}
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
                    onOpenTimeModal={() => handleOpenTimeModal(appointment)}
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
      {isTimeModalOpen && (
        <div className="modal-overlay" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div className="modal-content" style={{ backgroundColor: 'white', padding: '24px', borderRadius: '8px', maxWidth: '600px', width: '100%', maxHeight: '90vh', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3 style={{ margin: 0 }}>Cập nhật thời gian hẹn</h3>
              <button onClick={handleCloseTimeModal} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>×</button>
            </div>

            {timeStepIndex === 0 && (
              <BookingDayStep
                availableDays={availableDays}
                selectedDate={selectedDate}
                onSelectDate={handleSelectDate}
                onNext={() => setTimeStepIndex(1)}
              />
            )}

            {timeStepIndex === 1 && (
              <BookingTimeStep
                timeSlots={timeSlots}
                selectedDate={selectedDate}
                selectedTime={selectedTime}
                onSelectTime={setSelectedTime}
                onNext={handleSaveTimeChange} 
                loading={loadingSlots}
              />
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
              {timeStepIndex === 1 && (
                 <button className="booking__secondary" onClick={() => setTimeStepIndex(0)}>Quay lại chọn ngày</button>
              )}
              {timeStepIndex === 1 && (
                 <button 
                   className="booking__primary" 
                   onClick={handleSaveTimeChange} 
                   disabled={!selectedTime}
                 >
                   Xác nhận lưu
                 </button>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default AppointmentsPage;
