import './footer.css'

const NAV_COLS = {
  'Trang web': ['Về chúng tôi'],
  'Dịch vụ': ['MRI & Chẩn đoán hình ảnh', 'EEG & Động kinh', 'Chăm sóc đột quỵ', 'Chăm sóc trí nhớ', 'Rối loạn vận động', 'Phòng khám đau đầu', 'Phẫu thuật thần kinh', 'Thần kinh nhi'],
  'Thông tin bệnh nhân': ['Đặt lịch hẹn', 'Bảo hiểm', 'Hồ sơ y tế'],
  'Câu hỏi thường gặp': ['Giới thiệu', 'Quyền riêng tư', 'Bảo mật', 'Liên hệ'],
}

export default function SiteFooter() {
  const year = new Date().getFullYear()

  return (
    <footer className="site-footer" id="footer">
      <div className="site-footer__inner lp-container">

        <div className="site-footer__brand">
          <a href="#hero" className="site-footer__logo">
            <svg width="26" height="26" viewBox="0 0 28 28" fill="none">
              <circle cx="14" cy="14" r="14" fill="#2563EB" />
              <circle cx="14" cy="14" r="5" fill="white" />
              <circle cx="14" cy="14" r="2" fill="#2563EB" />
            </svg>
            <span className="site-footer__tagline">
              Được tạo bởi <a href="#team">XXX Team</a>
            </span>
          </a>
        </div>

        <nav className="site-footer__nav">
          {Object.entries(NAV_COLS).map(([col, links]) => (
            <div key={col} className="site-footer__col">
              <h4 className="site-footer__col-head">{col}</h4>
              <ul className="site-footer__col-list">
                {links.map(link => (
                  <li key={link}>
                    <a href="#" className="site-footer__link">{link}</a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>

      </div>

      <div className="site-footer__bottom">
        <div className="lp-container site-footer__bottom-inner">
          <p>© {year}</p>
          <div className="site-footer__bottom-links">
            <a href="#">Chính sách quyền riêng tư</a>
            <a href="#">Điều khoản dịch vụ</a>
            <a href="#">Chính sách cookie</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
