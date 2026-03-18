export const ROLE = {
  Patient: "Patient",
  Doctor: "Doctor",
  Admin: "Admin",
  Receptionist: "Receptionist",
};

export const DEFAULT_NAV_LINKS = [{ label: "Trang chủ", href: "#home" }];

export const DEFAULT_AUTH_NAV_LINKS = {
  Patient: [
    { label: "Trang chủ", href: "/dashboard" },
    { label: "Lịch hẹn của tôi", href: "/appointments" },
    { label: "Hồ sơ bệnh án", href: "/medical-records" },
  ],
  Doctor: [
    { label: "Trang chủ", href: "/doctor/today" },
    { label: "Lịch làm việc", href: "/schedule" },
    { label: "Hồ sơ bệnh án", href: "/medical-records" },
  ],
  Admin: [
    { label: "Trang chủ", href: "/dashboard" },
    { label: "Quản lý bác sĩ", href: "/doctors" },
    { label: "Quản lý lịch hẹn", href: "/appointments" },
    { label: "Quản lý bệnh nhân", href: "/patients" },
  ],
  Receptionist: [
    { label: "Trang chủ", href: "/dashboard" },
    { label: "Quản lý lịch hẹn", href: "/appointments" },
    { label: "Quản lý bệnh nhân", href: "/patients" },
  ],
};

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

export const APPOINTMENT_STATUS = {
  SCHEDULED: "scheduled",
  IN_PROGRESS: "in_progress",
  COMPLETED: "completed",
  CANCELLED: "cancelled",
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
  switch (status) {
    case APPOINTMENT_STATUS.SCHEDULED:
      return "Sắp khám";
    case APPOINTMENT_STATUS.IN_PROGRESS:
      return "Đang khám";
    case APPOINTMENT_STATUS.COMPLETED:
      return "Đã khám";
    case APPOINTMENT_STATUS.CANCELLED:
      return "Đã hủy";
    default:
      return status;
  }
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

export const PROFILE_MENU_ITEMS = [
    { label: 'Profile', icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z', active: true },
    { label: 'Settings', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' },
  ];

export const SUPPORTED_COUNTRIES = [
  { code: "VN", label: "Vietnam", phoneCode: "+84" },
];

export const GENDER_OPTIONS = [
  { value: "MALE", label: "Nam" },
  { value: "FEMALE", label: "Nữ" },
  { value: "OTHER", label: "Khác" },
];