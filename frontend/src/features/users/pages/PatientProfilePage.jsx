import "@css/users/patient-profile-page.css";

import { getProfileSidebarItems } from "@configs/const";
import Navbar from "@features/users/components/Navbar";
import ProfileSidebar from "@features/users/components/ProfileSidebar";
import { usePatientProfile } from "@features/users/hooks/use-patient-profile";

const PatientProfilePage = () => {
  const {
    patientProfile,
    loading,
    error,
    contextUser,
    displayName,
    formatDate,
    getGenderText,
    handleGoBack,
    handleRetry,
  } = usePatientProfile();

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
          <button type="button" className="pp-btn-back" onClick={handleGoBack}>
            &#8592; Quay lại
          </button>

          <div className="pp-page-header">
            <h1 className="profile-main__title">Hồ sơ bệnh nhân</h1>
          </div>

          <div className="pp-container">
            {loading ? (
              <div className="pp-loading">
                <div className="pp-spinner"></div>
                <p>Đang tải hồ sơ...</p>
              </div>
            ) : error ? (
              <div className="pp-error">
                <p>{error}</p>
                <button onClick={handleRetry} className="pp-btn-retry">
                  Thử lại
                </button>
              </div>
            ) : patientProfile ? (
              <div className="pp-card">
                <div className="pp-header-section">
                  <div className="pp-avatar-wrapper">
                    {patientProfile.avatar ? (
                      <img
                        src={patientProfile.avatar}
                        alt="Avatar"
                        className="pp-avatar"
                      />
                    ) : (
                      <div className="pp-avatar-placeholder">
                        {patientProfile.lastName?.[0] || "U"}
                      </div>
                    )}
                  </div>
                  <div className="pp-title-info">
                    <h2>
                      {patientProfile.lastName} {patientProfile.firstName}
                    </h2>
                    <span className="pp-badge">Thông tin cá nhân</span>
                  </div>
                </div>

                <div className="pp-content-section">
                  <div className="pp-grid">
                    <div className="pp-item">
                      <span className="pp-label">Ngày sinh</span>
                      <span className="pp-value">
                        {formatDate(patientProfile.dateOfBirth)}
                      </span>
                    </div>
                    <div className="pp-item">
                      <span className="pp-label">Giới tính</span>
                      <span className="pp-value">
                        {getGenderText(patientProfile.gender)}
                      </span>
                    </div>
                    <div className="pp-item">
                      <span className="pp-label">Số điện thoại</span>
                      <span className="pp-value">
                        {patientProfile.phone || "Chưa cập nhật"}
                      </span>
                    </div>
                    <div className="pp-item pp-item--full">
                      <span className="pp-label">Địa chỉ</span>
                      <span className="pp-value">
                        {patientProfile.address || "Chưa cập nhật"}
                      </span>
                    </div>
                  </div>

                  <div className="pp-history-section">
                    <h3 className="pp-history-title">Tiền sử bệnh lý</h3>
                    <div className="pp-history-box">
                      {patientProfile.medicalHistory ||
                        "Chưa ghi nhận tiền sử bệnh lý nào."}
                    </div>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        </main>
      </div>
    </>
  );
};

export default PatientProfilePage;
