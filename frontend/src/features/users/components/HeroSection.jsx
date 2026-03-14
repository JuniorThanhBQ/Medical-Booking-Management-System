import "../../../css/hero.css";

const STATS = [
  { value: "24/7", label: "Cấp cứu thần kinh 24/7" },
  { value: "15+", label: "Bác sĩ thần kinh chuyên khoa" },
  { value: "95%", label: "Mức độ hài lòng của bệnh nhân" },
  { value: "50K+", label: "Bệnh nhân đã được điều trị" },
];

export default function HeroSection() {
  return (
    <section className="hero" id="hero">
      <div className="hero__bg">
        <img
          src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1600&auto=format&fit=crop&q=85"
          alt=""
          fetchPriority="high"
          decoding="async"
        />
        <div className="hero__overlay" />
      </div>

      <div className="hero__body">
        <div className="hero__content">
          <span className="hero__badge">Đa khoa</span>

          <h1 className="hero__title">
            Open 
            <br />
            Medical 
            <br />
            Appointment 
          </h1>

          <p className="hero__desc">
            Đội ngũ bác sĩ giàu kinh nghiệm. Chăm sóc toàn diện cho não bộ và hệ
            thần kinh – từ chẩn đoán chính xác đến phác đồ điều trị cá nhân hóa,
            lâu dài.
          </p>

          <div className="hero__ctas">
            <a href="/dashboard" className="hero__btn-primary">
              Đặt lịch tư vấn
            </a>
            <a href="#services" className="hero__btn-ghost">
              Xem tất cả dịch vụ
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                <path
                  d="M5 12h14M13 6l6 6-6 6"
                  stroke="currentColor"
                  strokeWidth="2.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </a>
          </div>
        </div>
      </div>

      <div className="hero__stats-strip">
        <div className="hero__stats-inner lp-container">
          {STATS.map((s) => (
            <div key={s.label} className="hero__stat">
              <span className="hero__stat-value">{s.value}</span>
              <span className="hero__stat-label">{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
