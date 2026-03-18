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
    birthday: formatBirthday(formData.birthYear, formData.birthMonth, formData.birthDay),
    gender: formData.gender,
  };
}

export const MONTH_OPTIONS = Array.from({ length: 12 }, (_, i) => ({
  value: i + 1,
  label: new Date(0, i).toLocaleString("default", { month: "long" }),
}));
