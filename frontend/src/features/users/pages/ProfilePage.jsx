import { useState } from 'react';
import { useProfileStore } from '../hooks/use-profile-store';
import ProfileSidebar from '../components/ProfileSidebar';
import ProfileCard from '../components/ProfileCard';
import EditProfileForm from '../components/EditProfileForm';
import ActivityView from '../components/activity/ActivityView';
import Navbar from '../components/Navbar';
import { getRoleMenuItems } from '@/utils/utils';
import { DEFAULT_NAV_LINKS } from '@/configs/const';
import '@/assets/css/users/profile.css';

const ProfilePage = () => {
  const { user } = useProfileStore();
  const [activeTab, setActiveTab] = useState("profile");

  const handleSave = (updatedData) => {
    // updateProfile(updatedData);
    console.log('Profile updated locally:', updatedData);
    // zustand update profile here
  };

  return (
    <>
      <Navbar menuItems={getRoleMenuItems()} navLinks={DEFAULT_NAV_LINKS} />
      
      <div className="profile-layout">
        <ProfileSidebar userName={user?.name || "User"} activeKey={activeTab} onSelect={setActiveTab} />
        
        <main className="profile-main">
          <h1 className="profile-main__title">{activeTab === "activity" ? "Hoạt động" : "Hồ sơ"}</h1>

          {activeTab === "activity" ? (
            <ActivityView />
          ) : (
            <div className="profile-content">
              <ProfileCard profile={user} />
              <EditProfileForm profile={user} onSave={handleSave} />
            </div>
          )}
        </main>
      </div>
    </>
  );
};

export default ProfilePage;
