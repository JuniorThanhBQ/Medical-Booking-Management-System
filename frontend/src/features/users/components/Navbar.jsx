import { useNavbarMenu } from "../hooks/use-navbar-menu";
import { BellIcon } from "@/assets/icons";
import "@/assets/css/users/navbar.css";
import { DEFAULT_MENU_ITEMS, DEFAULT_NAV_LINKS } from "@/configs/const";
import { handleLogout } from "../../auth/api/authService";
import { getRoleNavLinks } from "@/utils/utils";

export default function Navbar({
  navLinks = DEFAULT_NAV_LINKS,
  menuItems = DEFAULT_MENU_ITEMS,
}) {
  const { scrolled, menuOpen, menuRef, toggleMenu, closeMenu } =
    useNavbarMenu();

  const isLoggedIn = Boolean(localStorage.getItem("token"));

  const resolvedNavLinks = getRoleNavLinks();
  const resolvedMenuItems = isLoggedIn
    ? [
        { label: "Hồ sơ", href: "/profile" },
        { type: "divider" },
        {
          label: "Đăng xuất",
          isLogout: true,
          danger: true,
          onClick: handleLogout,
        },
      ]
    : menuItems;

  return (
    <div className={`navbar-wrap${scrolled ? " navbar-wrap--scrolled" : ""}`}>
      <header className="navbar-pill">
        <nav className="navbar__nav">
          {resolvedNavLinks.map(({ label, href, onClick }) => (
            <a
              key={href ?? label}
              href={href}
              className="navbar__link"
              onClick={onClick}
            >
              {label}
            </a>
          ))}
        </nav>

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
