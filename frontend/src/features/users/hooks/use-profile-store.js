import { create } from "zustand";
import Apis from "@/configs/Apis";
import { getStoredUser } from "@/utils/auth-helpers";
import { setUser as persistUser } from "@/repository/local-storage-repository";

export const useProfileStore = create((set) => ({
  user: getStoredUser(),
  loading: false,

  setUser: (user) => {
    persistUser(user);
    set({ user });
  },

  updateAvatar: (avatarUrl) =>
    set((state) => {
      const updatedUser = { ...state.user, avatar: avatarUrl };
      persistUser(updatedUser);
      return { user: updatedUser };
    }),

  updateProfile: async (data) => {
    set({ loading: true });

    try {
      const res = await Apis.patch("/users/me", data);

      set((state) => {
        const updatedUser = {
          ...state.user,
          ...res.data,
        };

        persistUser(updatedUser);

        return { user: updatedUser };
      });
    } catch (err) {
      console.error("Update failed:", err);
    } finally {
      set({ loading: false });
    }
  },
}));