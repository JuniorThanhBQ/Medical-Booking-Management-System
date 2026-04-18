import "./NotificationPage.css";

import { getProfileSidebarItems } from "@configs/const";
import { NotificationContext } from "@contexts/notifications/NotificationContext";
import Navbar from "@features/users/components/Navbar";
import ProfileSidebar from "@features/users/components/ProfileSidebar";
import { useContext, useEffect, useState } from "react";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

import NotificationItem from "../components/NotificationItem";

const NotificationPage = () => {
  const {
    notifications,
    loading,
    error,
    pagination,
    fetchNotifications,
    markAllAsRead,
    deleteNotification,
  } = useContext(NotificationContext);

  const { user: contextUser } = useAuth();
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    fetchNotifications(currentPage);
  }, [currentPage, fetchNotifications]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleMarkAllRead = async () => {
    await markAllAsRead();
  };

  const handleDeleteAll = async () => {
    const readNotifications = notifications.filter((n) => n.is_read);
    if (readNotifications.length === 0) {
      toast.info("Không có thông báo đã đọc nào để xóa.");
      return;
    }

    if (confirm(`Xoá ${readNotifications.length} thông báo đã đọc?`)) {
      for (const notification of readNotifications) {
        await deleteNotification(notification.id);
      }
    }
  };

  const renderPagination = () => {
    const pages = [];
    const totalPages = pagination.total_pages;

    if (totalPages <= 1) return null;

    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <button
          key={i}
          className={`pagination-btn ${i === currentPage ? "active" : ""}`}
          onClick={() => handlePageChange(i)}
        >
          {i}
        </button>,
      );
    }

    return (
      <div className="pagination">
        <button
          className="pagination-btn"
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          ‹ Trước
        </button>
        {pages}
        <button
          className="pagination-btn"
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Sau ›
        </button>
      </div>
    );
  };

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

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
          <div className="notification-page">
            <div className="notification-page-header">
              <h2>Thông báo</h2>
              {notifications.length > 0 && (
                <div className="notification-page-actions">
                  <button
                    className="mark-all-read-btn"
                    onClick={handleMarkAllRead}
                  >
                    ✓ Đánh dấu tất cả đã đọc
                  </button>
                  <button
                    className="delete-all-read-btn"
                    onClick={handleDeleteAll}
                  >
                    🗑 Xoá thông báo đã đọc
                  </button>
                </div>
              )}
            </div>

            <div className="notification-page-content">
              {loading && notifications.length === 0 && (
                <div className="loading-state">Đang tải thông báo...</div>
              )}

              {error && (
                <div className="error-state">
                  <p>{error}</p>
                  <button onClick={() => fetchNotifications(currentPage)}>
                    Thử lại
                  </button>
                </div>
              )}

              {!loading && notifications.length === 0 && !error && (
                <div className="empty-state">
                  <div className="empty-icon">🔔</div>
                  <h3>Không có thông báo nào</h3>
                  <p>Bạn sẽ nhận được thông báo khi có hoạt động mới.</p>
                </div>
              )}

              <div className="notification-list">
                {notifications.map((notification) => (
                  <NotificationItem
                    key={notification.id}
                    notification={notification}
                    onClose={() => {}}
                  />
                ))}
              </div>

              {renderPagination()}
            </div>
          </div>
        </main>
      </div>
    </>
  );
};

export default NotificationPage;
