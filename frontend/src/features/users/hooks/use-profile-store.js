import { create } from "zustand";
import Apis from "@/configs/Apis";

const getInitialUser = () => {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
};

export const useProfileStore = create((set) => ({
  user: getInitialUser(),
  loading: false,

  setUser: (user) => {
    localStorage.setItem("user", JSON.stringify(user));
    set({ user });
  },

  updateProfile: async (data) => {
    set({ loading: true });

    try {
      const res = await Apis.patch("/users/me", data);

      set((state) => {
        const updatedUser = {
          ...state.user,
          ...res.data,
        };

        localStorage.setItem("user", JSON.stringify(updatedUser));

        return { user: updatedUser };
      });
    } catch (err) {
      console.error("Update failed:", err);
    } finally {
      set({ loading: false });
    }
  },
}));