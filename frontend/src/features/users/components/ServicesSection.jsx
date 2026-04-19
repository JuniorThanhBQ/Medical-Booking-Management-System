import "@css/common/services.css";

import { getMedicalServiceDetail } from "@features/shared/services/public-api-service";
import useMedicalServices from "@features/users/hooks/use-services-section";
import { useState } from "react";

import { EditSquareIcon, GlobeIcon, ShieldIcon } from "@/assets/icons";

import { ServiceDetailModal } from "./ServiceDetailModal";

const getIconComponent = (iconName) => {
  const iconMap = {
    shield: <ShieldIcon size={20} />,
    globe: <GlobeIcon size={20} />,
    edit: <EditSquareIcon size={20} />,
  };
  return iconMap[iconName] || null;
};

export default function ServicesSection() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedService, setSelectedService] = useState(null);
  const [isLoadingDetail, setIsLoadingDetail] = useState(false);

  const {
    services,
    currentPage,
    totalPages,
    isTransitioning,
    handlePrev,
    handleNext,
  } = useMedicalServices(5);

  const handleViewDetail = async (serviceId) => {
    setIsLoadingDetail(true);
    try {
      const detail = await getMedicalServiceDetail(serviceId);
      setSelectedService(detail);
      setIsModalOpen(true);
    } catch (error) {
      console.error("Lỗi khi lấy chi tiết dịch vụ:", error);
    } finally {
      setIsLoadingDetail(false);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedService(null);
  };

  const getVisualProps = (id, index) => {
    const iconList = ["shield", "globe", "edit"];
    if (index % 2 === 0) {
      return { icon: iconList[index % 3] };
    } else {
      return { logoText: `MCK${id}` };
    }
  };

  const renderIconWrap = (visual) => {
    if (visual.logoText) {
      return <span className="service-card__logo-text">{visual.logoText}</span>;
    } else {
      return (
        <span className="service-card__icon">
          {getIconComponent(visual.icon)}
        </span>
      );
    }
  };

  const getGridStyle = () => {
    return {
      opacity: isTransitioning ? 0 : 1,
      transition: "opacity 0.3s ease-in-out",
    };
  };

  return (
    <section className="services" id="services">
      <div className="services__wrap lp-container">
        <h2 className="services__title">Và nhiều hơn nữa</h2>

        {!services || services.length === 0 ? (
          <div className="services__empty-state" style={{ textAlign: "center", padding: "3rem 0", color: "#666" }}>
            <p>Chưa có dịch vụ nào trong hệ thống.</p>
          </div>
        ) : (
          <>
            <div className="services__grid" style={getGridStyle()}>
              {services.map((svc, index) => {
                const visual = getVisualProps(svc.specialtyId, index);

                return (
                  <article key={svc.id} className="service-card">
                    <div className="service-card__icon-wrap">
                      {renderIconWrap(visual)}
                    </div>
                    <h3 className="service-card__name">{svc.name}</h3>
                    <p className="service-card__desc">{svc.description}</p>
                    <button
                      type="button"
                      className="service-card__badge service-card__badge--live btn-detail"
                      onClick={() => handleViewDetail(svc.id)}
                      disabled={isLoadingDetail}
                    >
                      Xem chi tiết
                    </button>
                  </article>
                );
              })}
            </div>

            {totalPages > 1 && (
              <div className="services__pagination">
                <button
                  onClick={handlePrev}
                  disabled={currentPage === 1 || isTransitioning}
                  className="services__pagination-btn"
                >
                  &lt;
                </button>
                <span className="services__pagination-text">
                  {currentPage} / {totalPages}
                </span>
                <button
                  onClick={handleNext}
                  disabled={currentPage === totalPages || isTransitioning}
                  className="services__pagination-btn"
                >
                  &gt;
                </button>
              </div>
            )}
          </>
        )}

        <ServiceDetailModal
          isOpen={isModalOpen}
          service={selectedService}
          onClose={handleCloseModal}
        />
      </div>
    </section>
  );
}