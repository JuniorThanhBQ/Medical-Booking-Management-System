import useNotification from "@contexts/notifications/NotificationContext";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

export const useNotificationItem = (notification, onClose) => {
  const { markAsRead, deleteNotification } = useNotification();
  const navigate = useNavigate();
  const [isDeleting, setIsDeleting] = useState(false);

  const handleClick = async () => {
    try {
      await markAsRead(notification.id);
      navigate(`/notifications/${notification.id}`);
      if (onClose) onClose();
    } catch {
      toast.error("Có lỗi xảy ra khi đánh dấu lịch hẹn.");
    }
  };

  const handleDelete = async (e) => {
    e.stopPropagation();
    setIsDeleting(true);
    try {
      await deleteNotification(notification.id);
    } catch {
      toast.error("Có lỗi xảy ra khi xoá lịch hẹn.");
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
        return "&#128197;";
      case "SYSTEM":
        return "&#9881;";
      case "PROMOTION":
        return "&#127881;";
      default:
        return "&#128276;";
    }
  };

  return {
    isDeleting,
    handleClick,
    handleDelete,
    formatDate,
    getTypeIcon,
  };
};
