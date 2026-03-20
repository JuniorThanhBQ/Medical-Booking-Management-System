import { UserProfileIcon, ActivityIcon } from '@/assets/icons';

export const ROLE = {
  Patient: "Patient",
  Doctor: "Doctor",
  Admin: "Admin",
  Receptionist: "Receptionist",
};

export const DEFAULT_NAV_LINKS = [{ label: "Trang chủ", href: "#home" }];

export const DEFAULT_AUTH_NAV_LINKS = {
  Patient: [{ label: "Trang chủ", href: "/dashboard" }],
  Doctor: [{ label: "Trang chủ", href: "/doctor/today" }],
  Admin: [{ label: "Trang chủ", href: "/dashboard" }],
  Receptionist: [{ label: "Trang chủ", href: "/dashboard" }],
};

export const DEFAULT_AUTH_MENU_ITEMS = {
  Patient: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Hoạt động", href: "/activity" },
  ],
  Doctor: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Hoạt động", href: "/activity" },
    { label: "Lịch làm việc", href: "/schedule" },
  ],
  Admin: [
    { label: "Quản lý bác sĩ", href: "/doctors" },
    { label: "Quản lý lịch hẹn", href: "/appointments" },
    { label: "Quản lý bệnh nhân", href: "/patients" },
    { label: "Trợ giúp và hỗ trợ", href: "#support" },
  ],
  Receptionist: [
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

export const AVAILABLE_BOOKING_DAYS = 15;

export const APPOINTMENT_STATUS = {
  PENDING: "pending",
  CONFIRMED: "confirmed",
  IN_PROGRESS: "in_progress",
  COMPLETED: "completed",
  CANCELLED: "cancelled",
};

export const STATUS_LABELS = {
  pending: "Chờ xác nhận",
  confirmed: "Đã xác nhận",
  in_progress: "Đang khám",
  completed: "Hoàn thành",
  cancelled: "Đã hủy",
};

export const REASON_OPTIONS = [
  { value: "sick", label: "Ốm / bệnh" },
  { value: "personal", label: "Cá nhân" },
  { value: "conference", label: "Hội nghị / đào tạo" },
];

export const TYPE_OPTIONS = [
  { value: "time_off", label: "Nghỉ phép" },
  { value: "shift_change", label: "Đổi ca / thay đổi lịch" },
];

export function getStatusLabel(status) {
  return STATUS_LABELS[status] || status;
}

export const DAY_LABELS = {
  Mon: "Thứ 2",
  Tue: "Thứ 3",
  Wed: "Thứ 4",
  Thu: "Thứ 5",
  Fri: "Thứ 6",
  Sat: "Thứ 7",
  Sun: "Chủ nhật",
};

export const INITIAL_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

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


export const SUPPORTED_COUNTRIES = [
  { code: "VN", label: "Việt Nam", phoneCode: "+84" },
];

export const GENDER_OPTIONS = [
  { value: "MALE", label: "Nam" },
  { value: "FEMALE", label: "Nữ" },
  { value: "OTHER", label: "Khác" },
];

export const EXAM_STATUS = {
  DRAFT: "draft",
  COMPLETED: "completed",
};
