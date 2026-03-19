import { useMemo, useState } from "react";
import ActivityFilters from "./ActivityFilters";
import UpcomingActivityCard from "./UpcomingActivityCard";
import PastActivityList from "./PastActivityList";
import ActivityDetailPanel from "./ActivityDetailPanel";
import { medicalRecords, appointments } from "@/data/mocks/users";
import { DOCTORS } from "@/data/mocks/doctors";
import { normalizeActivity } from "@/features/users/utils/profile-utils";

const FILTERS = [
  { key: "all", label: "Tất cả" },
  { key: "appointments", label: "Lịch hẹn" },
  { key: "medical_records", label: "Hồ sơ bệnh án" },
];

const doctorMap = Object.fromEntries(DOCTORS.map((d) => [d.id, d]));
const MOCK_ITEMS = [...medicalRecords, ...appointments].map((it) =>
  normalizeActivity(it, doctorMap)
);

const ActivityView = () => {
  const [activeFilter, setActiveFilter] = useState("all");
  const [selectedId, setSelectedId] = useState(MOCK_ITEMS[0]?.id ?? null);

  const filteredItems = useMemo(() => {
    if (activeFilter === "all") return MOCK_ITEMS;
    return MOCK_ITEMS.filter((it) => it.type === activeFilter);
  }, [activeFilter]);

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
    const nextItems = nextFilter === "all" ? MOCK_ITEMS : MOCK_ITEMS.filter((it) => it.type === nextFilter);
    setSelectedId(nextItems[0]?.id ?? null);
  };

  return (
    <section className="profile-activity">
      <div className="profile-activity__left">
        <ActivityFilters
          filters={FILTERS}
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

