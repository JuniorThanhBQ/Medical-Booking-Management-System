import "./NotificationDetailPage.css";

import { getProfileSidebarItems, ROLE } from "@configs/const";
import { NotificationContext } from "@contexts/notifications/NotificationContext";
import Navbar from "@features/users/components/Navbar";
import ProfileSidebar from "@features/users/components/ProfileSidebar";
import { useContext, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";

const NotificationDetailPage = () => {
  const { notificationId } = useParams();
  const { getNotificationDetail } = useContext(NotificationContext);
  const { user: contextUser } = useAuth();
  const navigate = useNavigate();

  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const loadDetail = async () => {
      if (!notificationId) return;
      setLoading(true);
      try {
        const result = await getNotificationDetail(notificationId);
        if (!mounted) return;
        setNotification(result);
        setError("");
      } catch {
        if (!mounted) return;
        setError("Không thể tải chi tiết thông báo.");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadDetail();

    return () => {
      mounted = false;
    };
  }, [notificationId, getNotificationDetail]);

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

  const appointmentId = notification?.appointment_id;

  const handleViewAppointment = () => {
    if (!appointmentId) return;
    if (contextUser?.role === ROLE.Doctor) {
      navigate(`/doctor/exam/${appointmentId}`);
    } else {
      navigate(`/appointments/${appointmentId}`);
    }
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

  return (
    <>
      <Navbar />
      <div className="profile-layout">
        <ProfileSidebar
          userName={displayName}
          activeKey="notifications"
          items={getProfileSidebarItems(contextUser?.role)}
        />
        <main className="profile-main">
          <button
            type="button"
            className="nd-btn-back"
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
            Quay lại danh sách
          </button>

          <h1 className="profile-main__title">Chi tiết thông báo</h1>

          <div className="nd-container">
            {loading ? (
              <div className="nd-loading">
                <div className="nd-spinner"></div>
                <p>Đang tải chi tiết thông báo...</p>
              </div>
            ) : error ? (
              <div className="nd-error">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <p>{error}</p>
              </div>
            ) : (
              <div className="nd-card">
                <div className="nd-card-header">
                  <div className="nd-icon">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                      <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                    </svg>
                  </div>
                  <div className="nd-header-content">
                    <h2 className="nd-title">{notification?.title}</h2>
                    <span className="nd-time">
                      {formatDate(notification?.created_at)}
                    </span>
                  </div>
                </div>

                <div className="nd-card-body">
                  <p className="nd-message">{notification?.message}</p>
                </div>

                <div className="nd-card-meta">
                  <div className="nd-meta-group">
                    <span className="nd-meta-label">Mã thông báo</span>
                    <span className="nd-meta-value">#{notification?.id}</span>
                  </div>
                  <div className="nd-meta-group">
                    <span className="nd-meta-label">Loại</span>
                    <span className="nd-meta-value nd-badge nd-badge--gray">
                      {notification?.type || "Hệ thống"}
                    </span>
                  </div>
                  <div className="nd-meta-group">
                    <span className="nd-meta-label">Trạng thái đọc</span>
                    <span
                      className={`nd-meta-value nd-badge ${notification?.is_read ? "nd-badge--green" : "nd-badge--blue"}`}
                    >
                      {notification?.is_read ? "Đã đọc" : "Chưa đọc"}
                    </span>
                  </div>
                  <div className="nd-meta-group">
                    <span className="nd-meta-label">Email thông báo</span>
                    <span
                      className={`nd-meta-value nd-badge ${notification?.send_email ? "nd-badge--green" : "nd-badge--gray"}`}
                    >
                      {notification?.send_email ? "Đã gửi" : "Không gửi"}
                    </span>
                  </div>
                </div>

                {appointmentId && (
                  <div className="nd-card-actions">
                    <div className="nd-action-info">
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
                      <span>
                        Mã lịch hẹn liên kết: <strong>#{appointmentId}</strong>
                      </span>
                    </div>
                    <button
                      className="nd-btn-primary"
                      onClick={handleViewAppointment}
                    >
                      Xem chi tiết lịch hẹn
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </main>
      </div>
    </>
  );
};

export default NotificationDetailPage;
