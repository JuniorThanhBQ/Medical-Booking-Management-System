import './services.css'

const SERVICES = [
  {
    id: 'mri',
    logoText: 'MRI',
    name: 'MRI & Chẩn đoán hình ảnh thần kinh',
    desc: 'MRI não tiên tiến, MRI chức năng, phổ cộng hưởng từ và chụp tưới máu cho chẩn đoán thần kinh toàn diện.',
    status: 'live',
  },
  {
    id: 'eeg',
    logoText: 'EEG',
    name: 'EEG & Động kinh',
    desc: 'EEG lưu động, điện não đồ video, quản lý động kinh và điều trị rối loạn co giật.',
    status: 'live',
  },
  {
    id: 'stroke',
    icon: 'shield',
    name: 'Chăm sóc đột quỵ',
    desc: 'Đáp ứng đột quỵ nhanh, phối hợp điều trị tPA, phục hồi chức năng sau đột quỵ và lập kế hoạch hồi phục lâu dài.',
    status: 'live',
  },
  {
    id: 'movement',
    icon: 'globe',
    name: 'Rối loạn vận động',
    desc: 'Chẩn đoán Parkinson, run vô căn, loạn trương lực và thất điều, quản lý thuốc và đánh giá chỉ định kích thích não sâu (DBS).',
    status: 'coming-soon',
  },
  {
    id: 'custom',
    icon: 'edit',
    name: 'Phác đồ chăm sóc theo yêu cầu',
    desc: 'Phác đồ chăm sóc thần kinh cá nhân hóa, theo dõi từ xa, phối hợp chuyên gia và tích hợp nhóm chăm sóc.',
    status: 'coming-soon',
  },
]

const ICONS = {
  shield: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  ),
  globe: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10A15.3 15.3 0 018 12 15.3 15.3 0 0112 2z" />
    </svg>
  ),
  edit: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
    </svg>
  ),
}

export default function ServicesSection() {
  return (
    <section className="services" id="services">
      <div className="services__wrap lp-container">
        <h2 className="services__title">Và nhiều hơn nữa</h2>

        <div className="services__grid">
          {SERVICES.map(svc => (
            <article key={svc.id} className="service-card">
              <div className="service-card__icon-wrap">
                {svc.logoText
                  ? <span className="service-card__logo-text">{svc.logoText}</span>
                  : <span className="service-card__icon">{ICONS[svc.icon]}</span>
                }
              </div>
              <h3 className="service-card__name">{svc.name}</h3>
              <p className="service-card__desc">{svc.desc}</p>
              <span className={`service-card__badge service-card__badge--${svc.status}`}>
                {svc.status === 'live' ? 'Đang hoạt động' : 'Sắp ra mắt'}
              </span>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
