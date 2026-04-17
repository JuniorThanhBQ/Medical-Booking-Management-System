import "./NotificationItem.css";

import { NotificationContext } from "@contexts/notifications/NotificationContext";
import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";

const NotificationItem = ({ notification, onClose }) => {
  const { markAsRead, deleteNotification } = useContext(NotificationContext);
  const navigate = useNavigate();
  const [isDeleting, setIsDeleting] = useState(false);

  const handleClick = async () => {
    try {
      await markAsRead(notification.id);
      navigate(`/notifications/${notification.id}`);
      onClose();
    } catch (error) {
      console.error("Failed to handle notification click:", error);
    }
  };

  const handleDelete = async (e) => {
    e.stopPropagation();
    setIsDeleting(true);
    try {
      await deleteNotification(notification.id);
    } catch (error) {
      console.error("Failed to delete notification:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));

    if (diffInHours < 1) {
      return "Vừa xong";
    } else if (diffInHours < 24) {
      return `${diffInHours} giờ trước`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays} ngày trước`;
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case "APPOINTMENT":
        return "📅";
      case "SYSTEM":
        return "⚙️";
      case "PROMOTION":
        return "🎉";
      default:
        return "🔔";
    }
  };

  return (
    <div
      className={`notification-item ${!notification.is_read ? "unread" : ""}`}
      onClick={handleClick}
    >
      <div className="notification-icon">{getTypeIcon(notification.type)}</div>

      <div className="notification-content">
        <div className="notification-title">{notification.title}</div>
        <div className="notification-message">{notification.message}</div>
        <div className="notification-time">
          {formatDate(notification.created_at)}
        </div>
      </div>

      <div className="notification-actions">
        {notification.is_read && (
          <button
            className="notification-delete-btn"
            onClick={handleDelete}
            disabled={isDeleting}
            title="Xóa thông báo"
            aria-label="Xóa thông báo"
          >
            ✕
          </button>
        )}
      </div>

      {!notification.is_read && <div className="notification-unread-dot"></div>}
    </div>
  );
};

export default NotificationItem;
