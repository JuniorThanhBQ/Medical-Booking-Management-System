import { createAppointment } from "@features/booking/services/booking-api-service";
import {
  getDoctorDetail,
  getDoctors,
  getMedicalServices,
  getSpecialtyDetail,
  getTimeSlots,
} from "@features/shared/services/public-api-service";
import { create } from "zustand";

import { apis as api } from "@/configs/apis";
import { STEPS } from "@/utils/booking-utils.js";

const initialState = {
  stepIndex: 0,
  selectedMedicalServiceId: "",
  selectedDate: null,
  selectedTime: "",
  selectedDoctorId: "",
  patientNotes: "",
  firstName: "",
  lastName: "",
  phone: "",
  gender: "MALE",
  birthday: "",
  address: "",
  confirmed: false,
  specialty: null,
  medicalServices: [],
  doctors: [],
  allDoctors: [],
  selectedDoctorSchedule: null,
  timeSlots: [],
  loading: false,
  timeSlotsLoading: false,
  fetchError: null,
  timeSlotsError: null,
  submitting: false,
  submitError: null,
};

export const useBookingStore = create((set, get) => ({
  ...initialState,

  setFirstName: (val) => set({ firstName: val }),
  setLastName: (val) => set({ lastName: val }),
  setPhone: (val) => set({ phone: val }),
  setGender: (val) => set({ gender: val }),
  setBirthday: (val) => set({ birthday: val }),
  setAddress: (val) => set({ address: val }),

  setSelectedMedicalServiceId: (value) => {
    const state = get();
    const selectedService = state.medicalServices.find((s) => s.id === value);
    const filteredDoctors = selectedService
      ? state.allDoctors.filter(
          (d) => d.specialtyId === selectedService.specialtyId,
        )
      : state.allDoctors;

    set({
      selectedMedicalServiceId: value,
      selectedDoctorId: "",
      selectedDate: null,
      selectedTime: "",
      doctors: filteredDoctors,
    });
  },

  setSelectedDate: (value) => set({ selectedDate: value, selectedTime: "" }),

  setSelectedTime: (value) => set({ selectedTime: value }),

  setSelectedDoctorId: (value) =>
    set({
      selectedDoctorId: value,
      selectedDoctorSchedule: null,
      selectedDate: null,
      selectedTime: "",
    }),

  setPatientNotes: (value) => set({ patientNotes: value }),

  setConfirmed: (value) => set({ confirmed: value }),

  increaseStepIndex: () => set((state) => ({ stepIndex: state.stepIndex + 1 })),

  goToStep: (nextIndex) =>
    set((state) => {
      const currentIndex = state.stepIndex;
      const currentStep = STEPS[currentIndex]?.id;

      if (nextIndex < currentIndex) {
        return { stepIndex: Math.max(0, nextIndex) };
      }

      if (nextIndex > currentIndex + 1) {
        return state;
      }

      if (nextIndex === currentIndex + 1) {
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
          return state;
        }

        return { stepIndex: Math.min(currentIndex + 1, STEPS.length - 1) };
      }

      return state;
    }),

  resetBooking: () => set(initialState),

  fetchDoctorDetail: async (doctorId) => {
    if (!doctorId) return;
    try {
      const doctorDetail = await getDoctorDetail(doctorId);
      set({ selectedDoctorSchedule: doctorDetail?.workSchedule ?? null });
    } catch (err) {
      console.error("Failed to load doctor detail:", err);
      set({ selectedDoctorSchedule: null });
    }
  },

  fetchSpecialtyAndDoctors: async (specialtyId) => {
    set({ loading: true, fetchError: null });
    try {
      const [specialtyData, doctorsData, servicesData] = await Promise.all([
        getSpecialtyDetail(specialtyId),
        getDoctors({ specialtyId: specialtyId }),
        getMedicalServices({ specialtyId: specialtyId }),
      ]);
      set({
        specialty: specialtyData,
        doctors: doctorsData.items || [],
        allDoctors: doctorsData.items || [],
        medicalServices: servicesData,
        loading: false,
      });
    } catch (err) {
      console.error("Failed to fetch booking data:", err);
      set({
        loading: false,
        fetchError: "Không thể tải dữ liệu. Vui lòng thử lại.",
      });
    }
  },

  fetchTimeSlots: async (doctorId, dateStr, serviceId) => {
    set({ timeSlotsLoading: true, timeSlotsError: null });
    try {
      const data = await getTimeSlots(doctorId, dateStr, serviceId);
      const slots = data?.[0]?.availableTimeSlots ?? [];

      set({ timeSlots: slots, timeSlotsLoading: false });
    } catch {
      set({
        timeSlots: [],
        timeSlotsLoading: false,
        timeSlotsError: "Không thể tải khung giờ.",
      });
    }
  },

  resetFormOnly: () =>
    set({
      ...initialState,
      specialty: get().specialty,
      medicalServices: get().medicalServices,
      doctors: get().allDoctors,
      allDoctors: get().allDoctors,
    }),

  confirmBooking: async (token, payload, isReceptionist) => {
    set({ submitting: true, submitError: null });
    try {
      if (!token) {
        set({
          submitting: false,
          submitError: "Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.",
        });
        return;
      }
      await createAppointment(api, payload, isReceptionist);
      console.log("Booking confirmed:", payload);
      set({ confirmed: true, submitting: false });
    } catch (err) {
      console.error("Booking failed:", err);
      set({
        submitting: false,
        submitError: "Đặt lịch thất bại. Vui lòng thử lại.",
      });
    }
  },
}));
