import { create } from "zustand";
import { STEPS } from "../utils/booking-utils";

const initialState = {
  stepIndex: 0,
  selectedDate: null,
  selectedTime: "",
  selectedDoctorId: "",
  patientNotes: "",
  confirmed: false,
};

export const useBookingStore = create((set) => ({
  ...initialState,

  setSelectedDate: (value) => set({ selectedDate: value }),

  setSelectedTime: (value) => set({ selectedTime: value }),

  setSelectedDoctorId: (value) => set({ selectedDoctorId: value }),

  setPatientNotes: (value) => set({ patientNotes: value }),

  setConfirmed: (value) => set({ confirmed: value }),

  increaseStepIndex: () => set((state) => ({ stepIndex: state.stepIndex + 1 })),

  goToStep: (nextIndex) =>
    set((/*state ==> Lỗi eslint được đánh dấu ngày 15/03/2026*/) => ({
      stepIndex: Math.max(0, Math.min(nextIndex, STEPS.length - 1)),
    })),

  resetBooking: () => set(initialState),

  confirmBooking: (payload) => {
    const appointment = {
      id: `apt_${Date.now()}`,
      ...payload,
      createdAt: new Date().toISOString(),
    };
    console.log("appointment", appointment);
    // saveAppointment(appointment);
    set({ confirmed: true });
  },
}));
