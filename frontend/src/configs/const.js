import { ActivityIcon, BellIcon, UserProfileIcon } from "@/assets/icons";

export const FIELDS = [
  { label: "Họ", key: "firstName", type: "text" },
  { label: "Tên", key: "lastName", type: "text" },
  { label: "Số điện thoại", key: "phone", type: "tel" },
  { label: "Ngày sinh", key: "dateOfBirth", type: "date" },
];

export const GENDER_OPTIONS = [
  { value: "male", label: "Nam" },
  { value: "female", label: "Nữ" },
  { value: "other", label: "Khác" },
];

export const OPTIONS = [
  {
    id: "patient",
    title: "Đăng nhập bệnh nhân",
    description: "Đặt lịch hẹn và theo dõi bệnh án",
  },
  {
    id: "doctor",
    title: "Đăng nhập bác sĩ",
    description: "Đăng ký và quản lý hồ sơ sức khoẻ bệnh nhân",
  },
  {
    id: "receptionist",
    title: "Đăng nhập lễ tân",
    description: "Quản lý lịch hẹn và hỗ trợ bệnh nhân",
  },
];

export const ROLE = {
  Patient: "PATIENT",
  Doctor: "DOCTOR",
  Admin: "ADMIN",
  Receptionist: "RECEPTIONIST",
};

export const TABS = { PROFILE: "profile", ACTIVITY: "activity" };

export const DEFAULT_NAV_LINKS = [{ label: "Trang chủ", href: "/" }];

export const DEFAULT_AUTH_NAV_LINKS = {
  PATIENT: [{ label: "Trang chủ", href: "/dashboard" }],
  DOCTOR: [{ label: "Trang chủ", href: "/doctor/today" }],
  ADMIN: [{ label: "Trang chủ", href: "/dashboard" }],
  RECEPTIONIST: [{ label: "Trang chủ", href: "/dashboard" }],
};

export const DEFAULT_MENU_ITEMS = [
  { label: "Đăng nhập & Đăng ký", href: "/auth" },
];

export const DEFAULT_AUTH_MENU_ITEMS = {
  PATIENT: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Hoạt động", href: "/activity" },
    { label: "Thông báo", href: "/notifications" },
  ],
  DOCTOR: [
    { label: "Hồ sơ", href: "/profile" },
    { label: "Hoạt động", href: "/activity" },
    { label: "Lịch làm việc", href: "/schedule" },
    { label: "Thông báo", href: "/notifications" },
  ],
  ADMIN: [
    { label: "Quản lý bác sĩ", href: "/doctors" },
    { label: "Quản lý lịch hẹn", href: "/receptionist/appointments" },
    { label: "Quản lý bệnh nhân", href: "/patients" },
    { label: "Thông báo", href: "/notifications" },
  ],
  RECEPTIONIST: [
    { label: "Quản lý lịch hẹn", href: "/receptionist/appointments" },
    { label: "Thông báo", href: "/notifications" },
  ],
};

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
  {
    key: "notifications",
    path: "/notifications",
    label: "Thông báo",
    Icon: BellIcon,
  },
];

export const APPOINTMENT_STATUS = {
  PENDING: "PENDING",
  APPROVED: "APPROVED",
  IN_PROGRESS: "in_progress",
  COMPLETED: "COMPLETED",
  CANCEL: "CANCEL",
  CONFIRMED: "APPROVED",
  CANCELLED: "CANCEL",
};

export const EXAM_STATUS = {
  DRAFT: "draft",
  COMPLETED: "completed",
};

const STATUS_LABELS = {
  PENDING: "Đang chờ",
  APPROVED: "Đã duyệt",
  IN_PROGRESS: "Đang tiến hành",
  COMPLETED: "Đã hoàn thành",
  CANCEL: "Đã hủy",
};

export const OPEN_HOURS = {
  start: 9,
  end: 16,
};

export const INITIAL_DAYS = [
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
  "SATURDAY",
  "SUNDAY",
];

export const DAY_LABELS = {
  MONDAY: "Thứ 2",
  TUESDAY: "Thứ 3",
  WEDNESDAY: "Thứ 4",
  THURSDAY: "Thứ 5",
  FRIDAY: "Thứ 6",
  SATURDAY: "Thứ 7",
  SUNDAY: "Chủ nhật",
};

export const SUPPORTED_COUNTRIES = [
  { code: "VN", label: "Việt Nam", phoneCode: "+84" },
];

export function getStatusLabel(status) {
  return STATUS_LABELS[status] || status;
}

export function getProfileSidebarItems(role) {
  return role === ROLE.Doctor
    ? PROFILE_SIDEBAR_ITEMS.map((item) =>
        item.key === "activity" ? { ...item, path: "/activity" } : item,
      )
    : PROFILE_SIDEBAR_ITEMS;
}
