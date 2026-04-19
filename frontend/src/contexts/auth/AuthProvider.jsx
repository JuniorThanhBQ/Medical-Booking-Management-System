import { apis as api, endpoints } from "@configs/apis";
import { BASE_URL } from "@configs/apis";
import axios from "axios";
import { useEffect, useMemo, useReducer, useRef } from "react";
import { toast } from "sonner";

import { AuthContext } from "./AuthContext";
import authReducer, { initialState } from "./authReducer";

let isRefreshing = false;
let failedQueue = [];

const fetchNewToken = async () => {
  const res = await axios.post(
    `${BASE_URL}${endpoints["auth_refresh"]}`,
    {},
    { withCredentials: true,
      xsrfCookieName: 'csrf_token',
      xsrfHeaderName: 'X-CSRFToken'
    },
  );
  return res.data.access_token;
};

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

const handleAuthError = (dispatch, error) => {
  localStorage.removeItem("isAuth");
  dispatch({ type: "AUTH_FAILED" });
  return Promise.reject(error);
};

const setupInterceptors = (dispatch, accessTokenRef) => {
  const requestIntercept = api.interceptors.request.use(
    (config) => {
      if (accessTokenRef.current) {
        config.headers["Authorization"] = `Bearer ${accessTokenRef.current}`;
      }
      return config;
    },
    (error) => Promise.reject(error),
  );

  const responseIntercept = api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error?.config;
      const isAuth = localStorage.getItem("isAuth") === "true";
      if (error?.response?.status !== 401 || !originalRequest || !isAuth) {
        return Promise.reject(error);
      }

      if (!originalRequest._retry) {
        if (isRefreshing) {
          return new Promise(function (resolve, reject) {
            failedQueue.push({ resolve, reject });
          })
            .then((token) => {
              originalRequest.headers["Authorization"] = `Bearer ${token}`;
              return api(originalRequest);
            })
            .catch((err) => {
              return Promise.reject(err);
            });
        }

        originalRequest._retry = true;
        isRefreshing = true;
        try {
          const newAccessToken = await fetchNewToken();
          dispatch({
            type: "REFRESH_TOKEN_SUCCESS",
            payload: { accessToken: newAccessToken },
          });

          processQueue(null, newAccessToken);
          originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;

          return api(originalRequest);
        } catch (err) {
          processQueue(err, null);
          return handleAuthError(dispatch, err);
        } finally {
          isRefreshing = false;
        }
      }
      return Promise.reject(error);
    },
  );

  return { requestIntercept, responseIntercept };
};

const initializeUser = async (dispatch, accessTokenRef) => {
  if (localStorage.getItem("isAuth") !== "true") {
    dispatch({ type: "AUTH_FAILED" });
    return;
  }

  dispatch({ type: "SET_LOADING", payload: true });

  try {
    if (!accessTokenRef.current) {
      const newToken = await fetchNewToken();
      dispatch({
        type: "REFRESH_TOKEN_SUCCESS",
        payload: { accessToken: newToken },
      });

      accessTokenRef.current = newToken;
    }

    const response = await api.get(endpoints["auth_current_user"]);
    dispatch({
      type: "LOGIN_SUCCESS",
      payload: {
        user: response.data.user,
        accessToken: accessTokenRef.current,
      },
    });
  } catch {
    localStorage.removeItem("isAuth");
    dispatch({ type: "AUTH_FAILED" });
  }
};

const createAuthActions = (dispatch) => ({
  login: async (email, password, role) => {
    try {
      const response = await api.post(endpoints["auth_login"], {
        email,
        password,
        role,
      });
      const { access_token, user } = response.data;
      localStorage.setItem("isAuth", "true");
      dispatch({
        type: "LOGIN_SUCCESS",
        payload: { accessToken: access_token, user },
      });
      return { success: true, user };
    } catch (error) {
      if (error.response?.status === 403) {
        const errorMessage = "Tài khoản chưa xác thực hoặc đã bị khoá.";
        toast.error(errorMessage);
        return { success: false, message: errorMessage };
      }

      return {
        success: false,
        message:
          error.response?.data?.message || "Lỗi xảy ra trong luồng đăng nhập.",
      };
    }
  },

  register: async (
    email,
    password,
    firstName,
    lastName,
    phone,
    dateOfBirth,
    gender,
  ) => {
    try {
      const payload = {
        email,
        password,
        firstName,
        lastName,
        phone,
        dayOfBirth: dateOfBirth,
        gender: gender ? gender.toUpperCase() : "",
      };
      const response = await api.post(endpoints["auth_register"], payload);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data?.message || "Email không tồn tại trong thực tế.",
      };
    }
  },

  logout: async () => {
    try {
      await api.post(endpoints["auth_logout"]);
    } catch (error) {
      console.error(error);
    } finally {
      localStorage.removeItem("isAuth");
      dispatch({ type: "LOGOUT" });
    }
  },
});

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const accessTokenRef = useRef(state.accessToken);

  useEffect(() => {
    accessTokenRef.current = state.accessToken;
  }, [state.accessToken]);

  useEffect(() => {
    const { requestIntercept, responseIntercept } = setupInterceptors(
      dispatch,
      accessTokenRef,
    );
    initializeUser(dispatch, accessTokenRef);
    return () => {
      api.interceptors.request.eject(requestIntercept);
      api.interceptors.response.eject(responseIntercept);
    };
  }, []);

  const authActions = useMemo(() => createAuthActions(dispatch), []);

  return (
    <AuthContext.Provider value={{ ...state, ...authActions, api }}>
      {children}
    </AuthContext.Provider>
  );
};
