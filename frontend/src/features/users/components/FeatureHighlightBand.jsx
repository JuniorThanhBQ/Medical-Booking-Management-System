import "@css/common/feature-highlight.css";

export default function FeatureHighlightBand() {
  return (
    <section className="feature-highlight">
      <div className="lp-container feature-highlight__inner">
        <div className="feature-highlight__content">
          <p className="feature-highlight__eyebrow">DỊCH VỤ CHUYÊN NGHIỆP</p>

          <h2 className="feature-highlight__title">
            Hệ Thống Đặt Lịch Khám Thông Minh Và Toàn Diện
          </h2>

          <div className="feature-highlight__pills">
            <span className="feature-highlight__pill">
              Chủ động thời gian thăm khám
            </span>
            <span className="feature-highlight__pill">
              Kết nối bác sĩ chuyên khoa nhanh chóng
            </span>
          </div>
        </div>

        <aside className="feature-highlight__aside">
          <div className="feature-highlight__stat">
            <p className="feature-highlight__stat-value">85%</p>
            <p className="feature-highlight__stat-label">
              GIẢM THỜI GIAN CHỜ ĐỢI TẠI QUẦY TIẾP ĐÓN
            </p>
          </div>
          <div className="feature-highlight__stat">
            <p className="feature-highlight__stat-value">5 Phút</p>
            <p className="feature-highlight__stat-label">
              THỜI GIAN TRUNG BÌNH ĐỂ HOÀN TẤT ĐẶT LỊCH TRỰC TUYẾN
            </p>
          </div>
          <div className="feature-highlight__divider" />
          <p className="feature-highlight__footnote">
            Các chỉ số dựa trên khảo sát thực tế về trải nghiệm người dùng trên
            hệ thống quản lý lịch hẹn của chúng tôi.
          </p>
        </aside>
      </div>
    </section>
  );
}
