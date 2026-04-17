const STORAGE_KEYS = {
  token: "token",
  user: "user",
  examStore: "exam-store",
};

export const getExamStore = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.examStore);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

export const setExamStore = (data) => {
  try {
    localStorage.setItem(STORAGE_KEYS.examStore, JSON.stringify(data));
  } catch {
    console.warn("Failed to save exam-store to localStorage");
  }
};
