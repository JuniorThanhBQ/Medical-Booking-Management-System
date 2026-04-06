import { useEffect } from 'react';
import { useProfileStore } from '../hooks/use-profile-store';
import ProfileSidebar from '../components/ProfileSidebar';
import ProfileCard from '../components/ProfileCard';
import EditProfileForm from '../components/EditProfileForm';
import Navbar from '../../medical_records/components/Navbar.jsx';
import { getUserToken } from '@/utils/auth-helpers';
import '@/assets/css/users/profile.css';

export const TABS = { PROFILE: 'profile', ACTIVITY: 'activity' };

const ProfilePage = () => {
  const { user, updateAvatar, getProfile, updateProfile } = useProfileStore();

  useEffect(() => {
    const token = getUserToken();
    if (!token) return;

    getProfile(token);
  }, [getProfile]);

  const handleSave = async (updatedData) => {
    const token = getUserToken();
    if (!token) return;

    await updateProfile(token, {
      ...updatedData,
      avatar: user?.avatar,
    });
  };

  const handleAvatarChange = (avatarUrl) => {
    updateAvatar(avatarUrl);
  };

  const profileData = {
    ...user,
    name: [user?.firstName, user?.lastName].filter(Boolean).join(' ').trim() || user?.name || 'User',
    dateOfBirth: user?.dayOfBirth || user?.dateOfBirth || '',
    phone: user?.phone || '',
    email: user?.email || '',
    gender: user?.gender || '',
    avatar: user?.avatar || '',
  };

  return (
    <>
      <Navbar />

      <div className="profile-layout">
        <ProfileSidebar userName={profileData.name} activeKey={TABS.PROFILE} />

        <main className="profile-main">
          <h1 className="profile-main__title">Hồ sơ</h1>

          <div className="profile-content">
            <ProfileCard profile={profileData} onAvatarChange={handleAvatarChange} />
            <EditProfileForm profile={profileData} onSave={handleSave} />
          </div>
        </main>
      </div>
    </>
  );
};

export default ProfilePage;
