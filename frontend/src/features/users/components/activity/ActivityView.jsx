import { useMemo, useState } from "react";
import ActivityFilters from "./ActivityFilters";
import UpcomingActivityCard from "./UpcomingActivityCard";
import PastActivityList from "./PastActivityList";
import ActivityDetailPanel from "./ActivityDetailPanel";

const ActivityView = ({ filters = [], items = [] }) => {
  const [activeFilter, setActiveFilter] = useState("all");
  const [selectedId, setSelectedId] = useState(items[0]?.id ?? null);

  const filteredItems = useMemo(() => {
    if (activeFilter === "all") return items;
    return items.filter((it) => it.type === activeFilter);
  }, [activeFilter, items]);

  const effectiveSelectedId = useMemo(() => {
    if (!filteredItems.length) return null;
    if (selectedId && filteredItems.some((it) => it.id === selectedId)) return selectedId;
    return filteredItems[0].id;
  }, [filteredItems, selectedId]);

  const selectedItem = useMemo(
    () => filteredItems.find((it) => it.id === effectiveSelectedId) ?? null,
    [filteredItems, effectiveSelectedId]
  );

  const handleFilterChange = (nextFilter) => {
    setActiveFilter(nextFilter);
    const nextItems = nextFilter === "all" ? items : items.filter((it) => it.type === nextFilter);
    setSelectedId(nextItems[0]?.id ?? null);
  };

  if (!items.length) {
    return (
      <section className="profile-activity">
        <p className="profile-activity__muted">Tính năng đang phát triển</p>
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
            0
          </span>
        </div>

        <UpcomingActivityCard onSearchVenues={() => console.log("search venues")} />

        <h3 className="profile-activity__section-title">Đã qua</h3>
        <PastActivityList
          items={filteredItems}
          selectedId={effectiveSelectedId}
          onSelect={setSelectedId}
        />
      </div>

      <ActivityDetailPanel item={selectedItem} />
    </section>
  );
};

export default ActivityView;

