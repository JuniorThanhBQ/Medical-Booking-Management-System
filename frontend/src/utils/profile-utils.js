export function splitName(fullName = "") {
  const parts = fullName.trim().split(/\s+/);
  return {
    firstName: parts[0] || "",
    lastName: parts.slice(1).join(" ") || "",
  };
}

export function splitBirthday(birthdayStr = "") {
  if (!birthdayStr) return { day: "", month: "", year: "" };
  const [year, month, day] = birthdayStr.split("-");
  return {
    day: parseInt(day, 10) || "",
    month: parseInt(month, 10) || "",
    year: parseInt(year, 10) || "",
  };
}

export function formatBirthday(year, month, day) {
  if (!year || !month || !day) return "";
  return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

export function formatProfileUpdate(formData) {
  return {
    name: `${formData.firstName} ${formData.lastName}`.trim(),
    phone: formData.phone,
    email: formData.email,
    dateOfBirth: formatBirthday(
      formData.birthYear,
      formData.birthMonth,
      formData.birthDay,
    ),
    gender: formData.gender,
  };
}

export const MONTH_OPTIONS = Array.from({ length: 12 }, (_, i) => ({
  value: i + 1,
  label: new Date(0, i).toLocaleString("vi-VN", { month: "long" }),
}));

const MAX_AVATAR_SIZE = 2 * 1024 * 1024;
const ALLOWED_AVATAR_TYPES = ["image/jpeg", "image/png", "image/webp"];

export function readAvatarFile(event, callback) {
  const file = event.target.files[0];
  event.target.value = "";
  if (!file) return;
  if (!ALLOWED_AVATAR_TYPES.includes(file.type)) {
    alert("Chỉ chấp nhận ảnh JPEG, PNG, hoặc WebP");
    return;
  }
  if (file.size > MAX_AVATAR_SIZE) {
    alert("Ảnh không được vượt quá 2MB");
    return;
  }
  const reader = new FileReader();
  reader.onload = () => callback(reader.result);
  reader.onerror = () => console.error("Không thể đọc tệp ảnh");
  reader.readAsDataURL(file);
}

export function normalizeActivity(item, doctorMap = {}) {
  if (item.type === "medical_records") {
    return {
      ...item,
      title: item.diagnosis || "Hồ sơ bệnh án",
      meta: [item.doctorName, item.specialty].filter(Boolean).join(" · "),
    };
  }
  if (item.type === "appointments") {
    const doctor = doctorMap[item.doctorId];
    return {
      ...item,
      title: doctor?.name || "Lịch hẹn",
      meta: [item.date, item.startTime].filter(Boolean).join(" "),
    };
  }
  return { ...item, title: item.title ?? "", meta: item.meta ?? "" };
}

export function getActivityStatusLabel(status) {
  switch (status) {
    case "cancelled":
      return "Đã hủy";
    case "completed":
      return "Hoàn thành";
    case "active":
      return "Đang hoạt động";
    default:
      return status || "Trạng thái";
  }
}

export function getStatusClassName(status) {
  switch (status) {
    case "cancelled":
      return "profile-activity__pill--cancelled";
    case "completed":
      return "profile-activity__pill--completed";
    case "active":
    case "confirmed":
      return "profile-activity__pill--active";
    case "pending":
      return "profile-activity__pill--pending";
    case "in_progress":
      return "profile-activity__pill--in-progress";
    default:
      return "";
  }
}
