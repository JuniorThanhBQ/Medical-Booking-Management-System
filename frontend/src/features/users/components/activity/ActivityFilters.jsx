const ActivityFilters = ({ filters, activeKey, onChange }) => {
  return (
    <div className="profile-activity__filters">
      {filters.map((filter) => {
        const active = filter.key === activeKey;
        return (
          <button
            key={filter.key}
            type="button"
            className={`profile-activity__chip ${active ? "profile-activity__chip--active" : ""}`}
            onClick={() => onChange?.(filter.key)}
          >
            {filter.label}
          </button>
        );
      })}
    </div>
  );
};

export default ActivityFilters;
