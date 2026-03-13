import './feature-sections.css'

const FEATURES = [
  {
    id: 'diagnostics',
    imgSide: 'left',
    badge: 'CHẨN ĐOÁN',
    title: 'Chẩn Đoán Hình Ảnh Não Bộ Chính Xác',
    desc: 'Hệ thống MRI hiện đại, chẩn đoán hình ảnh thần kinh chức năng và EEG giúp hiển thị rõ nhất tình trạng thần kinh của bạn – hỗ trợ chẩn đoán nhanh hơn, chính xác hơn, giảm số lần tái khám không cần thiết.',
    stats: [
      { value: '98%',  label: 'ĐỘ CHÍNH XÁC CHẨN ĐOÁN' },
      { value: '<48H', label: 'THỜI GIAN TRẢ KẾT QUẢ' },
      { value: '12+',  label: 'PHƯƠNG THỨC CHỤP ẢNH'  },
    ],
    secondaryCta: { label: 'Xem dịch vụ chẩn đoán hình ảnh',   href: '#services'    },
    card: {
      title: 'Phòng MRI Hiện Đại',
      sub:   'MRI từ trường cao 3T cho hình ảnh cực kỳ sắc nét',
    },
    img: {
      src: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=700&auto=format&fit=crop&q=80',
      srcSet: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&auto=format&fit=crop&q=70 400w, https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=700&auto=format&fit=crop&q=80 700w',
      alt: 'Bác sĩ thần kinh đang xem phim chụp MRI não',
    },
  },
  {
    id: 'treatment',
    imgSide: 'right',
    badge: 'ĐIỀU TRỊ',
    title: 'Phác Đồ Điều Trị Cá Nhân Hóa Hoàn Toàn',
    desc: 'Mỗi bệnh nhân đều được xây dựng phác đồ phù hợp với tình trạng, lối sống và mục tiêu riêng – được phối hợp chặt chẽ giữa bác sĩ thần kinh, các chuyên gia liên quan và gia đình bệnh nhân.',
    stats: [
      { value: '10K+', label: 'CA ĐIỀU TRỊ ĐÃ THỰC HIỆN' },
      { value: '92%',  label: 'TỶ LỆ PHỤC HỒI'        },
      { value: '30+',  label: 'BỆNH LÝ ĐƯỢC ĐIỀU TRỊ'   },
    ],
    secondaryCta: { label: 'Xem tất cả dịch vụ',     href: '#services'  },
    card: {
      title: 'Đội Ngũ Chuyên Gia',
      sub:   'Bác sĩ thần kinh và chuyên khoa được chứng nhận',
    },
    img: {
      src: 'https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=700&auto=format&fit=crop&q=80',
      srcSet: 'https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=400&auto=format&fit=crop&q=70 400w, https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=700&auto=format&fit=crop&q=80 700w',
      alt: 'Bác sĩ thần kinh đang xem kế hoạch điều trị cho bệnh nhân',
    },
  },
]

function FeatureBlock({ f }) {
  return (
    <div className={`fb ${f.imgSide === 'left' ? 'fb--img-left' : ''}`}>
      <div className="fb__content">
        <span className="fb__badge">{f.badge}</span>
        <h2 className="fb__title">{f.title}</h2>
        <p className="fb__desc">{f.desc}</p>

        <div className="fb__stats">
          {f.stats.map(s => (
            <div key={s.label} className="fb__stat">
              <span className="fb__stat-value">{s.value}</span>
              <span className="fb__stat-label">{s.label}</span>
            </div>
          ))}
        </div>

        <div className="fb__ctas">
          <a href={f.secondaryCta.href} className="fb__btn-link">
            {f.secondaryCta.label}
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
              <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor"
                strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
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

        <div className={`fb__card fb__card--${f.imgSide === 'left' ? 'right' : 'left'}`}>
          <div className="fb__card-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
              <path d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
          </div>
          <div>
            <p className="fb__card-title">{f.card.title}</p>
            <p className="fb__card-sub">{f.card.sub}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function FeatureSections() {
  return (
    <div className="feature-sections">
      {FEATURES.map(f => <FeatureBlock key={f.id} f={f} />)}
    </div>
  )
}
