import "@/assets/css/users/booking.css";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useMemo } from "react";
import { SPECIALTIES } from "@/data/mocks/specialties";
import { DOCTORS } from "@/data/mocks/doctors";
import { useBookingStore } from "../hooks/use-booking-store";
import { STEPS, toISODate, buildTimeSlots } from "../utils/booking-utils";
import { AVAILABLE_BOOKING_DAYS } from "@/configs/const";
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
    stepIndex,
    selectedDate,
    selectedTime,
    selectedDoctorId,
    patientNotes,
    confirmed,
    setSelectedDate,
    setSelectedTime,
    setSelectedDoctorId,
    setPatientNotes,
    goToStep,
    increaseStepIndex,
    resetBooking,
    confirmBooking,
  } = useBookingStore();

  const numericSpecialtyId = Number(specialtyId);

  const specialty = SPECIALTIES.find((s) => s.id === numericSpecialtyId);

  const doctorsForSpecialty = useMemo(
    () => DOCTORS.filter((d) => d.specialtyId === numericSpecialtyId),
    [numericSpecialtyId],
  );

  const availableDays = useMemo(() => {
    const base = new Date();
    base.setHours(0, 0, 0, 0);
    const days = [];
    for (let i = 0; i < AVAILABLE_BOOKING_DAYS; i += 1) {
      const d = new Date(base);
      d.setDate(base.getDate() + i);
      days.push(d);
    }
    console.log(days);
    return days;
  }, []);

  const timeSlots = useMemo(() => buildTimeSlots(selectedDate), [selectedDate]);

  const selectedDoctor = useMemo(
    () => doctorsForSpecialty.find((d) => d.id === selectedDoctorId) ?? null,
    [doctorsForSpecialty, selectedDoctorId],
  );

  const handleConfirm = () => {
    confirmBooking({
      specialtyId,
      specialtyName: specialty?.name ?? specialtyId,
      date: selectedDate ? toISODate(selectedDate) : null,
      startTime: selectedTime,
      doctorId: selectedDoctor?.id ?? null,
      doctorName: selectedDoctor ? `${selectedDoctor.firstName} ${selectedDoctor.lastName}` : null,
      notes: patientNotes.trim() || null,
    });
  };

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
              <Link
                to={`/specialties/${specialtyId}`}
                className="booking__back"
              >
                <span aria-hidden="true">←</span> {specialty.name}
              </Link>
              <h1 className="booking__title">Đặt lịch khám</h1>
              <p className="booking__subtitle">
                Chọn ngày, giờ, bác sĩ và xác nhận đầy đủ thông tin.
              </p>
            </div>
            <BookingStepper stepIndex={stepIndex} onGoToStep={goToStep} />
          </div>

          <div className="booking__grid">
            <div className="booking__panel">
              {/* Lỗi eslint được đánh dấu ngày 15/03/2026 False Positive*/}
              {/* eslint-disable-next-line security/detect-object-injection*/}
              {STEPS[stepIndex]?.id === "day" && (
                <BookingDayStep
                  availableDays={availableDays}
                  selectedDate={selectedDate}
                  onSelectDate={setSelectedDate}
                  onNext={increaseStepIndex}
                />
              )}
              {/* Lỗi eslint được đánh dấu ngày 15/03/2026 */}
              {/* eslint-disable-next-line security/detect-object-injection*/}
              {STEPS[stepIndex]?.id === "time" && (
                <BookingTimeStep
                  timeSlots={timeSlots}
                  selectedDate={selectedDate}
                  selectedTime={selectedTime}
                  onSelectTime={setSelectedTime}
                  onNext={increaseStepIndex}
                />
              )}
              {/* Lỗi eslint được đánh dấu ngày 15/03/2026 */}
              {/* eslint-disable-next-line security/detect-object-injection*/}
              {STEPS[stepIndex]?.id === "doctor" && (
                <BookingDoctorStep
                  doctorsForSpecialty={doctorsForSpecialty}
                  selectedDate={selectedDate}
                  selectedTime={selectedTime}
                  selectedDoctorId={selectedDoctorId}
                  onSelectDoctor={setSelectedDoctorId}
                  onNext={increaseStepIndex}
                />
              )}
              {/* Lỗi eslint được đánh dấu ngày 15/03/2026 */}
              {/* eslint-disable-next-line security/detect-object-injection*/}
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
                  canConfirm={Boolean(
                    selectedDate && selectedTime && selectedDoctorId,
                  )}
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
