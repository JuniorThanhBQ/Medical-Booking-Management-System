import { Link } from "react-router-dom";

export function BookingSuccessView({
  specialtyId,
  // specialtyName,  ==> Lỗi eslint được đánh dấu ngày 15/03/2026
  onBookAnother,
}) {
  return (
    <main className="booking">
      <section className="booking__shell">
        <div className="booking__success-container">
          <div className="booking__success">
            <div className="booking__success-badge">✓</div>
            <h1 className="booking__title">Appointment requested</h1>
            <p className="booking__subtitle">
              We saved your booking details. You can review it in your history
              later.
            </p>
            <div className="booking__success-actions">
              <Link to="/dashboard" className="booking__primary">
                Back to dashboard
              </Link>
              <Link
                to={`/specialties/${specialtyId}/book`}
                className="booking__secondary"
                onClick={onBookAnother}
              >
                Book another
              </Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
