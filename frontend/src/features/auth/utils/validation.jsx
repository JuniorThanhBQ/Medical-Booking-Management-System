export function isValidEmail(value) {
  const v = value.trim();
  if (!v) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
}

export function isValidPassword(value) {
  return value.length >= 6;
}

export function isValidName(value) {
  return value.length >= 2;
}

export function isValidPhone(value) {
  return value.length >= 10;
}

export function isValidDateOfBirth(value) {
  return value.length >= 10;
}

export function isValidGender(value) {
  return value === "male" || value === "female";
}

export function isValidRole(value) {
  return value === "patient" || value === "doctor";
}
