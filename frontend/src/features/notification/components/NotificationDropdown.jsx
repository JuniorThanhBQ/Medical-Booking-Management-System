import "@css/notification/notification-dropdown.css";

import { useNotificationDropdown } from "@features/notification/hooks/use-notification-dropdown";

import NotificationItem from "./NotificationItem";

const NotificationDropdown = ({ onClose }) => {
  const {
    dropdownRef,
    notifications,
    loading,
    error,
    displayNotifications,
    handleMarkAllRead,
    handleDeleteAll,
    handleViewAll,
  } = useNotificationDropdown(onClose);

  return (
    <div className="notification-dropdown" ref={dropdownRef}>
      <div className="notification-header">
        <h3>Thông báo</h3>
        {notifications.length > 0 && (
          <div className="notification-header-actions">
            <button
              className="mark-all-read-btn"
              onClick={handleMarkAllRead}
              title="Đánh dấu tất cả đã đọc"
            >
              &#10003; Đã đọc
            </button>
            <button
              className="delete-all-read-btn"
              onClick={handleDeleteAll}
              title="Xóa những thông báo đã đọc"
            >
              &#128465; Xoá
            </button>
          </div>
        )}
      </div>

      <div className="notification-list">
        {loading && notifications.length === 0 && (
          <div className="notification-loading">Đang tải...</div>
        )}

        {error && <div className="notification-error">{error}</div>}

        {!loading && notifications.length === 0 && !error && (
          <div className="notification-empty">Không có thông báo nào</div>
        )}

        {displayNotifications.map((notification) => (
          <NotificationItem
            key={notification.id}
            notification={notification}
            onClose={onClose}
          />
        ))}

        {notifications.length > 5 && (
          <button className="view-all-btn" onClick={handleViewAll}>
            Xem tất cả thông báo
          </button>
        )}
      </div>
    </div>
  );
};

export default NotificationDropdown;
