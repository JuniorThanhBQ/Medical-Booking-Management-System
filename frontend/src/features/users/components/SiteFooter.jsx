import "@/assets/css/users/footer.css";

const NAV_COLS = {
  "Trang web": ["Về chúng tôi"],
  "Thông tin mở": ["Đặt lịch hẹn", "Tra cứu bác sĩ", "Xem dịch vụ"],
  "Câu hỏi thường gặp": ["Giới thiệu", "Quyền riêng tư", "Bảo mật", "Liên hệ"],
  "Đại học Mở TP.HCM": ["Web", "Facebook", "Youtube"],
};

export default function SiteFooter() {
  const year = new Date().getFullYear();

  return (
    <footer className="site-footer" id="footer">
      <div className="site-footer__inner lp-container">
        <div className="site-footer__brand">
          <h2 className="site-footer__logo">Medical Appointment B3</h2>
          <p className="site-footer__tagline">Đặt lịch hẹn khám bệnh nhanh chóng và tiện lợi qua hệ thống trực tuyến của chúng tôi</p>
        </div>

        <nav className="site-footer__nav">
          {Object.entries(NAV_COLS).map(([col, links]) => (
            <div key={col} className="site-footer__col">
              <h4 className="site-footer__col-head">{col}</h4>
              <ul className="site-footer__col-list">
                {links.map((link) => (
                  <li key={link}>
                    <a href="#" className="site-footer__link">
                      {link}
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
            <a href="https://ou.edu.vn/">Đồ án thuộc trường Đại học Mở Thành phố Hồ Chí Minh</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
