export function RoleCard({ option, isSelected, onSelect }) {
  return (
    <button
      type="button"
      className={`signin-card ${isSelected ? " signin-card--selected" : ""}`}
      onClick={() => onSelect(option.id)}
    >


      <div className="signin-card__text">
        <div className="signin-card__title">
          {option.title}
        </div>
        <div className="signin-card__description">
          {option.description}
        </div>
      </div>


      <span className="signin-card__chevron">&#8594;</span>
    </button>
  );
}
