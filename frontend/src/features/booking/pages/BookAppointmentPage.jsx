import "@css/users/booking.css";

import { useBookAppointmentPage } from "@features/booking/hooks/use-booking-appointment-page";
import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { Link } from "react-router-dom";

import { STEPS } from "@/utils/booking-utils.js";

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
  const {
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
  } = useBookAppointmentPage();

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
      <BookingNotFoundView onBrowseSpecialties={handleBrowseSpecialties} />
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
                <span aria-hidden="true">&#8592;</span> {specialty.name}
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
