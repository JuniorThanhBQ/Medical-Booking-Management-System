import "@css/notification/notification-page.css";

import { getProfileSidebarItems } from "@configs/const";
import { useNotificationPage } from "@features/notification/hooks/use-notification-page";
import Navbar from "@features/users/components/Navbar";
import ProfileSidebar from "@features/users/components/ProfileSidebar";

import NotificationItem from "../components/NotificationItem";

const NotificationPage = () => {
  const {
    notifications,
    loading,
    error,
    pagination,
    currentPage,
    contextUser,
    displayName,
    handlePageChange,
    handleMarkAllRead,
    handleDeleteAll,
    fetchNotifications,
  } = useNotificationPage();

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
          &#8249; Trước
        </button>
        {pages}
        <button
          className="pagination-btn"
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Sau &#8250;
        </button>
      </div>
    );
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
          <div className="notification-page">
            <div className="notification-page-header">
              <h2>Thông báo</h2>
              {notifications.length > 0 && (
                <div className="notification-page-actions">
                  <button
                    className="mark-all-read-btn"
                    onClick={handleMarkAllRead}
                  >
                    &#10003; Đánh dấu tất cả đã đọc
                  </button>
                  <button
                    className="delete-all-read-btn"
                    onClick={handleDeleteAll}
                  >
                    &#128465; Xoá thông báo đã đọc
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
                  <div className="empty-icon">&#128276;</div>
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
