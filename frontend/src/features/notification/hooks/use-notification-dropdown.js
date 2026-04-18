import useNotification from "@contexts/notifications/NotificationContext";
import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

export const useNotificationDropdown = (onClose) => {
  const navigate = useNavigate();
  const { notifications, loading, error, markAllAsRead, deleteNotification } =
    useNotification();
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
      toast.info("Không có thông báo đã đọc nào để xóa.");
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

  return {
    dropdownRef,
    notifications,
    loading,
    error,
    displayNotifications,
    handleMarkAllRead,
    handleDeleteAll,
    handleViewAll,
  };
};
