import "@css/users/profile.css";

import { TABS } from "@configs/const";
import { useEffect } from "react";

import useAuth from "@/contexts/auth/AuthContext";

import EditProfileForm from "../components/EditProfileForm";
import Navbar from "../components/Navbar";
import ProfileCard from "../components/ProfileCard";
import ProfileSidebar from "../components/ProfileSidebar";
import { useProfileStore } from "../hooks/use-profile-store";

const ProfilePage = () => {
  const { user: contextUser, api } = useAuth();
  const {
    updateProfile,
    getProfile,
    user: profileUser,
    loading,
  } = useProfileStore();

  const handleSave = async (updatedData) => {
    if (!api) return;

    await updateProfile(api, updatedData);
  };

  const handleAvatarChange = async (avatarUrl) => {
    if (!api) return;

    await updateProfile(api, { avatar: avatarUrl });
  };

  useEffect(() => {
    if (api && !profileUser) {
      getProfile(api);
    }
  }, [api, profileUser, getProfile]);

  const userData = profileUser || contextUser;

  const profileData = {
    ...userData,
    name:
      [userData?.firstName, userData?.lastName]
        .filter(Boolean)
        .join(" ")
        .trim() ||
      userData?.name ||
      "User",
    dateOfBirth: userData?.dayOfBirth || userData?.dateOfBirth || "",
    phone: userData?.phone || "",
    email: userData?.email || "",
    gender: userData?.gender || "",
    avatar: userData?.avatar || "",
  };

  return (
    <>
      <Navbar />

      <div className="profile-layout">
        <ProfileSidebar userName={profileData.name} activeKey={TABS.PROFILE} />

        <main className="profile-main">
          <h1 className="profile-main__title">Hồ sơ</h1>

          <div className="profile-content">
            <ProfileCard
              profile={profileData}
              onAvatarChange={handleAvatarChange}
              loading={loading}
            />
            <EditProfileForm profile={profileData} onSave={handleSave} />
          </div>
        </main>
      </div>
    </>
  );
};

export default ProfilePage;
