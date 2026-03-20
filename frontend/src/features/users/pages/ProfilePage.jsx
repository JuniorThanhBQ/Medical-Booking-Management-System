import { useProfileStore } from '../hooks/use-profile-store';
import ProfileSidebar from '../components/ProfileSidebar';
import ProfileCard from '../components/ProfileCard';
import EditProfileForm from '../components/EditProfileForm';
import Navbar from '../components/Navbar';
import '@/assets/css/users/profile.css';

export const TABS = { PROFILE: 'profile', ACTIVITY: 'activity' };

const ProfilePage = () => {
  const { user } = useProfileStore();

  const handleSave = (updatedData) => {
    // updateProfile(updatedData);
    console.log('Profile updated locally:', updatedData);
    // zustand update profile here
  };

  return (
    <>
      <Navbar />

      <div className="profile-layout">
        <ProfileSidebar userName={user?.name || "User"} activeKey={TABS.PROFILE} />

        <main className="profile-main">
          <h1 className="profile-main__title">Hồ sơ</h1>

          <div className="profile-content">
            <ProfileCard profile={user} />
            <EditProfileForm profile={user} onSave={handleSave} />
          </div>
        </main>
      </div>
    </>
  );
};

export default ProfilePage;
