import { create } from "zustand";
import { STEPS } from "../utils/booking-utils";
import { getSpecialtyDetail, getDoctors, getTimeSlots } from "@/services/public-api-service";
import { getUserToken } from "@/utils/auth-helpers";
import { createAppointment } from "../services/appointment-api-service";

const initialState = {
  stepIndex: 0,
  selectedDate: null,
  selectedTime: "",
  selectedDoctorId: "",
  patientNotes: "",
  confirmed: false,
  specialty: null,
  doctors: [],
  timeSlots: [],
  loading: false,
  timeSlotsLoading: false,
  fetchError: null,
  timeSlotsError: null,
  submitting: false,
  submitError: null,
};

export const useBookingStore = create((set) => ({
  ...initialState,

  setSelectedDate: (value) =>
    set({ selectedDate: value, selectedDoctorId: "", selectedTime: "" }),

  setSelectedTime: (value) => set({ selectedTime: value }),

  setSelectedDoctorId: (value) =>
    set({ selectedDoctorId: value, selectedTime: "" }),

  setPatientNotes: (value) => set({ patientNotes: value }),

  setConfirmed: (value) => set({ confirmed: value }),

  increaseStepIndex: () =>
    set((state) => ({ stepIndex: state.stepIndex + 1 })),

  goToStep: (nextIndex) =>
    set(() => ({
      stepIndex: Math.max(0, Math.min(nextIndex, STEPS.length - 1)),
    })),

  resetBooking: () => set(initialState),

  fetchSpecialtyAndDoctors: async (specialtyId) => {
    set({ loading: true, fetchError: null });
    try {
      const [specialtyData, doctorsData] = await Promise.all([
        getSpecialtyDetail(specialtyId),
        getDoctors({ specialty_id: specialtyId }),
      ]);
      set({ specialty: specialtyData, doctors: doctorsData, loading: false });
    } catch (err) {
      console.error("Failed to fetch booking data:", err);
      set({ loading: false, fetchError: "Không thể tải dữ liệu. Vui lòng thử lại." });
    }
  },

  fetchTimeSlots: async (doctorId, dateStr) => {
    set({ timeSlotsLoading: true, timeSlotsError: null });
    try {
      console.log("fetching time slots for doctor:", doctorId, "on date:", dateStr)
      const data = await getTimeSlots(doctorId, dateStr);
      const slots = data?.[0]?.availableTimeSlots ?? [];
      console.log("fetched time slots:", slots)
      set({ timeSlots: slots, timeSlotsLoading: false });
    } catch (err) {
      console.error("Failed to fetch time slots:", err);
      set({ timeSlots: [], timeSlotsLoading: false, timeSlotsError: "Không thể tải khung giờ." });
    }
  },

  confirmBooking: async ({ doctorId, date, time, notes }) => {
    set({ submitting: true, submitError: null });
    try {
      const token = getUserToken();
      if (!token) {
        set({ submitting: false, submitError: "Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại." });
        return;
      }
      await createAppointment(token, {
        doctorId,
        appointmentDate: date,
        startTime: time,
        note: notes || "",
      });
      set({ confirmed: true, submitting: false });
    } catch (err) {
      console.error("Booking failed:", err);
      set({ submitting: false, submitError: "Đặt lịch thất bại. Vui lòng thử lại." });
    }
  },
}));
