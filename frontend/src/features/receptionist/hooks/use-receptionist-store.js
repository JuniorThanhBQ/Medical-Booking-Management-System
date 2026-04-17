import { create } from "zustand";

import {
  createReceptionistAppointment,
  deleteAppointment,
  getAllAppointments,
  getAppointmentDetail,
  getReceptionistAppointments,
  updateAppointment,
} from "../services/appointment-api-service";

const initialState = {
  receptionistAppointments: [],
  allAppointments: [],
  appointmentDetail: null,
  loading: false,
  error: null,
  updating: false,
  updateError: null,
  deleting: false,
  deleteError: null,
  creating: false,
  createError: null,
  pagination: {
    total: 0,
    pages: 0,
    currentPage: 1,
    perPage: 10,
    hasNext: false,
    hasPrev: false,
  },
  api: null,
};

export const useReceptionistStore = create((set, get) => ({
  ...initialState,

  setApi: (api) => set({ api }),

  fetchReceptionistAppointments: async () => {
    const { api } = get();
    if (!api) return;

    set({ loading: true, error: null });
    try {
      const data = await getReceptionistAppointments(api);
      set({ receptionistAppointments: data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchAllAppointments: async (params = {}) => {
    const { api } = get();
    if (!api) return;

    set({ loading: true, error: null });
    try {
      const data = await getAllAppointments(api, params);
      set({
        allAppointments: data.items,
        pagination: data.meta,
        loading: false,
      });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchAppointmentDetail: async (appointmentId) => {
    const { api } = get();
    if (!api) return;

    set({ loading: true, error: null });
    try {
      const data = await getAppointmentDetail(api, appointmentId);
      set({ appointmentDetail: data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  updateAppointmentStatus: async (appointmentId, payload) => {
    const { api } = get();
    if (!api) throw new Error("API not initialized");

    set({ updating: true, updateError: null });
    try {
      const data = await updateAppointment(api, appointmentId, payload);
      const state = get();
      const updatedAppointments = state.allAppointments.map((appt) =>
        appt.id === appointmentId ? { ...appt, ...payload } : appt,
      );
      set({
        allAppointments: updatedAppointments,
        updating: false,
      });
      return data;
    } catch (error) {
      set({ updateError: error.message, updating: false });
      throw error;
    }
  },

  deleteAppointmentById: async (appointmentId) => {
    const { api } = get();
    if (!api) throw new Error("API not initialized");

    set({ deleting: true, deleteError: null });
    try {
      await deleteAppointment(api, appointmentId);
      const state = get();
      const filteredAppointments = state.allAppointments.filter(
        (appt) => appt.id !== appointmentId,
      );
      set({
        allAppointments: filteredAppointments,
        deleting: false,
      });
    } catch (error) {
      set({ deleteError: error.message, deleting: false });
      throw error;
    }
  },

  clearAppointmentDetail: () => {
    set({ appointmentDetail: null });
  },

  createAppointment: async (payload) => {
    const { api } = get();
    if (!api) throw new Error("API not initialized");

    set({ creating: true, createError: null });
    try {
      const data = await createReceptionistAppointment(api, payload);
      set({ creating: false });
      return data;
    } catch (error) {
      set({ createError: error.message, creating: false });
      throw error;
    }
  },
}));
