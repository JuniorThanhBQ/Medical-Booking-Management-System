import { ShieldIcon, GlobeIcon, EditSquareIcon } from "@/assets/icons";
import "@/assets/css/users/services.css";

const SERVICES = [
  {
    id: "mri",
    logoText: "MRI",
    name: "MRI & Chẩn đoán hình ảnh thần kinh",
    desc: "MRI não tiên tiến, MRI chức năng, phổ cộng hưởng từ và chụp tưới máu cho chẩn đoán thần kinh toàn diện.",
    status: "live",
  },
  {
    id: "eeg",
    logoText: "EEG",
    name: "EEG & Động kinh",
    desc: "EEG lưu động, điện não đồ video, quản lý động kinh và điều trị rối loạn co giật.",
    status: "live",
  },
  {
    id: "stroke",
    icon: "shield",
    name: "Chăm sóc đột quỵ",
    desc: "Đáp ứng đột quỵ nhanh, phối hợp điều trị tPA, phục hồi chức năng sau đột quỵ và lập kế hoạch hồi phục lâu dài.",
    status: "live",
  },
  {
    id: "movement",
    icon: "globe",
    name: "Rối loạn vận động",
    desc: "Chẩn đoán Parkinson, run vô căn, loạn trương lực và thất điều, quản lý thuốc và đánh giá chỉ định kích thích não sâu (DBS).",
    status: "coming-soon",
  },
  {
    id: "custom",
    icon: "edit",
    name: "Phác đồ chăm sóc theo yêu cầu",
    desc: "Phác đồ chăm sóc thần kinh cá nhân hóa, theo dõi từ xa, phối hợp chuyên gia và tích hợp nhóm chăm sóc.",
    status: "coming-soon",
  },
];

const getIconComponent = (iconName) => {
  const iconMap = {
    shield: <ShieldIcon size={20} />,
    globe: <GlobeIcon size={20} />,
    edit: <EditSquareIcon size={20} />,
  };
  return iconMap[iconName] || null;
};

export default function ServicesSection() {
  return (
    <section className="services" id="services">
      <div className="services__wrap lp-container">
        <h2 className="services__title">Và nhiều hơn nữa</h2>

        <div className="services__grid">
          {SERVICES.map((svc) => (
            <article key={svc.id} className="service-card">
              <div className="service-card__icon-wrap">
                {svc.logoText ? (
                  <span className="service-card__logo-text">
                    {svc.logoText}
                  </span>
                ) : (
                  <span className="service-card__icon">{getIconComponent(svc.icon)}</span>
                )}
              </div>
              <h3 className="service-card__name">{svc.name}</h3>
              <p className="service-card__desc">{svc.desc}</p>
              <span
                className={`service-card__badge service-card__badge--${svc.status}`}
              >
                {svc.status === "live" ? "Đang hoạt động" : "Sắp ra mắt"}
              </span>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
