import { useNavbarMenu } from "../../users/hooks/use-navbar-menu.js";
import { BellIcon } from "@/assets/icons";
import "@/assets/css/users/navbar.css";
import { DEFAULT_MENU_ITEMS } from "@/configs/const";
import { handleLogout } from "../../auth/services/authService.jsx";
import { getRoleNavLinks, getRoleMenuItems } from "@/utils/utils";
import { isAuthenticated } from "@/utils/auth-helpers";

export default function Navbar() {
  const { scrolled, menuOpen, menuRef, toggleMenu, closeMenu } =
    useNavbarMenu();

  const isLoggedIn = isAuthenticated();

  const allNavLinks = getRoleNavLinks();
  const homeLink = allNavLinks[0];
  const menuItems = isLoggedIn ? getRoleMenuItems() : [];
  const divider = menuItems.length > 0 ? [{ type: "divider" }] : [];
  const actionItems = isLoggedIn
    ? [{ label: "Đăng xuất", isLogout: true, danger: true, onClick: handleLogout }]
    : DEFAULT_MENU_ITEMS;
  const resolvedMenuItems = [...menuItems, ...divider, ...actionItems];

  return (
    <div className={`navbar-wrap${scrolled ? " navbar-wrap--scrolled" : ""}`}>
      <header className="navbar-pill">
        {homeLink && (
          <nav className="navbar__nav">
            <a href={homeLink.href} className="navbar__link">{homeLink.label}</a>
          </nav>
        )}
        <div className="navbar__actions">
          {isLoggedIn && (
            <button
              type="button"
              className="navbar__icon-button"
              aria-label="Thông báo"
            >
              <BellIcon className="navbar__icon" aria-hidden="true" />
            </button>
          )}

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
                        className={`navbar__menu-item${item.danger ? " navbar__menu-item--danger" : ""
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
                      className={`navbar__menu-item${item.danger ? " navbar__menu-item--danger" : ""
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
