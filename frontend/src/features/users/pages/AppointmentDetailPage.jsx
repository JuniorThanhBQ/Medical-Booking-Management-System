import "./AppointmentDetailPage.css";

import { getProfileSidebarItems } from "@configs/const";
import Navbar from "@features/users/components/Navbar";
import ProfileSidebar from "@features/users/components/ProfileSidebar";
import { getAppointmentDetail } from "@features/users/services/appointment-api-service";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

const AppointmentDetailPage = () => {
  const { appointmentId: id } = useParams();
  const navigate = useNavigate();
  const { user: contextUser, api } = useAuth();

  const [appointment, setAppointment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const fetchDetail = async () => {
      if (!api || !id) return;

      setLoading(true);
      try {
        const data = await getAppointmentDetail(api, id);
        if (!mounted) return;
        setAppointment(data);
        setError("");
      } catch (err) {
        if (!mounted) return;
        const errorMessage =
          err.response?.data?.message || "Không thể tải thông vị lịch hẹn.";
        setError(errorMessage);
        toast.error(errorMessage);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchDetail();

    return () => {
      mounted = false;
    };
  }, [id, api]);

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

  const getStatusDisplay = (status) => {
    const statusMap = {
      APPROVED: { text: "Đã xác nhận", className: "ad-badge--green" },
      PENDING: { text: "Chờ xác nhận", className: "ad-badge--yellow" },
      CANCELLED: { text: "Đã hủy", className: "ad-badge--red" },
      COMPLETED: { text: "Đã hoàn thành", className: "ad-badge--blue" },
    };
    return statusMap[status] || { text: status, className: "ad-badge--gray" };
  };

  const formatDate = (dateString) => {
    if (!dateString) return "—";
    try {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      }).format(date);
    } catch {
      return dateString;
    }
  };

  const statusInfo = getStatusDisplay(appointment?.status);

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
            className="ad-btn-back"
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
                <button
                  onClick={() => window.location.reload()}
                  className="ad-btn-retry"
                >
                  Thử lại
                </button>
              </div>
            ) : appointment ? (
              <div className="ad-card">
                <div className="ad-section">
                  <h3 className="ad-section-title">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="16" x2="12" y2="12"></line>
                      <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                    Thông tin chung
                  </h3>
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
                        <svg
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <rect
                            x="3"
                            y="4"
                            width="18"
                            height="18"
                            rx="2"
                            ry="2"
                          ></rect>
                          <line x1="16" y1="2" x2="16" y2="6"></line>
                          <line x1="8" y1="2" x2="8" y2="6"></line>
                          <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        {formatDate(appointment.appointmentDate)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="ad-section">
                  <h3 className="ad-section-title">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                    Thông tin người tham gia
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
                          onClick={() =>
                            navigate(`/appointments/${id}/patient-profile`)
                          }
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
                        <svg
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                          <polyline points="14 2 14 8 20 8"></polyline>
                          <line x1="16" y1="13" x2="8" y2="13"></line>
                          <line x1="16" y1="17" x2="8" y2="17"></line>
                          <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                        Ghi chú bệnh nhân
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
