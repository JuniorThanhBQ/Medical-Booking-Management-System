import "@css/shared/feature-sections.css";

import { ArrowRightIcon, BadgeCheckIcon } from "@/assets/icons";

const FEATURES = [
  {
    id: "booking-service",
    imgSide: "left",
    badge: "DỊCH VỤ",
    title: "Quy Trình Đặt Lịch Hoàn Toàn Tự Động",
    desc: "Hệ thống quản lý lịch hẹn thông minh giúp tối ưu hóa thời gian của bệnh nhân. Với tính năng tự động gửi thông báo nhắc hẹn qua email và hệ thống, bạn sẽ luôn chủ động trong việc sắp xếp thời gian thăm khám mà không lo bỏ lỡ các đợt kiểm tra quan trọng.",
    stats: [
      { value: "100%", label: "TỰ ĐỘNG THÔNG BÁO" },
      { value: "<3 Phút", label: "HOÀN TẤT ĐẶT LỊCH" },
      { value: "24/7", label: "HỆ THỐNG TRỰC TUYẾN" },
    ],
    secondaryCta: {
      label: "Tìm hiểu quy trình đặt lịch",
      href: "#services",
    },
    card: {
      title: "Thông Báo Thông Minh",
      sub: "Tự động gửi lời nhắc và cập nhật trạng thái lịch hẹn",
    },
    img: {
      src: "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=700&auto=format&fit=crop&q=80",
      srcSet:
        "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=400&auto=format&fit=crop&q=70 400w, https://images.unsplash.com/photo-1516549655169-df83a0774514?w=700&auto=format&fit=crop&q=80 700w",
      alt: "Giao diện quản lý lịch hẹn y tế chuyên nghiệp",
    },
  },
  {
    id: "medical-team",
    imgSide: "right",
    badge: "ĐỘI NGŨ",
    title: "Kết Nối Trực Tiếp Với Chuyên Gia",
    desc: "Chúng tôi quy tụ đội ngũ bác sĩ có chuyên môn cao và giàu kinh nghiệm trong nhiều lĩnh vực thăm khám. Thông qua hệ thống, bệnh nhân có thể dễ dàng xem hồ sơ năng lực và lựa chọn bác sĩ phù hợp nhất cho nhu cầu chăm sóc sức khỏe cá nhân.",
    stats: [
      { value: "50+", label: "BÁC SĨ CHUYÊN KHOA" },
      { value: "15+", label: "NĂM KINH NGHIỆM" },
      { value: "100%", label: "TẬN TÂM CHĂM SÓC" },
    ],
    secondaryCta: { label: "Xem danh sách bác sĩ", href: "/dashboard" },
    card: {
      title: "Chuyên Gia Đầu Ngành",
      sub: "Đội ngũ được đào tạo bài bản và cấp phép hành nghề",
    },
    img: {
      src: "https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=700&auto=format&fit=crop&q=80",
      srcSet:
        "https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=400&auto=format&fit=crop&q=70 400w, https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=700&auto=format&fit=crop&q=80 700w",
      alt: "Đội ngũ bác sĩ đang thảo luận chuyên môn",
    },
  },
];

function FeatureBlock({ f }) {
  return (
    <div className={`fb ${f.imgSide === "left" ? "fb--img-left" : ""}`}>
      <div className="fb__content">
        <span className="fb__badge">{f.badge}</span>
        <h2 className="fb__title">{f.title}</h2>
        <p className="fb__desc">{f.desc}</p>

        <div className="fb__stats">
          {f.stats.map((s) => (
            <div key={s.label} className="fb__stat">
              <span className="fb__stat-value">{s.value}</span>
              <span className="fb__stat-label">{s.label}</span>
            </div>
          ))}
        </div>

        <div className="fb__ctas">
          <a href={f.secondaryCta.href} className="fb__btn-link">
            {f.secondaryCta.label}
            <ArrowRightIcon size={15} />
          </a>
        </div>
      </div>

      <div className="fb__media">
        <div className="fb__img-wrap">
          <img
            src={f.img.src}
            srcSet={f.img.srcSet}
            sizes="50vw"
            alt={f.img.alt}
            loading="lazy"
            width="700"
            height="525"
          />
        </div>

        <div
          className={`fb__card fb__card--${f.imgSide === "left" ? "right" : "left"}`}
        >
          <div className="fb__card-icon">
            <BadgeCheckIcon size={20} className="fb__card-badge" />
          </div>
          <div>
            <p className="fb__card-title">{f.card.title}</p>
            <p className="fb__card-sub">{f.card.sub}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function FeatureSections() {
  return (
    <div className="feature-sections">
      {FEATURES.map((f) => (
        <FeatureBlock key={f.id} f={f} />
      ))}
    </div>
  );
}
