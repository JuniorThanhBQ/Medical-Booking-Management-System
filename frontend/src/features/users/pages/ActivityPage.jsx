import { useEffect, useState } from 'react';
import { useProfileStore } from '../hooks/use-profile-store';
import ProfileSidebar from '../components/ProfileSidebar';
import ActivityView from '../components/activity/ActivityView';
import Navbar from '../components/Navbar';
import { TABS } from './ProfilePage';
import { getActivityConfig } from '@utils/activity-config.js';
import { getUserToken } from '@/utils/auth-helpers';
import { getProfileSidebarItems } from '@configs/const';
import '@/assets/css/users/profile.css';

const ActivityPage = () => {
  const { user } = useProfileStore();
  const [activityData, setActivityData] = useState({ filters: [], items: [], upcomingItems: [], });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;

    const loadActivity = async () => {
      const token = getUserToken();
      if (!token) {
        if (mounted) {
          setActivityData({ filters: [], items: [], upcomingItems: [] });
          setError('');
          setLoading(false);
        }
        return;
      }

      setLoading(true);
      try {
        const config = await getActivityConfig(user?.role, token);
        if (!mounted) return;
        setActivityData(config);
        setError('');
      } catch {
        if (!mounted) return;
        setActivityData({ filters: [], items: [], upcomingItems: [] });
        setError('Không thể tải dữ liệu hoạt động');
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
  }, [user?.role]);

  const displayName = [user?.firstName, user?.lastName].filter(Boolean).join(' ').trim() || user?.name || 'User';

  return (
    <>
      <Navbar />
      <div className="profile-layout">
        <ProfileSidebar userName={displayName} activeKey={TABS.ACTIVITY} items={getProfileSidebarItems(user?.role)} />

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
