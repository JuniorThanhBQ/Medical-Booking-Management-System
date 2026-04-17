import "./NotificationBell.css";

import useAuth from "@contexts/auth/AuthContext";
import { NotificationContext } from "@contexts/notifications/NotificationContext";
import { useContext, useState } from "react";

import NotificationDropdown from "./NotificationDropdown";

const NotificationBell = () => {
  const { unreadCount } = useContext(NotificationContext);
  const { accessToken } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    if (accessToken) {
      setIsOpen(!isOpen);
    }
  };

  return (
    <div className="notification-bell-container">
      <button
        className="notification-bell"
        onClick={toggleDropdown}
        aria-label="Notifications"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        {unreadCount > 0 && (
          <span className="notification-badge">{unreadCount}</span>
        )}
      </button>

      {isOpen && <NotificationDropdown onClose={() => setIsOpen(false)} />}
    </div>
  );
};

export default NotificationBell;
