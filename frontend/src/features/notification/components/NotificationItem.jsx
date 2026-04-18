import "@css/notification/notification-item.css";

import { useNotificationItem } from "@features/notification/hooks/use-notification-item";

const NotificationItem = ({ notification, onClose }) => {
  const { isDeleting, handleClick, handleDelete, formatDate, getTypeIcon } =
    useNotificationItem(notification, onClose);

  return (
    <div
      className={`notification-item ${!notification.is_read ? "unread" : ""}`}
      onClick={handleClick}
    >
      <div
        className="notification-icon"
        dangerouslySetInnerHTML={{ __html: getTypeIcon(notification.type) }}
      />

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
            &#10005;
          </button>
        )}
      </div>

      {!notification.is_read && <div className="notification-unread-dot"></div>}
    </div>
  );
};

export default NotificationItem;
