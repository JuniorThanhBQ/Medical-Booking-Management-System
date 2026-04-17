import "./PatientProfilePage.css";

import { getProfileSidebarItems } from "@configs/const";
import Navbar from "@features/users/components/Navbar";
import ProfileSidebar from "@features/users/components/ProfileSidebar";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "sonner";

import { endpoints } from "@/configs/apis";
import useAuth from "@/contexts/auth/AuthContext";

const PatientProfilePage = () => {
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
          <button
            type="button"
            className="pp-btn-back"
            onClick={() => navigate(-1)}
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
            Quay lại
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
                <button
                  onClick={() => window.location.reload()}
                  className="pp-btn-retry"
                >
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
