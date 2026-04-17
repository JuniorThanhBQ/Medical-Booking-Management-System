import "@css/users/profile.css";

import { getProfileSidebarItems } from "@configs/const";
import { TABS } from "@configs/const";
import { getActivityConfig } from "@utils/activity-config.js";
import { useEffect, useState } from "react";

import useAuth from "@/contexts/auth/AuthContext";

import ActivityView from "../components/activity/ActivityView";
import Navbar from "../components/Navbar";
import ProfileSidebar from "../components/ProfileSidebar";

const ActivityPage = () => {
  const { api, user: contextUser } = useAuth();
  const [activityData, setActivityData] = useState({
    filters: [],
    items: [],
    upcomingItems: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const loadActivity = async () => {
      if (!api) {
        if (mounted) {
          setActivityData({ filters: [], items: [], upcomingItems: [] });
          setError("");
          setLoading(false);
        }
        return;
      }

      setLoading(true);
      try {
        const config = await getActivityConfig(contextUser?.role, api);
        if (!mounted) return;
        setActivityData(config);
        setError("");
      } catch {
        if (!mounted) return;
        setActivityData({ filters: [], items: [], upcomingItems: [] });
        setError("Không thể tải dữ liệu hoạt động");
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadActivity();

    return () => {
      mounted = false;
    };
  }, [contextUser?.role, api]);

  const displayName =
    [contextUser?.firstName, contextUser?.lastName]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    contextUser?.name ||
    "User";

  return (
    <>
      <Navbar />
      <div className="profile-layout">
        <ProfileSidebar
          userName={displayName}
          activeKey={TABS.ACTIVITY}
          items={getProfileSidebarItems(contextUser?.role)}
        />

        <main className="profile-main">
          <h1 className="profile-main__title">Hoạt động</h1>
          <ActivityView
            filters={activityData.filters}
            items={activityData.items}
            upcomingItems={activityData.upcomingItems}
            loading={loading}
            error={error}
          />
        </main>
      </div>
    </>
  );
};

export default ActivityPage;
