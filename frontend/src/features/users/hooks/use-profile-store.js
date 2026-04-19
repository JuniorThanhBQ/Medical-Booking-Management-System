import { create } from "zustand";

import { endpoints } from "@/configs/apis";

const PROFILE_UPDATE_FIELDS = [
  "email",
  "firstName",
  "lastName",
  "dayOfBirth",
  "gender",
  "phone",
  "address",
  "medicalHistory",
  "avatar",
];

const splitFullName = (name = "") => {
  const parts = String(name).trim().split(/\s+/).filter(Boolean);

  return {
    firstName: parts[0] || "",
    lastName: parts.slice(1).join(" ") || "",
  };
};

const mapApiUserToStoreUser = (apiUser = {}) => {
  const profile = apiUser.profile || {};
  const fullName = [apiUser.firstName, apiUser.lastName]
    .filter(Boolean)
    .join(" ")
    .trim();
  const resolvedName = fullName || apiUser.name || "User";

  return {
    ...apiUser,
    name: resolvedName,
    dateOfBirth: profile.dateOfBirth || apiUser.dateOfBirth || "",
    dayOfBirth: profile.dateOfBirth || apiUser.dayOfBirth || "",
    gender: profile.gender || apiUser.gender || "",
    phone: profile.phone || apiUser.phone || "",
    address: profile.address || apiUser.address || "",
    medicalHistory: profile.medicalHistory || apiUser.medicalHistory || "",
    avatar: profile.avatar || apiUser.avatar || "",
  };
};

const normalizeProfilePayload = (data = {}) => {
  const payload = {
    ...data,
    dayOfBirth: data.dayOfBirth || data.dateOfBirth || "",
    gender: data.gender ? data.gender.toUpperCase() : data.gender,
  };

  if ((!payload.firstName || !payload.lastName) && payload.name) {
    const nameParts = splitFullName(payload.name);
    payload.firstName = payload.firstName || nameParts.firstName;
    payload.lastName = payload.lastName || nameParts.lastName;
  }

  return PROFILE_UPDATE_FIELDS.reduce((acc, key) => {
    if (payload[key] !== undefined && payload[key] !== null) {
      acc[key] = payload[key];
    }
    return acc;
  }, {});
};

export const useProfileStore = create((set) => ({
  user: null,
  loading: false,

  setUser: (user) => {
    set({ user });
  },

  updateAvatar: (avatarUrl) =>
    set((state) => {
      const updatedUser = { ...state.user, avatar: avatarUrl };
      return { user: updatedUser };
    }),

  getProfile: async (api) => {
    set({ loading: true });

    try {
      const res = await api.get(endpoints["auth_current_user"]);
      const mappedUser = mapApiUserToStoreUser(res.data?.user);
      set({ user: mappedUser });
      return mappedUser;
    } catch (err) {
      console.error("Fetch profile failed:", err);
      return null;
    } finally {
      set({ loading: false });
    }
  },

  updateProfile: async (api, data) => {
    set({ loading: true });

    try {
      const payload = normalizeProfilePayload(data);
      const res = await api.patch(endpoints["auth_current_user"], payload);
      const patchedUser = mapApiUserToStoreUser(res.data?.data);

      set((state) => {
        const updatedUser = {
          ...state.user,
          ...patchedUser,
        };

        return { user: updatedUser };
      });
      return res.data?.data || null;
    } catch (err) {
      console.error("Update failed:", err);
      return null;
    } finally {
      set({ loading: false });
    }
  },
}));
