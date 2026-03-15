export const ROLE = {
  Patient: "Patient",
  Doctor: "Doctor",
  Admin: "Admin",
  Receptionist: "Receptionist",
};

export const DEFAULT_NAV_LINKS = [{ label: "Trang chủ", href: "#home" }];

export const DEFAULT_AUTH_MENU_ITEMS = {
  Patient: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Lịch sử khám", href: "/history" },
    { label: "Trợ giúp và hỗ trợ", href: "#support" },
  ],
  Doctor: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Trợ giúp và hỗ trợ", href: "#support" },
  ],
  Admin: [{ label: "Trợ giúp và hỗ trợ", href: "#support" }],
  Receptionist: [{ label: "Trợ giúp và hỗ trợ", href: "#support" }],
};
export const DEFAULT_MENU_ITEMS = [
  { label: "Đăng nhập & Đăng ký", href: "/auth" },
  { label: "Trợ giúp và hỗ trợ", href: "#support" },
];

export const OPEN_HOURS = {
  start: 9,
  end: 16,
};

export const AVAILABLE_BOOKING_DAYS = 15;
