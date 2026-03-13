import { useNavbarMenu } from '../hooks/use-navbar-menu'
import './navbar.css'

export default function Navbar() {
  const { scrolled, menuOpen, menuRef, toggleMenu } = useNavbarMenu()

  return (
    <div className={`navbar-wrap${scrolled ? ' navbar-wrap--scrolled' : ''}`}>
      <header className="navbar-pill">
        <nav className="navbar__nav">
          <a href="#home" className="navbar__link">Trang chủ</a>
        </nav>

        <div className="navbar__actions">
          <div className="navbar__menu-wrapper" ref={menuRef}>
            <button type="button" className="navbar__menu-trigger" onClick={toggleMenu}>
              Menu
            </button>

            {menuOpen && (
              <div className="navbar__menu">
                <a href="/signin" className="navbar__menu-item">Đăng nhập</a>
                <a href="#settings" className="navbar__menu-item">Đăng ký</a>
                <div className="navbar__menu-divider" />
                <a href="#support" className="navbar__menu-item">Trợ giúp và hỗ trợ</a>
              </div>
            )}
          </div>
        </div>
      </header>
    </div>
  )
}
