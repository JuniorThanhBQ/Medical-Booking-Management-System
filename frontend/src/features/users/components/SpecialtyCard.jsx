import { ArrowRightFilledIcon } from "@/assets/icons";
import { CTA_DISPLAY_MAP } from "@/configs/const";

const SpecialtyCard = ({ specialty, onClick }) => {
  const { id, level, name, description, images } = specialty;

  return (
    <button
      key={id}
      type="button"
      className="dashboard-specialty-card"
      onClick={onClick}
    >
      <div
        className="dashboard-specialty-card__media"
        style={{ backgroundImage: `url(${images})` }}
      />

      <div className="dashboard-specialty-card__meta">{level}</div>

      <div className="dashboard-specialty-card__name">{name}</div>

      <p className="dashboard-specialty-card__description">{description}</p>
    </button>
  );
};

export default SpecialtyCard;
