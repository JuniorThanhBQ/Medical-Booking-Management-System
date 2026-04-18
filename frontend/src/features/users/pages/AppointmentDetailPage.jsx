import "@css/users/appointment-detail-page.css";

import { getProfileSidebarItems } from "@configs/const";
import Navbar from "@features/users/components/Navbar";
import ProfileSidebar from "@features/users/components/ProfileSidebar";
import { useAppointmentDetail } from "@features/users/hooks/use-appointment-detail";

const AppointmentDetailPage = () => {
  const {
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
  } = useAppointmentDetail();

  return (
    <>
      <Navbar />
      <div className="profile-layout">
        <ProfileSidebar
          userName={displayName}
          activeKey="appointments"
          items={getProfileSidebarItems(contextUser?.role)}
        />
        <main className="profile-main">
          <button type="button" className="ad-btn-back" onClick={handleGoBack}>
            &#8592; Quay lại
          </button>

          <div className="ad-page-header">
            <h1 className="profile-main__title">Chi tiết lịch hẹn</h1>
            {!loading && !error && appointment && (
              <span className={`ad-badge ${statusInfo.className}`}>
                {statusInfo.text}
              </span>
            )}
          </div>

          <div className="ad-container">
            {loading ? (
              <div className="ad-loading">
                <div className="ad-spinner"></div>
                <p>Đang tải dữ liệu...</p>
              </div>
            ) : error ? (
              <div className="ad-error">
                <p>{error}</p>
                <button onClick={handleRetry} className="ad-btn-retry">
                  Thử lại
                </button>
              </div>
            ) : appointment ? (
              <div className="ad-card">
                <div className="ad-section">
                  <h3 className="ad-section-title">&#8505; Thông tin chung</h3>
                  <div className="ad-grid">
                    <div className="ad-info-group">
                      <span className="ad-label">Dịch vụ</span>
                      <span className="ad-value ad-highlight">
                        {appointment.service ||
                          appointment.medicalServiceName ||
                          "—"}
                      </span>
                    </div>
                    <div className="ad-info-group">
                      <span className="ad-label">Tên lịch</span>
                      <span className="ad-value">
                        {appointment.name || "—"}
                      </span>
                    </div>
                    <div className="ad-info-group">
                      <span className="ad-label">Ngày hẹn</span>
                      <span className="ad-value ad-time">
                        &#128197; {formatDate(appointment.appointmentDate)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="ad-section">
                  <h3 className="ad-section-title">
                    &#128101; Thông tin người tham gia
                  </h3>
                  <div className="ad-grid">
                    <div className="ad-info-group">
                      <span className="ad-label">Bệnh nhân</span>
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "10px",
                        }}
                      >
                        <span className="ad-value">
                          {appointment.patientName}
                        </span>
                        <button
                          type="button"
                          className="ad-btn-view-profile"
                          onClick={handleViewPatientProfile}
                        >
                          Xem hồ sơ
                        </button>
                      </div>
                    </div>
                    <div className="ad-info-group">
                      <span className="ad-label">Bác sĩ phụ trách</span>
                      <span className="ad-value">{appointment.doctorName}</span>
                    </div>
                    <div className="ad-info-group">
                      <span className="ad-label">Chuyên khoa</span>
                      <span className="ad-value">
                        {appointment.specialty?.name || appointment.specialty}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="ad-section ad-section--bg">
                  <div className="ad-grid">
                    <div className="ad-info-group ad-full-width">
                      <span className="ad-label">
                        &#128221; Ghi chú bệnh nhân
                      </span>
                      <span className="ad-value ad-note-box">
                        {appointment.note || "Không có ghi chú."}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="ad-footer">
                  <span className="ad-system-time">
                    Mã lịch hẹn: {appointment.id}
                  </span>
                </div>
              </div>
            ) : null}
          </div>
        </main>
      </div>
    </>
  );
};

export default AppointmentDetailPage;
