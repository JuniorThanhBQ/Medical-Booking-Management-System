
const ProfileCard = ({ profile }) => {
  console.log("profile card",profile);
  const getInitials = (name) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase();
  };

  const infoItems = [
    { label: 'First name', value: profile.name.split(' ')[0] },
    { label: 'Last name', value: profile.name.split(' ').slice(1).join(' ') },
    { label: 'Mobile number', value: profile.phone },
    { label: 'Email', value: profile.email },
    { label: 'Date of birth', value: profile.birthday || '-' },
    { label: 'Gender', value: profile.gender || '-' },
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
        <button className="profile-card__avatar-edit" aria-label="Edit avatar">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
        </button>
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
