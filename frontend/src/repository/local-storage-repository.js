const STORAGE_KEYS = {
  token: "token",
  user: "user",
  examStore: "exam-store",
};

export const getToken = () => localStorage.getItem(STORAGE_KEYS.token);
export const setToken = (token) => {
  try { localStorage.setItem(STORAGE_KEYS.token, token); }
  catch { console.warn("Failed to save token to localStorage"); }
};
export const removeToken = () => localStorage.removeItem(STORAGE_KEYS.token);

export const getUser = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.user);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};
export const setUser = (user) => {
  try { localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(user)); }
  catch { console.warn("Failed to save user to localStorage"); }
};
export const removeUser = () => localStorage.removeItem(STORAGE_KEYS.user);

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
  } catch { console.warn("Failed to save exam-store to localStorage"); }
};

export const clearAuth = () => {
  removeToken();
  removeUser();
};
