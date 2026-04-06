import { ChevronRightIcon } from "@/assets/icons";

const PastActivityList = ({ items, selectedId, onSelect }) => {
  if (!items.length) {
    return (
      <div className="profile-activity__muted">
        Không tìm thấy hoạt động nào cho bộ lọc này.
      </div>
    );
  }
  return (
    <div className="profile-activity__list">
      {items.map((item) => {
        const active = item.id === selectedId;
        return (
          <button
            key={item.id}
            type="button"
            className={`profile-activity__row ${active ? "profile-activity__row--active" : ""}`}
            onClick={() => onSelect?.(item.id)}
          >
            <div>
              <p className="profile-activity__row-title">{item.title}</p>
              <p className="profile-activity__row-meta">{item.meta}</p>
            </div>
            <div className="profile-activity__row-right">
              <ChevronRightIcon size={16} />
            </div>
          </button>
        );
      })}
    </div>
  );
};

export default PastActivityList;

