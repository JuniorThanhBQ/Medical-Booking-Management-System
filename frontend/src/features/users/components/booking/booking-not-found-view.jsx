import { Link } from "react-router-dom";

export function BookingNotFoundView({ onBrowseSpecialties }) {
  return (
    <main className="booking">
      <section className="booking__shell">
        <div className="booking__container">
          <Link to="/dashboard" className="booking__back">
            <span aria-hidden="true">←</span> Back to Dashboard
          </Link>
          <h1 className="booking__title">Specialty not found</h1>
          <p className="booking__subtitle">
            Please start from the dashboard and choose a specialty.
          </p>
          <button
            type="button"
            className="booking__primary"
            onClick={onBrowseSpecialties}
          >
            Browse specialties
          </button>
        </div>
      </section>
    </main>
  );
}
