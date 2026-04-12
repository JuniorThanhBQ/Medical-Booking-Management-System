import "@/assets/css/users/booking.css";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useEffect, useMemo } from "react";
import { useBookingStore } from "../hooks/use-booking-store";
import { STEPS, toISODate } from "@/utils/booking-utils.js";
import { AVAILABLE_BOOKING_DAYS } from "@/configs/const";
import LoadingSpinner from "@/components/LoadingSpinner";
import {
  BookingNotFoundView,
  BookingSuccessView,
  BookingStepper,
  BookingDayStep,
  BookingTimeStep,
  BookingDoctorStep,
  BookingConfirmStep,
  BookingSummary,
} from "../components/booking";

export default function BookAppointmentPage() {
  const { specialtyId } = useParams();
  const navigate = useNavigate();

  const {
    stepIndex, selectedDate, selectedTime, selectedDoctorId, patientNotes, confirmed,
    specialty, doctors, timeSlots, loading, timeSlotsLoading, fetchError, submitting, submitError,
    setSelectedDate, setSelectedTime, setSelectedDoctorId, setPatientNotes,
    goToStep, increaseStepIndex, resetBooking, confirmBooking,
    fetchSpecialtyAndDoctors, fetchTimeSlots,
  } = useBookingStore();

  useEffect(() => {
    resetBooking();
    let cancelled = false;
    fetchSpecialtyAndDoctors(specialtyId).then(() => {
      if (cancelled) resetBooking();
    });
    return () => { cancelled = true; };
  }, [specialtyId]);

  useEffect(() => {
    if (!selectedDoctorId || !selectedDate) return;
    let cancelled = false;
    fetchTimeSlots(selectedDoctorId, toISODate(selectedDate)).then(() => {
      if (cancelled) return;
    });
    return () => { cancelled = true; };
  }, [selectedDoctorId, selectedDate]);

  const availableDays = useMemo(() => {
    const base = new Date();
    base.setHours(0, 0, 0, 0);
    const days = [];
    for (let i = 1; i <= AVAILABLE_BOOKING_DAYS; i += 1) {
      const d = new Date(base);
      d.setDate(base.getDate() + i);
      days.push(d);
    }
    return days;
  }, []);

  const selectedDoctor = useMemo(
    () => doctors.find((d) => d.id === selectedDoctorId) ?? null,
    [doctors, selectedDoctorId],
  );

  const handleConfirm = () => {
    confirmBooking({
      doctorId: selectedDoctorId,
      date: selectedDate ? toISODate(selectedDate) : null,
      time: selectedTime,
      notes: patientNotes.trim() || "",
    });
  };

  if (loading) {
    return <main className="booking"><LoadingSpinner fullPage label="Đang tải..." /></main>;
  }

  if (fetchError) {
    return <main className="booking"><p className="booking__error">{fetchError}</p></main>;
  }

  if (!specialty) {
    return <BookingNotFoundView onBrowseSpecialties={() => navigate("/dashboard")} />;
  }

  if (confirmed) {
    return (
      <BookingSuccessView
        specialtyId={specialtyId}
        specialtyName={specialty.name}
        onBookAnother={() => resetBooking()}
      />
    );
  }

  return (
    <main className="booking">
      <section className="booking__shell">
        <div className="booking__container">
          <div className="booking__header">
            <div>
              <Link to={`/specialties/${specialtyId}`} className="booking__back">
                <span aria-hidden="true">←</span> {specialty.name}
              </Link>
              <h1 className="booking__title">Đặt lịch khám</h1>
              <p className="booking__subtitle">
                Chọn ngày, bác sĩ, giờ và xác nhận đầy đủ thông tin.
              </p>
            </div>
            <BookingStepper stepIndex={stepIndex} onGoToStep={goToStep} />
          </div>

          <div className="booking__grid">
            <div className="booking__panel">
              {/* eslint-disable-next-line security/detect-object-injection */}
              {STEPS[stepIndex]?.id === "day" && (
                <BookingDayStep
                  availableDays={availableDays}
                  selectedDate={selectedDate}
                  onSelectDate={setSelectedDate}
                  onNext={increaseStepIndex}
                />
              )}
              {/* eslint-disable-next-line security/detect-object-injection */}
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
              {/* eslint-disable-next-line security/detect-object-injection */}
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
              {/* eslint-disable-next-line security/detect-object-injection */}
              {STEPS[stepIndex]?.id === "confirm" && (
                <BookingConfirmStep
                  specialtyName={specialty.name}
                  selectedDate={selectedDate}
                  selectedTime={selectedTime}
                  selectedDoctorName={selectedDoctor ? `${selectedDoctor.firstName} ${selectedDoctor.lastName}` : null}
                  patientNotes={patientNotes}
                  onPatientNotesChange={setPatientNotes}
                  onConfirm={handleConfirm}
                  onGoToStep={goToStep}
                  canConfirm={Boolean(selectedDate && selectedTime && selectedDoctorId)}
                  submitting={submitting}
                  submitError={submitError}
                />
              )}
            </div>

            <BookingSummary
              specialtyName={specialty.name}
              selectedDate={selectedDate}
              selectedTime={selectedTime}
              selectedDoctorName={selectedDoctor ? `${selectedDoctor.firstName} ${selectedDoctor.lastName}` : null}
            />
          </div>
        </div>
      </section>
    </main>
  );
}
