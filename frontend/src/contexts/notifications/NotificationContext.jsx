import { createContext, useContext } from "react";

export const NotificationContext = createContext();

export default function useNotification() {
  return useContext(NotificationContext);
}
