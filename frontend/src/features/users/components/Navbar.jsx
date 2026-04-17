import "@css/shared/navbar.css";

import { useEffect, useState } from "react";

import { DEFAULT_MENU_ITEMS } from "@/configs/const";
import useAuth from "@/contexts/auth/AuthContext";
import NotificationBell from "@/features/notifications/components/NotificationBell";
import { getRoleMenuItems, getRoleNavLinks } from "@/utils/Utils.js";

import { useNavbarMenu } from "../hooks/useNavbarMenu";

export default function Navbar() {
  const { scrolled, menuOpen, menuRef, toggleMenu, closeMenu } =
    useNavbarMenu();

  const { accessToken, user, logout } = useAuth();
  const [shouldRedirect, setShouldRedirect] = useState(false);

  useEffect(() => {
    if (shouldRedirect) {
      window.location.href = "/";
    }
  }, [shouldRedirect]);

  const isLoggedIn = Boolean(accessToken);
  const allNavLinks = getRoleNavLinks(user?.role);
  const homeLink = allNavLinks[0];
  const menuItems = isLoggedIn ? getRoleMenuItems(user?.role) : [];
  const divider = menuItems.length > 0 ? [{ type: "divider" }] : [];
  const actionItems = isLoggedIn
    ? [
        {
          label: "Đăng xuất",
          isLogout: true,
          danger: true,
          onClick: async () => {
            await logout();
            setShouldRedirect(true);
          },
        },
      ]
    : DEFAULT_MENU_ITEMS;
  const resolvedMenuItems = [...menuItems, ...divider, ...actionItems];

  return (
    <div className={`navbar-wrap${scrolled ? " navbar-wrap--scrolled" : ""}`}>
      <header className="navbar-pill">
        {homeLink && (
          <nav className="navbar__nav">
            <a href={homeLink.href} className="navbar__link">
              {homeLink.label}
            </a>
          </nav>
        )}
        <div className="navbar__actions">
          {isLoggedIn && <NotificationBell />}

          <div className="navbar__menu-wrapper" ref={menuRef}>
            <button
              type="button"
              className="navbar__menu-trigger"
              onClick={toggleMenu}
            >
              Menu
            </button>

            {menuOpen && (
              <div className="navbar__menu">
                {resolvedMenuItems.map((item, index) => {
                  if (item.type === "divider") {
                    return (
                      <div
                        key={`divider-${index}`}
                        className="navbar__menu-divider"
                      />
                    );
                  }

                  if (item.onClick) {
                    return (
                      <button
                        key={item.label}
                        type="button"
                        className={`navbar__menu-item${
                          item.danger ? " navbar__menu-item--danger" : ""
                        }`}
                        onClick={() => {
                          closeMenu();
                          item.onClick();
                        }}
                      >
                        {item.label}
                      </button>
                    );
                  }

                  return (
                    <a
                      key={item.label}
                      href={item.href}
                      className={`navbar__menu-item${
                        item.danger ? " navbar__menu-item--danger" : ""
                      }`}
                      onClick={closeMenu}
                    >
                      {item.label}
                    </a>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </header>
    </div>
  );
}
