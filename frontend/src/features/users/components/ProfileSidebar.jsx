import { PROFILE_MENU_ITEMS } from '@/configs/const';

const ProfileSidebar = ({ userName }) => {

  return (
    <aside className="profile-sidebar">
      <h2 className="profile-sidebar__user-name">{userName}</h2>
      <nav className="profile-sidebar__nav">
        {PROFILE_MENU_ITEMS.map((item) => (
          <button
            key={item.label}
            className={`profile-sidebar__item ${item.active ? 'profile-sidebar__item--active' : ''}`}
          >
            <svg
              className="profile-sidebar__icon"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d={item.icon}
              />
            </svg>
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
};

export default ProfileSidebar;
