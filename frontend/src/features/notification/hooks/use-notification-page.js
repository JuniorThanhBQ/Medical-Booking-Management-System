import useNotification from "@contexts/notifications/NotificationContext";
import { useEffect, useState } from "react";
import { toast } from "sonner";

import useAuth from "@/contexts/auth/AuthContext";

export const useNotificationPage = () => {
  const {
    notifications,
    loading,
    error,
    pagination,
    fetchNotifications,
    markAllAsRead,
    deleteNotification,
  } = useNotification();

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

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

  return {
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
  };
};
