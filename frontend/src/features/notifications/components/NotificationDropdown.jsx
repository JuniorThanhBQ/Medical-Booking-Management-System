import "./NotificationDropdown.css";

import { NotificationContext } from "@contexts/notifications/NotificationContext";
import { useContext, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

import NotificationItem from "./NotificationItem";

const NotificationDropdown = ({ onClose }) => {
  const navigate = useNavigate();
  const { notifications, loading, error, markAllAsRead, deleteNotification } =
    useContext(NotificationContext);

  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        onClose();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [onClose]);

  const handleMarkAllRead = async () => {
    await markAllAsRead();
  };

  const handleDeleteAll = async () => {
    const readNotifications = notifications.filter((n) => n.is_read);
    if (readNotifications.length === 0) {
      alert("Không có thông báo đã đọc để xoá");
      return;
    }

    if (confirm(`Xoá ${readNotifications.length} thông báo đã đọc?`)) {
      for (const notification of readNotifications) {
        await deleteNotification(notification.id);
      }
    }
  };

  const handleViewAll = () => {
    navigate("/notifications");
    onClose();
  };

  const displayNotifications = notifications.slice(0, 5);

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
              ✓ Đã đọc
            </button>
            <button
              className="delete-all-read-btn"
              onClick={handleDeleteAll}
              title="Xóa những thông báo đã đọc"
            >
              🗑 Xoá
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
