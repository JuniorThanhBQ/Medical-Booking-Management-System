import { useRef } from "react";
import { EditPenIcon } from "@/assets/icons";
import { readAvatarFile } from "../utils/profile-utils.js";

const ProfileCard = ({ profile, onAvatarChange }) => {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    readAvatarFile(e, (base64) => onAvatarChange?.(base64));
  };

  const getInitials = (name) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase();
  };

  const infoItems = [
    { label: 'Họ', value: profile.name.split(' ')[0] },
    { label: 'Tên', value: profile.name.split(' ').slice(1).join(' ') },
    { label: 'Số điện thoại', value: profile.phone },
    { label: 'Email', value: profile.email },
    { label: 'Ngày sinh', value: profile.dateOfBirth || '-' },
    { label: 'Giới tính', value: profile.gender || '-' },
  ];

  return (
    <div className="profile-card">

      <div className="profile-card__avatar-container">
        <div className="profile-card__avatar">
          {profile.avatar ? (
            <img src={profile.avatar} alt={profile.name} className="profile-card__avatar" />
          ) : (
            getInitials(profile.name)
          )}
        </div>
        <button className="profile-card__avatar-edit" aria-label="Chỉnh sửa ảnh đại diện" onClick={() => fileInputRef.current?.click()}>
          <EditPenIcon size={16} className="w-4 h-4" />
        </button>
        <input ref={fileInputRef} type="file" accept="image/*" hidden onChange={handleFileChange} />
      </div>

      <h3 className="profile-card__name">{profile.name}</h3>

      <div className="profile-card__divider"></div>

      <div className="profile-card__info">
        {infoItems.map((item) => (
          <div key={item.label} className="profile-info-item">
            <div className="profile-info-item__label">{item.label}</div>
            <div className="profile-info-item__value">{item.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProfileCard;
