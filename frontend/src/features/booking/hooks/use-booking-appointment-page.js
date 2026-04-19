import { useBookingStore } from "@features/booking/hooks/use-booking-store";
import { useEffect, useMemo } from "react";
import { useNavigate, useParams } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";
import { getDoctorAvailableDays, toISODate } from "@/utils/booking-utils.js";

export const useBookAppointmentPage = () => {
  const { specialtyId } = useParams();
  const navigate = useNavigate();
  const { accessToken, user } = useAuth();
  const isReceptionist = user?.role === "RECEPTIONIST";

  const {
    stepIndex,
    selectedMedicalServiceId,
    selectedDate,
    selectedTime,
    selectedDoctorId,
    patientNotes,
    confirmed,
    specialty,
    medicalServices,
    doctors,
    selectedDoctorSchedule,
    timeSlots,
    loading,
    timeSlotsLoading,
    fetchError,
    submitting,
    submitError,
    setSelectedMedicalServiceId,
    setSelectedDate,
    setSelectedTime,
    setSelectedDoctorId,
    setPatientNotes,
    goToStep,
    increaseStepIndex,
    resetBooking,
    confirmBooking,
    fetchSpecialtyAndDoctors,
    fetchDoctorDetail,
    fetchTimeSlots,
    resetFormOnly,
    firstName,
    lastName,
    phone,
    gender,
    birthday,
    address,
    setFirstName,
    setLastName,
    setPhone,
    setGender,
    setBirthday,
    setAddress,
  } = useBookingStore();

  useEffect(() => {
    resetBooking();
    let cancelled = false;
    fetchSpecialtyAndDoctors(specialtyId).then(() => {
      if (cancelled) resetBooking();
    });
    return () => {
      cancelled = true;
    };
  }, [specialtyId, fetchSpecialtyAndDoctors, resetBooking]);

  useEffect(() => {
    if (!selectedDoctorId) return;
    let cancelled = false;
    fetchDoctorDetail(selectedDoctorId).then(() => {
      if (cancelled) return;
    });
    return () => {
      cancelled = true;
    };
  }, [selectedDoctorId, fetchDoctorDetail]);

  useEffect(() => {
    if (!selectedDoctorId || !selectedDate || !selectedMedicalServiceId) return;
    let cancelled = false;
    fetchTimeSlots(
      selectedDoctorId,
      toISODate(selectedDate),
      selectedMedicalServiceId,
    ).then(() => {
      if (cancelled) return;
    });
    return () => {
      cancelled = true;
    };
  }, [
    selectedDoctorId,
    selectedDate,
    selectedMedicalServiceId,
    fetchTimeSlots,
  ]);

  const availableDays = useMemo(() => {
    if (selectedDoctorSchedule?.workDate?.length) {
      return getDoctorAvailableDays(selectedDoctorSchedule.workDate, 30);
    }

    const base = new Date();
    base.setHours(0, 0, 0, 0);
    const days = [];
    for (let i = 1; i <= 30; i += 1) {
      const d = new Date(base);
      d.setDate(base.getDate() + i);
      days.push(d);
    }
    return days;
  }, [selectedDoctorSchedule]);

  const selectedService = useMemo(
    () =>
      medicalServices.find((s) => s.id === selectedMedicalServiceId) ?? null,
    [medicalServices, selectedMedicalServiceId],
  );

  const selectedDoctor = useMemo(
    () => doctors.find((d) => d.id === selectedDoctorId) ?? null,
    [doctors, selectedDoctorId],
  );

  const handleConfirm = () => {
    const basePayload = {
      doctorId: selectedDoctorId,
      medicalServiceId: selectedMedicalServiceId,
      appointmentDate: selectedTime,
      note: patientNotes.trim() || "",
    };

    const finalPayload = isReceptionist
      ? {
          ...basePayload,
          firstName,
          lastName,
          phone,
          gender,
          birthday,
          address,
        }
      : basePayload;

    confirmBooking(accessToken, finalPayload, isReceptionist);
  };

  const handleBrowseSpecialties = () => {
    navigate("/dashboard");
  };

  return {
    specialtyId,
    isReceptionist,
    stepIndex,
    selectedMedicalServiceId,
    selectedDate,
    selectedTime,
    selectedDoctorId,
    patientNotes,
    confirmed,
    specialty,
    medicalServices,
    doctors,
    timeSlots,
    loading,
    timeSlotsLoading,
    fetchError,
    submitting,
    submitError,
    firstName,
    lastName,
    phone,
    gender,
    birthday,
    address,
    availableDays,
    selectedService,
    selectedDoctor,
    setSelectedMedicalServiceId,
    setSelectedDate,
    setSelectedTime,
    setSelectedDoctorId,
    setPatientNotes,
    goToStep,
    increaseStepIndex,
    resetFormOnly,
    setFirstName,
    setLastName,
    setPhone,
    setGender,
    setBirthday,
    setAddress,
    handleConfirm,
    handleBrowseSpecialties,
  };
};
