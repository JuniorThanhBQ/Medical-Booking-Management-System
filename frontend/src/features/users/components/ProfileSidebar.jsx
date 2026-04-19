import { useNavigate } from "react-router-dom";

import { PROFILE_SIDEBAR_ITEMS } from "@/configs/const";

const ProfileSidebar = ({
  userName,
  activeKey = "profile",
  onSelect,
  items,
}) => {
  const navigate = useNavigate();
  const sidebarItems = items || PROFILE_SIDEBAR_ITEMS;

  return (
    <aside className="profile-sidebar">
      <h2 className="profile-sidebar__user-name">{userName}</h2>
      <nav className="profile-sidebar__nav">
        {sidebarItems.map((item) => (
          <button
            key={item.label}
            type="button"
            className={`profile-sidebar__item ${item.key === activeKey ? "profile-sidebar__item--active" : ""}`}
            onClick={() =>
              item.path ? navigate(item.path) : onSelect?.(item.key)
            }
          >
            <item.Icon className="profile-sidebar__icon" />
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
};

export default ProfileSidebar;
