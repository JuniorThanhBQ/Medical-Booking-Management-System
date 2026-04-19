import { apis as api, endpoints } from "@configs/apis";
import { AuthContext } from "@contexts/auth/AuthContext";
import { useContext, useEffect, useMemo, useReducer, useRef } from "react";
import { toast } from "sonner";

import { NotificationContext } from "./NotificationContext";
import notificationReducer, { initialState } from "./notificationReducer";
const fetchNotificationsData = async (dispatch, page = 1, perPage = 6) => {
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
    toast.error("Có lỗi trong lấy thông báo.");
  } finally {
    dispatch({ type: "SET_LOADING", payload: false });
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
      const [response] = await Promise.all([
        api.get(endpoints["notification_detail"](notificationId)),
        api
          .patch(endpoints["notification_detail"](notificationId))
          .catch(() => {}),
      ]);
      dispatch({ type: "MARK_AS_READ", payload: notificationId });

      return response.data;
    } catch (error) {
      toast.error("Lỗi khi tải chi tiết thông báo.");
      throw error;
    }
  },
  deleteNotification: async (notificationId) => {
    try {
      await api.delete(endpoints["notification_detail"](notificationId));
      dispatch({ type: "DELETE_NOTIFICATION", payload: notificationId });
    } catch (error) {
      console.error(error);
      toast.error("Xóa thông báo thất bại.");
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
      dispatch({ type: "CLEAR_NOTIFICATIONS" });
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
