import { useNavbarMenu } from "../hooks/use-navbar-menu";
import "@/assets/css/users/navbar.css";
import { ROLE, DEFAULT_MENU_ITEMS, DEFAULT_NAV_LINKS } from "@/configs/const";
import { handleLogout } from "../../auth/api/authService";

const PATIENT_NAV_LINKS = [
  { label: "Trang chủ", href: "/" },
  { label: "Tìm bác sĩ", href: "/dashboard" },
  { label: "Lịch hẹn của tôi", href: "/appointments" },
  { label: "Hồ sơ bệnh án", href: "/medical-records" },
];

export default function Navbar({
  navLinks = DEFAULT_NAV_LINKS,
  menuItems = DEFAULT_MENU_ITEMS,
}) {
  const { scrolled, menuOpen, menuRef, toggleMenu, closeMenu } =
    useNavbarMenu();

  const isLoggedIn = Boolean(localStorage.getItem("token"));
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const role = user?.role;

  const resolvedNavLinks =
    isLoggedIn && role === ROLE.Patient ? PATIENT_NAV_LINKS : navLinks;

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
              <svg
                className="navbar__icon"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M12 2a5 5 0 0 0-5 5v2.382l-.894 4.47A1 1 0 0 0 7.09 15h9.82a1 1 0 0 0 .984-1.148L17 9.382V7a5 5 0 0 0-5-5Zm0 20a3 3 0 0 0 2.995-2.824L15 19h-6a3 3 0 0 0 2.824 2.995L12 22Z"
                  fill="currentColor"
                />
              </svg>
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
