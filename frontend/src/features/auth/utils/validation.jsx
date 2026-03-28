const EMAIL_REGEX = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#_\-?])[A-Za-z\d@#_\-?]{9,}$/;
const XSS_REGEX = /<[^>]*>/;
const DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/;

export function containsXss(value) {
  return typeof value === "string" && XSS_REGEX.test(value);
}

export function isValidEmail(value) {
  const v = value.trim();
  if (!v) return false;
  if (containsXss(v)) return false;
  return EMAIL_REGEX.test(v);
}

export function isValidPassword(value) {
  if (!value) return false;
  return PASSWORD_REGEX.test(value);
}

export function getPasswordErrors(value) {
  const errors = [];
  if (!value || value.length < 9) errors.push("Ít nhất 9 ký tự");
  if (!/[a-z]/.test(value)) errors.push("Ít nhất 1 chữ thường");
  if (!/[A-Z]/.test(value)) errors.push("Ít nhất 1 chữ hoa");
  if (!/\d/.test(value)) errors.push("Ít nhất 1 chữ số");
  if (!/[@#_\-?]/.test(value)) errors.push("Ít nhất 1 ký tự đặc biệt (@#_-?)");
  return errors;
}

export function isValidName(value) {
  const v = value.trim();
  if (containsXss(v)) return false;
  return v.length >= 2;
}

export function isValidPhone(value) {
  const v = value.trim();
  if (containsXss(v)) return false;
  return v.length >= 10;
}

export function isValidDateOfBirth(value) {
  if (!DATE_REGEX.test(value)) return false;
  const parsed = new Date(value);
  if (isNaN(parsed.getTime())) return false;
  const now = new Date();
  return parsed < now && parsed.getFullYear() >= now.getFullYear() - 120;
}

export function isValidGender(value) {
  return value === "male" || value === "female" || value === "other";
}

export function isValidRole(value) {
  return value === "patient" || value === "doctor";
}
