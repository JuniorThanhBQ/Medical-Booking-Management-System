import { useCtaEmailForm } from "../hooks/use-cta-email-form";
import "@/assets/css/users/cta-banner.css";

export default function CtaBanner() {
  const { email, setEmail, submitting, handleSubmit } = useCtaEmailForm();

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
              Bạn là bác sĩ? Hãy gia nhập đội ngũ của chúng tôi ngay hôm nay để
              cùng nâng cao trải nghiệm và chất lượng chăm sóc cho bệnh nhân.
            </p>

            <form
              className="cta-banner__form"
              onSubmit={handleSubmit}
              noValidate
            >
              <div className="cta-banner__input-wrap">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M3 8l9 5 9-5M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                    stroke="currentColor"
                    strokeWidth="1.75"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <input
                  id="cta-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email công việc"
                  autoComplete="email"
                  required
                />
              </div>

              <button
                type="submit"
                className="cta-banner__submit"
                disabled={submitting}
              >
                {submitting ? "ĐANG GỬI…" : "THAM GIA"}
              </button>
            </form>

            <p className="cta-banner__disclaimer">
              KHÔNG SPAM &nbsp;·&nbsp; KHÔNG CẦN CHUẨN BỊ &nbsp;·&nbsp; PHẢN HỒI
              TRONG 2 GIỜ
            </p>
          </div>

          <div className="cta-banner__testimonial">
            <blockquote className="cta-banner__quote">
              "Nhóm của chúng tôi làm việc nhanh hơn vì mọi người đều hiểu rõ
              điều gì là đúng quy định. Đội ngũ chăm sóc giờ có thể tập trung
              vào công việc thực sự, thay vì phải chạy theo từng bước phê
              duyệt."
            </blockquote>
            <footer className="cta-banner__quote-footer">
              <p className="cta-banner__quote-role">
                TRƯỞNG BỘ PHẬN CHĂM SÓC BỆNH NHÂN
              </p>
              <p className="cta-banner__quote-org">Trung tâm y tế khu vực</p>
            </footer>
          </div>
        </div>
      </div>
    </section>
  );
}
