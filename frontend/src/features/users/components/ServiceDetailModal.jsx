import "@css/common/service-detail.css";

import { useNavigate } from "react-router-dom";

export function ServiceDetailModal({ isOpen, service, onClose }) {
  const navigate = useNavigate();

  if (!isOpen || !service) return null;

  const handleBooking = () => {
    if (service?.specialty?.id) {
      navigate(`/specialties/${service.specialty.id}/book`);
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} aria-label="Close">
          ×
        </button>

        <div className="service-detail">
          <h2 className="service-detail__title">{service.name}</h2>

          <p className="service-detail__description">{service.description}</p>

          {service.specialty && (
            <div className="service-detail__section">
              <h3 className="service-detail__section-title">Chuyên khoa</h3>
              <div className="service-detail__info-row">
                <span className="service-detail__label">Tên:</span>
                <span className="service-detail__value">
                  {service.specialty.name}
                </span>
              </div>
              {service.specialty.level && (
                <div className="service-detail__info-row">
                  <span className="service-detail__label">Cấp độ:</span>
                  <span className="service-detail__value">
                    {service.specialty.level}
                  </span>
                </div>
              )}
            </div>
          )}

          {service.visitType && (
            <div className="service-detail__section">
              <h3 className="service-detail__section-title">Thông tin khám</h3>
              <div className="service-detail__info-row">
                <span className="service-detail__label">Loại khám:</span>
                <span className="service-detail__value">
                  {service.visitType.name}
                </span>
              </div>
              {service.visitType.durationMinutes && (
                <div className="service-detail__info-row">
                  <span className="service-detail__label">Thời gian:</span>
                  <span className="service-detail__value">
                    {service.visitType.durationMinutes} phút
                  </span>
                </div>
              )}
            </div>
          )}

          <div className="service-detail__actions">
            <button
              className="service-detail__btn service-detail__btn--primary"
              onClick={handleBooking}
            >
              Đặt lịch khám
            </button>
            <button
              className="service-detail__btn service-detail__btn--secondary"
              onClick={onClose}
            >
              Đóng
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
