import "@css/common/footer.css";

const NAV_COLS = {
  "Trang web": [{ label: "Về chúng tôi", href: "#" }],
  "Thông tin mở": [
    { label: "Đặt lịch hẹn", href: "/dashboard" },
    { label: "Tra cứu bác sĩ", href: "/dashboard" },
    { label: "Xem dịch vụ", href: "/dashboard" },
  ],
  "Câu hỏi thường gặp": [
    { label: "Giới thiệu", href: "#" },
    { label: "Quyền riêng tư", href: "#" },
    { label: "Bảo mật", href: "#" },
    { label: "Liên hệ", href: "#" },
  ],
  "Đại học Mở TP.HCM": [
    { label: "Web", href: "https://ou.edu.vn/" },
    { label: "Facebook", href: "https://www.facebook.com/TruongDaiHocMo" },
    { label: "Youtube", href: "https://www.youtube.com/ou" },
  ],
};

export default function SiteFooter() {
  const year = new Date().getFullYear();

  return (
    <footer className="site-footer" id="footer">
      <div className="site-footer__inner lp-container">
        <div className="site-footer__brand">
          <h2 className="site-footer__logo">Medical Appointment B3</h2>
          <p className="site-footer__tagline">
            Đặt lịch hẹn khám bệnh nhanh chóng và tiện lợi qua hệ thống trực
            tuyến của chúng tôi
          </p>
        </div>

        <nav className="site-footer__nav">
          {Object.entries(NAV_COLS).map(([col, links]) => (
            <div key={col} className="site-footer__col">
              <h4 className="site-footer__col-head">{col}</h4>
              <ul className="site-footer__col-list">
                {links.map((link) => (
                  <li key={link.label}>
                    <a href={link.href} className="site-footer__link">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </div>

      <div className="site-footer__bottom">
        <div className="lp-container site-footer__bottom-inner">
          <p>© {year} Medical Appointment B3. All rights reserved.</p>
          <div className="site-footer__bottom-links">
            <a
              href="https://ou.edu.vn/"
              target="_blank"
              rel="noopener noreferrer"
            >
              Đồ án thuộc trường Đại học Mở Thành phố Hồ Chí Minh
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
