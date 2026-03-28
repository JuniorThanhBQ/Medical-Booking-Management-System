import { Link } from "react-router-dom";

export function BookingNotFoundView({ onBrowseSpecialties }) {
  return (
    <main className="booking">
      <section className="booking__shell">
        <div className="booking__container">
          <Link to="/dashboard" className="booking__back">
            <span aria-hidden="true">←</span> Về trang chủ
          </Link>
          <h1 className="booking__title">Không tìm thấy chuyên khoa</h1>
          <p className="booking__subtitle">
            Vui lòng quay lại trang chủ và chọn chuyên khoa.
          </p>
          <button
            type="button"
            className="booking__primary"
            onClick={onBrowseSpecialties}
          >
            Xem chuyên khoa
          </button>
        </div>
      </section>
    </main>
  );
}
