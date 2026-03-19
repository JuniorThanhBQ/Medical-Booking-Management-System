import { useProfileStore } from '../hooks/use-profile-store';
import ProfileSidebar from '../components/ProfileSidebar';
import ActivityView from '../components/activity/ActivityView';
import Navbar from '../components/Navbar';
import { getRoleMenuItems } from '@/utils/utils';
import { DEFAULT_NAV_LINKS } from '@/configs/const';
import { TABS } from './ProfilePage';
import { getActivityConfig } from '../utils/activity-config';
import '@/assets/css/users/profile.css';

const ActivityPage = () => {
  const { user } = useProfileStore();
  const { filters, items } = getActivityConfig(user?.role);

  return (
    <>
      <Navbar menuItems={getRoleMenuItems()} navLinks={DEFAULT_NAV_LINKS} />

      <div className="profile-layout">
        <ProfileSidebar userName={user?.name || "User"} activeKey={TABS.ACTIVITY} />

        <main className="profile-main">
          <h1 className="profile-main__title">Hoạt động</h1>
          <ActivityView filters={filters} items={items} />
        </main>
      </div>
    </>
  );
};

export default ActivityPage;
