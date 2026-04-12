import { UserProfileIcon, ActivityIcon } from '@/assets/icons';

export const ROLE = {
  Patient: "PATIENT",
  Doctor: "DOCTOR",
  Admin: "ADMIN",
  Receptionist: "RECEPTIONIST",
};

export const DEFAULT_NAV_LINKS = [{ label: "Trang chủ", href: "#home" }];

export const DEFAULT_AUTH_NAV_LINKS = {
  PATIENT: [{ label: "Trang chủ", href: "/dashboard" }],
  DOCTOR: [{ label: "Trang chủ", href: "/doctor/today" }],
  ADMIN: [{ label: "Trang chủ", href: "/dashboard" }],
  RECEPTIONIST: [{ label: "Trang chủ", href: "/dashboard" }],
};

export const DEFAULT_AUTH_MENU_ITEMS = {
  PATIENT: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Hoạt động", href: "/activity" },
  ],
  DOCTOR: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Hoạt động", href: "/doctor/activity" },
    { label: "Lịch làm việc", href: "/schedule" },
  ],
  ADMIN: [
    { label: "Quản lý bác sĩ", href: "/doctors" },
    { label: "Quản lý lịch hẹn", href: "/appointments" },
    { label: "Quản lý bệnh nhân", href: "/patients" },
    { label: "Trợ giúp và hỗ trợ", href: "#support" },
  ],
  RECEPTIONIST: [
    { label: "Quản lý lịch hẹn", href: "/appointments" },
    { label: "Quản lý bệnh nhân", href: "/patients" },
    { label: "Trợ giúp và hỗ trợ", href: "#support" },
  ],
};
export const DEFAULT_MENU_ITEMS = [
  { label: "Đăng nhập & Đăng ký", href: "/auth" },
  { label: "Trợ giúp và hỗ trợ", href: "#support" },
];

export const OPEN_HOURS = {
  start: 9,
  end: 16,
};

export const AVAILABLE_BOOKING_DAYS = 7;

export const APPOINTMENT_STATUS = {
  PENDING: "PENDING",
  APPROVED: "APPROVED",
  IN_PROGRESS: "in_progress", // not in back end yet
  COMPLETED: "COMPLETED",
  CANCEL: "CANCEL",
  CONFIRMED: "APPROVED",
  CANCELLED: "CANCEL",
};

export const STATUS_LABELS = {
  PENDING: "Chờ xác nhận",
  APPROVED: "Đã xác nhận",
  in_progress: "Đang khám",
  COMPLETED: "Hoàn thành",
  CANCEL: "Đã hủy",
};

export function getStatusLabel(status) {
  return STATUS_LABELS[status] || status;
}

export const DAY_LABELS = {
  MONDAY: "Thứ 2",
  TUESDAY: "Thứ 3",
  WEDNESDAY: "Thứ 4",
  THURSDAY: "Thứ 5",
  FRIDAY: "Thứ 6",
  SATURDAY: "Thứ 7",
  SUNDAY: "Chủ nhật",
};

export const INITIAL_DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"];

export const PROFILE_SIDEBAR_ITEMS = [
  {
    key: "profile",
    path: "/profile",
    label: "Hồ sơ",
    Icon: UserProfileIcon,
  },
  {
    key: "activity",
    path: "/activity",
    label: "Hoạt động",
    Icon: ActivityIcon,
  },
];

export function getProfileSidebarItems(role) {
  if (role === ROLE.Doctor) {
    return PROFILE_SIDEBAR_ITEMS.map((item) =>
      item.key === "activity" ? { ...item, path: "/doctor/activity" } : item
    );
  }
  return PROFILE_SIDEBAR_ITEMS;
}


export const SUPPORTED_COUNTRIES = [
  { code: "VN", label: "Việt Nam", phoneCode: "+84" },
];

export const GENDER_OPTIONS = [
  { value: "MALE", label: "Nam" },
  { value: "FEMALE", label: "Nữ" },
  { value: "OTHER", label: "Khác" },
];

export const CTA_DISPLAY_MAP = {
  CK1: "Đặt lịch khám",
  CK2: "Đặt lịch khám",
  CK3: "Đặt lịch khám",
};

export const EXAM_STATUS = {
  DRAFT: "draft",
  COMPLETED: "completed",
};
