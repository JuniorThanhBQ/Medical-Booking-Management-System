import { useState, useMemo } from "react";
import ActivityFilters from "./ActivityFilters";
import UpcomingActivityCard from "./UpcomingActivityCard";
import PastActivityList from "./PastActivityList";
import ActivityDetailPanel from "./ActivityDetailPanel";

const ActivityView = ({
  filters = [],
  items = [],
  upcomingItems = [],
  loading = false,
  error = "",
}) => {
  const [activeFilter, setActiveFilter] = useState("all");
  const [selectedId, setSelectedId] = useState(items[0]?.id ?? null);

  const filteredItems = useMemo(() => {
    if (activeFilter === "all") return items;
    return items.filter((it) => it.type === activeFilter);
  }, [activeFilter, items]);

  const selectedItem = filteredItems.find((it) => it.id === selectedId) ?? null;

  const handleFilterChange = (nextFilter) => {
    setActiveFilter(nextFilter);
    const nextItems = nextFilter === "all" ? items : items.filter((it) => it.type === nextFilter);
    setSelectedId(nextItems[0]?.id ?? null);
  };

  if (loading) {
    return (
      <section className="profile-activity">
        <p className="profile-activity__muted">Đang tải hoạt động...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="profile-activity">
        <p className="profile-activity__muted">{error}</p>
      </section>
    );
  }

  if (!items.length && !upcomingItems.length) {
    return (
      <section className="profile-activity">
        <p className="profile-activity__muted">Chưa có hoạt động nào.</p>
      </section>
    );
  }

  return (
    <section className="profile-activity">
      <div className="profile-activity__left">
        <ActivityFilters
          filters={filters}
          activeKey={activeFilter}
          onChange={handleFilterChange}
        />

        <div className="profile-activity__section-title-row">
          <h3 className="profile-activity__section-title">Sắp tới</h3>
          <span className="profile-activity__count">
            {upcomingItems.length}
          </span>
        </div>

        <UpcomingActivityCard items={upcomingItems} />

        <h3 className="profile-activity__section-title">Đã qua</h3>
        <PastActivityList
          items={filteredItems}
          selectedId={selectedId}
          onSelect={setSelectedId}
        />
      </div>

      <ActivityDetailPanel item={selectedItem} />
    </section>
  );
};

export default ActivityView;
