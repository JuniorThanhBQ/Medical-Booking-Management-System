import { create } from "zustand";
import { STEPS } from "@/utils/booking-utils.js";
import { getSpecialtyDetail, getDoctors, getTimeSlots, getMedicalServices } from "@features/shared/services/public-api-service";
import { getUserToken } from "@/utils/auth-helpers";
import { createAppointment } from "../services/appointment-api-service";

const initialState = {
  stepIndex: 0,
  selectedMedicalServiceId: "",
  selectedDate: null,
  selectedTime: "",
  selectedDoctorId: "",
  patientNotes: "",
  confirmed: false,
  specialty: null,
  medicalServices: [],
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

  setSelectedMedicalServiceId: (value) =>
    set({ selectedMedicalServiceId: value, selectedDoctorId: "", selectedDate: null, selectedTime: "" }),

  setSelectedDate: (value) =>
    set({ selectedDate: value, selectedTime: "" }),

  setSelectedTime: (value) => set({ selectedTime: value }),

  setSelectedDoctorId: (value) =>
    set({ selectedDoctorId: value, selectedDate: null, selectedTime: "" }),

  setPatientNotes: (value) => set({ patientNotes: value }),

  setConfirmed: (value) => set({ confirmed: value }),

  increaseStepIndex: () =>
    set((state) => ({ stepIndex: state.stepIndex + 1 })),

  goToStep: (nextIndex) =>
    set((state) => {
      const currentIndex = state.stepIndex;
      const currentStep = STEPS[currentIndex]?.id;
      
      // Allow going backward to any previous step
      if (nextIndex < currentIndex) {
        return { stepIndex: Math.max(0, nextIndex) };
      }
      
      // For forward navigation, only allow moving to next step (no skipping)
      if (nextIndex > currentIndex + 1) {
        return state; // Cannot skip steps
      }
      
      // Check if current step is complete before moving forward
      if (nextIndex === currentIndex + 1) {
        // Verify current step requirements are met
        let isStepComplete = false;
        switch (currentStep) {
          case "service":
            isStepComplete = Boolean(state.selectedMedicalServiceId);
            break;
          case "doctor":
            isStepComplete = Boolean(state.selectedDoctorId);
            break;
          case "day":
            isStepComplete = Boolean(state.selectedDate);
            break;
          case "time":
            isStepComplete = Boolean(state.selectedTime);
            break;
          default:
            isStepComplete = true;
        }
        
        if (!isStepComplete) {
          return state; // Cannot proceed, stay at current step
        }
        
        return { stepIndex: Math.min(currentIndex + 1, STEPS.length - 1) };
      }
      
      // Same step
      return state;
    }),

  resetBooking: () => set(initialState),

  fetchSpecialtyAndDoctors: async (specialtyId) => {
    set({ loading: true, fetchError: null });
    try {
      const [specialtyData, doctorsData, servicesData] = await Promise.all([
        getSpecialtyDetail(specialtyId),
        getDoctors({ specialtyId: specialtyId }),
        getMedicalServices({ specialtyId: specialtyId }),
      ]);
      console.log("specialtyData", specialtyData)
      console.log("doctorsData", doctorsData)
      console.log("servicesData", servicesData)
      set({ specialty: specialtyData, doctors: doctorsData, medicalServices: servicesData, loading: false });
    } catch (err) {
      console.error("Failed to fetch booking data:", err);
      set({ loading: false, fetchError: "Không thể tải dữ liệu. Vui lòng thử lại." });
    }
  },

  fetchTimeSlots: async (doctorId, dateStr, serviceId) => {
    set({ timeSlotsLoading: true, timeSlotsError: null });
    try {
      console.log("fetching time slots for doctor:", doctorId, "on date:", dateStr, "with service:", serviceId)
      const data = await getTimeSlots(doctorId, dateStr, serviceId);
      const slots = data?.[0]?.availableTimeSlots ?? [];
      console.log("fetched time slots:", slots)
      set({ timeSlots: slots, timeSlotsLoading: false });
    } catch (err) {
      console.error("Failed to fetch time slots:", err);
      set({ timeSlots: [], timeSlotsLoading: false, timeSlotsError: "Không thể tải khung giờ." });
    }
  },

  confirmBooking: async ({ doctorId, time, notes, medicalServiceId }) => {
    set({ submitting: true, submitError: null });
    try {
      const token = getUserToken();
      if (!token) {
        set({ submitting: false, submitError: "Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại." });
        return;
      }
      await createAppointment(token, {
        doctorId,
        medicalServiceId,
        appointmentDate: time,
        note: notes || "",
      });
      set({ confirmed: true, submitting: false });
    } catch (err) {
      console.error("Booking failed:", err);
      set({ submitting: false, submitError: "Đặt lịch thất bại. Vui lòng thử lại." });
    }
  },
}));
