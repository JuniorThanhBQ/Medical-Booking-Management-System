import "../../../css/feature-highlight-band.css";

export default function FeatureHighlightBand() {
  return (
    <section className="feature-highlight">
      <div className="lp-container feature-highlight__inner">
        <div className="feature-highlight__content">
          <p className="feature-highlight__eyebrow">CHĂM SÓC TOÀN DIỆN</p>

          <h2 className="feature-highlight__title">
            Một Bức Tranh Thống Nhất Cho Mỗi Bệnh Nhân
          </h2>

          <div className="feature-highlight__pills">
            <span className="feature-highlight__pill">
              Giảm số lần chụp lại
            </span>
            <span className="feature-highlight__pill">
              Ra quyết định hội chẩn nhanh hơn
            </span>
          </div>
        </div>

        <aside className="feature-highlight__aside">
          <div className="feature-highlight__stat">
            <p className="feature-highlight__stat-value">38%</p>
            <p className="feature-highlight__stat-label">
              GIẢM THỜI GIAN CHẨN ĐOÁN ĐỘT QUỴ
            </p>
          </div>
          <div className="feature-highlight__stat">
            <p className="feature-highlight__stat-value">2×</p>
            <p className="feature-highlight__stat-label">
              TĂNG GẤP ĐÔI TỐC ĐỘ PHỐI HỢP TRONG CA BỆNH PHỨC TẠP
            </p>
          </div>
          <div className="feature-highlight__divider" />
          <p className="feature-highlight__footnote">
            Các chỉ số tham chiếu từ những mạng lưới thần kinh học sử dụng quy
            trình làm việc thống nhất tương tự.
          </p>
        </aside>
      </div>
    </section>
  );
}
