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
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path
            d="M5 12h12.586l-3.293-3.293a1 1 0 0 1 1.414-1.414l5 5a1 1 0 0 1 0 1.414l-5 5a1 1 0 0 1-1.414-1.414L17.586 13H5a1 1 0 0 1 0-2Z"
            fill="currentColor"
          />
        </svg>
      </div>
    </button>
  );
};

export default SpecialtyCard;
