import { ArrowRightFilledIcon } from "@/assets/icons";

const SpecialtyCard = ({ specialty, onClick }) => {
  const { id, level, name, description, ctaLabel } = specialty;

  return (
    <button
      key={id}
      type="button"
      className="dashboard-specialty-card"
      onClick={onClick}
    >
      <div className="dashboard-specialty-card__media" />

      <div className="dashboard-specialty-card__meta">{level}</div>

      <div className="dashboard-specialty-card__name">{name}</div>

      <p className="dashboard-specialty-card__description">{description}</p>

      <div className="dashboard-specialty-card__cta">
        {ctaLabel}
        <ArrowRightFilledIcon size={24} aria-hidden="true" />
      </div>
    </button>
  );
};

export default SpecialtyCard;
