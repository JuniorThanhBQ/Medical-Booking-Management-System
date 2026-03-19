import { Link } from "react-router-dom";

export function BookingSuccessView({
  specialtyId,
  onBookAnother,
}) {
  return (
    <main className="booking">
      <section className="booking__shell">
        <div className="booking__success-container">
          <div className="booking__success">
            <div className="booking__success-badge">✓</div>
            <h1 className="booking__title">Yêu cầu đặt lịch thành công</h1>
            <p className="booking__subtitle">
              Thông tin đặt lịch đã được lưu. Bạn có thể xem lại trong lịch sử.
            </p>
            <div className="booking__success-actions">
              <Link to="/dashboard" className="booking__primary">
                Về trang chủ
              </Link>
              <Link
                to={`/specialties/${specialtyId}/book`}
                className="booking__secondary"
                onClick={onBookAnother}
              >
                Đặt tiếp
              </Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
