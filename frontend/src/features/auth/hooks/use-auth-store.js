import { create } from "zustand";

const initialState = {
  loading: false,
  role: null,
  email: "",
  authStep: "email",
  mode: null,
  profile: {
    firstName: "",
    lastName: "",
    phone: "",
    dateOfBirth: "",
    gender: "",
  },
  password: "",
  error: "",
  touchedEmail: false,
};

export const useAuthStore = create((set) => ({
  ...initialState,

  setLoading: (value) => set({ loading: value }),

  setRole: (value) => set({ role: value }),

  setEmail: (value) => set({ email: value }),

  setAuthStep: (value) => set({ authStep: value }),

  setMode: (value) => set({ mode: value }),

  setProfile: (updater) =>
    set((state) => ({
      profile: typeof updater === "function" ? updater(state.profile) : updater,
    })),

  setPassword: (value) => set({ password: value }),

  setError: (value) => set({ error: value }),

  setTouchedEmail: (value) => set({ touchedEmail: value }),

  resetAuthFlow: () =>
    set((state) => ({
      ...state,
      loading: false,
      authStep: initialState.authStep,
      mode: initialState.mode,
      profile: initialState.profile,
      password: initialState.password,
      error: initialState.error,
      touchedEmail: initialState.touchedEmail,
    })),

  reset: () => set(initialState),
}));
