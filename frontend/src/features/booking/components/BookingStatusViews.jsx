import { Link } from "react-router-dom";

export function BookingStatusViews({
  variant = "success",
  specialtyId,
  onBookAnother,
  onBrowseSpecialties,
}) {
  const isSuccess = variant === "success";

  return (
    <main className="booking">
      <section className="booking__shell">
        <div
          className={
            isSuccess
              ? "booking__success-container"
              : "booking__container"
          }
        >
          {isSuccess ? (
            <div className="booking__success">
              <div className="booking__success-badge">✓</div>

              <h1 className="booking__title">
                Yêu cầu đặt lịch thành công
              </h1>

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
          ) : (
            <>
              <Link to="/dashboard" className="booking__back">
                <span aria-hidden="true">←</span> Về trang chủ
              </Link>

              <h1 className="booking__title">
                Không tìm thấy chuyên khoa
              </h1>

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
            </>
          )}
        </div>
      </section>
    </main>
  );
}