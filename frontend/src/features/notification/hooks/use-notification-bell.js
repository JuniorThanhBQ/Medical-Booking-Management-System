import useAuth from "@contexts/auth/AuthContext";
import useNotification from "@contexts/notifications/NotificationContext";
import { useState } from "react";

export const useNotificationBell = () => {
  const { unreadCount } = useNotification();
  const { accessToken } = useAuth();
  const [isOpen, setIsOpen] = useState(false);


  const toggleDropdown = () => {
    if (accessToken) {
      setIsOpen(!isOpen);
    }
  };


  const handleClose = () => {
    setIsOpen(false);
  };


  return {
    unreadCount,
    isOpen,
    toggleDropdown,
    handleClose,
  };


};
