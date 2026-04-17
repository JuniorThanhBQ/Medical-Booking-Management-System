import "@css/users/booking.css";

import { useBookingStore } from "@features/booking/hooks/use-booking-store";
import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { useEffect, useMemo } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import useAuth from "@/contexts/auth/AuthContext";
import {
  getDoctorAvailableDays,
  STEPS,
  toISODate,
} from "@/utils/booking-utils.js";

import {
  BookingConfirmStep,
  BookingDayStep,
  BookingDoctorStep,
  BookingNotFoundView,
  BookingServiceStep,
  BookingStepper,
  BookingSuccessView,
  BookingSummary,
  BookingTimeStep,
} from "../components";

export default function BookAppointmentPage() {
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

  if (loading) {
    return (
      <main className="booking">
        <LoadingSpinner fullPage label="Đang tải..." />
      </main>
    );
  }

  if (fetchError) {
    return (
      <main className="booking">
        <p className="booking__error">{fetchError}</p>
      </main>
    );
  }

  if (!specialty) {
    return (
      <BookingNotFoundView onBrowseSpecialties={() => navigate("/dashboard")} />
    );
  }

  if (confirmed) {
    return (
      <BookingSuccessView
        specialtyId={specialtyId}
        specialtyName={specialty.name}
        onBookAnother={() => resetFormOnly()}
      />
    );
  }

  return (
    <main className="booking">
      <section className="booking__shell">
        <div className="booking__container">
          <div className="booking__header">
            <div>
              <Link
                to={`/specialties/${specialtyId}`}
                className="booking__back"
              >
                <span aria-hidden="true">←</span> {specialty.name}
              </Link>
              <h1 className="booking__title">Đặt lịch khám</h1>
              <p className="booking__subtitle">
                Chọn dịch vụ, bác sĩ, ngày, giờ và xác nhận đầy đủ thông tin.
              </p>
            </div>
            <BookingStepper stepIndex={stepIndex} onGoToStep={goToStep} />
          </div>

          <div className="booking__grid">
            <div className="booking__panel">
              {STEPS[stepIndex]?.id === "service" && (
                <BookingServiceStep
                  medicalServices={medicalServices}
                  selectedMedicalServiceId={selectedMedicalServiceId}
                  onSelectService={setSelectedMedicalServiceId}
                  onNext={increaseStepIndex}
                />
              )}
              {STEPS[stepIndex]?.id === "day" && (
                <BookingDayStep
                  availableDays={availableDays}
                  selectedDate={selectedDate}
                  onSelectDate={setSelectedDate}
                  onNext={increaseStepIndex}
                />
              )}
              {STEPS[stepIndex]?.id === "doctor" && (
                <BookingDoctorStep
                  doctorsForSpecialty={doctors}
                  selectedDate={selectedDate}
                  selectedTime={selectedTime}
                  selectedDoctorId={selectedDoctorId}
                  onSelectDoctor={setSelectedDoctorId}
                  onNext={increaseStepIndex}
                />
              )}
              {STEPS[stepIndex]?.id === "time" && (
                <BookingTimeStep
                  timeSlots={timeSlots}
                  selectedDate={selectedDate}
                  selectedTime={selectedTime}
                  onSelectTime={setSelectedTime}
                  onNext={increaseStepIndex}
                  loading={timeSlotsLoading}
                />
              )}
              {STEPS[stepIndex]?.id === "confirm" && (
                <BookingConfirmStep
                  specialtyName={specialty.name}
                  serviceName={selectedService ? selectedService.name : null}
                  selectedDate={selectedDate}
                  selectedTime={selectedTime}
                  selectedDoctorName={
                    selectedDoctor
                      ? `${selectedDoctor.firstName} ${selectedDoctor.lastName}`
                      : null
                  }
                  patientNotes={patientNotes}
                  onPatientNotesChange={setPatientNotes}
                  onConfirm={handleConfirm}
                  onGoToStep={goToStep}
                  submitting={submitting}
                  submitError={submitError}
                  isReceptionist={isReceptionist}
                  patientInfo={{
                    firstName,
                    lastName,
                    phone,
                    gender,
                    birthday,
                    address,
                  }}
                  onInfoChange={{
                    setFirstName,
                    setLastName,
                    setPhone,
                    setGender,
                    setBirthday,
                    setAddress,
                  }}
                  canConfirm={Boolean(
                    selectedMedicalServiceId &&
                    selectedDate &&
                    selectedTime &&
                    selectedDoctorId &&
                    (!isReceptionist || (firstName && lastName && phone)),
                  )}
                />
              )}
            </div>

            <BookingSummary
              serviceName={selectedService ? selectedService.name : null}
              specialtyName={specialty.name}
              selectedDate={selectedDate}
              selectedTime={selectedTime}
              selectedDoctorName={
                selectedDoctor
                  ? `${selectedDoctor.firstName} ${selectedDoctor.lastName}`
                  : null
              }
            />
          </div>
        </div>
      </section>
    </main>
  );
}
