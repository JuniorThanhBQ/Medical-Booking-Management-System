import "@css/common/cta-banner.css";

import { Link } from "react-router-dom";

export default function CtaBanner() {
  return (
    <section className="cta-banner cta-banner--flush-footer" id="contact">
      <div className="lp-container">
        <div className="cta-banner__card">
          <div className="cta-banner__content">
            <p className="cta-banner__eyebrow">SỨC KHỎE CỦA MỌI NGƯỜI</p>

            <h2 className="cta-banner__title">
              Mang đến trải nghiệm tốt nhất cho bệnh nhân
            </h2>

            <p className="cta-banner__desc">
              Bạn muốn gia nhập đội ngũ của chúng tôi? Hãy gửi thông tin nghiệp
              vụ của bạn ngay bây giờ để trở thành một phần của gia đình MAB3.
            </p>

            <Link to="/doctor-registration" className="cta-banner__submit">
              ĐĂNG KÝ TUYỂN DỤNG
            </Link>

            <p className="cta-banner__disclaimer">
              KHÔNG SPAM &nbsp;·&nbsp; THÔNG TIN CHUẨN XÁC &nbsp;·&nbsp; PHẢN
              HỒI TRONG 24 GIỜ
            </p>
          </div>

          <div className="cta-banner__testimonial">
            <blockquote className="cta-banner__quote">
              &quot;Nhóm của chúng tôi làm việc nhanh hơn vì mọi người đều hiểu
              rõ điều gì là đúng quy định. Đội ngũ chăm sóc giờ có thể tập trung
              vào công việc thực sự, thay vì phải chạy theo từng bước phê
              duyệt.&quot;
            </blockquote>
            <footer className="cta-banner__quote-footer">
              <p className="cta-banner__quote-role">
                TRƯỞNG PHÒNG BỘ PHẬN QUẢN LÝ CHẤT LƯỢNG NHÂN SỰ
              </p>
              <p className="cta-banner__quote-org">Medical Appointment B3</p>
            </footer>
          </div>
        </div>
      </div>
    </section>
  );
}
