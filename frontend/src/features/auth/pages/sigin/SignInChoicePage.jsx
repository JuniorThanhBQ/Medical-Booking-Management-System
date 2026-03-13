import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './signin-choice.css'

const OPTIONS = [
  {
    id: 'patient',
    title: 'Dành cho bệnh nhân',
    description: 'Đặt lịch hẹn và tra cứu hồ sơ y tế',
  },
  {
    id: 'doctor',
    title: 'Dành cho bác sĩ',
    description: 'Đăng ký và tra cứu hồ sơ y tế',
  },
]

export default function SignInChoicePage() {
  const navigate = useNavigate()
  const [selected, setSelected] = useState(null)

  const handleSelect = (id) => {
    setSelected(id)
  }

  return (
    <div className="signin-page">
      <header className="signin-page__header">
        <button
          type="button"
          aria-label="Quay lại"
          className="signin-page__back"
          onClick={() => navigate('/')}
        >
          <span aria-hidden="true" className="signin-page__back-icon">
            &#8592;
          </span>
        </button>
      </header>

      <main className="signin-page__main" >
        <h1 className="signin-page__title">
          Đăng ký/đăng nhập
        </h1>

        <div className="signin-page__cards">
          {OPTIONS.map((option) => (
            <button
              key={option.id}
              type="button"
              className={`signin-card${selected === option.id ? ' signin-card--selected' : ''}`}
              onClick={() => handleSelect(option.id)}
            >
              <div className="signin-card__text">
                <div className="signin-card__title">{option.title}</div>
                <div className="signin-card__description">{option.description}</div>
              </div>
              <span className="signin-card__chevron">
                →
              </span>
            </button>
          ))}
        </div>

        {selected && (
          <p className="signin-page__selection-hint">
            Đã chọn:&nbsp;
            <strong>{selected === 'patient' ? 'Patient' : 'Doctor'}</strong>
          </p>
        )}
      </main>

      <footer className="signin-page__footer">
        <button type="button" className="signin-footer__link">
          <span className="signin-footer__icon">
            ?
          </span>
          Trợ giúp và hỗ trợ
        </button>
      </footer>
    </div>
  )
}

