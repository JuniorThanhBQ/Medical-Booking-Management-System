import { apis as api, endpoints } from "@configs/apis";
import { AuthContext } from "@contexts/auth/AuthContext";
import { useContext, useEffect, useMemo, useReducer, useRef } from "react";

import { NotificationContext } from "./NotificationContext";
import notificationReducer, { initialState } from "./notificationReducer";
const fetchNotificationsData = async (dispatch, page = 1, perPage = 10) => {
  try {
    dispatch({ type: "SET_LOADING", payload: true });
    const response = await api.get(endpoints["notification"], {
      params: { page, per_page: perPage },
    });
    dispatch({ type: "SET_NOTIFICATIONS", payload: response.data });
  } catch (error) {
    dispatch({
      type: "SET_ERROR",
      payload: error.response?.data?.message || "Failed to fetch notifications",
    });
  }
};
const createNotificationActions = (dispatch) => ({
  fetchNotifications: (page, perPage) =>
    fetchNotificationsData(dispatch, page, perPage),
  markAllAsRead: async () => {
    try {
      await api.patch(endpoints["notification"]);
      dispatch({ type: "MARK_ALL_AS_READ" });
    } catch (error) {
      console.error(error);
    }
  },

  markAsRead: async (notificationId) => {
    try {
      await api.patch(endpoints["notification_detail"](notificationId));
      dispatch({ type: "MARK_AS_READ", payload: notificationId });
    } catch (error) {
      console.error(error);
    }
  },

  getNotificationDetail: async (notificationId) => {
    try {
      const response = await api.get(
        endpoints["notification_detail"](notificationId),
      );
      await api.patch(endpoints["notification_detail"](notificationId));
      dispatch({ type: "MARK_AS_READ", payload: notificationId });
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  },
  deleteNotification: async (notificationId) => {
    try {
      if (endpoints["notification_detail"]) {
        await api.delete(endpoints["notification_detail"](notificationId));
      }
      dispatch({ type: "DELETE_NOTIFICATION", payload: notificationId });
    } catch (error) {
      console.error(error);
    }
  },
});
export const NotificationProvider = ({ children }) => {
  const [state, dispatch] = useReducer(notificationReducer, initialState);
  const { accessToken } = useContext(AuthContext);
  const isInitialized = useRef(false);

  useEffect(() => {
    if (!accessToken) {
      isInitialized.current = false;
      return;
    }

    if (!isInitialized.current) {
      fetchNotificationsData(dispatch);
      isInitialized.current = true;
    }
  }, [accessToken]);

  const notificationActions = useMemo(
    () => createNotificationActions(dispatch),
    [],
  );

  return (
    <NotificationContext.Provider value={{ ...state, ...notificationActions }}>
      {children}
    </NotificationContext.Provider>
  );
};
