import { apis as api, endpoints } from "@configs/apis";
import { useEffect, useMemo, useReducer, useRef } from "react";

import { AuthContext } from "./AuthContext";
import authReducer, { initialState } from "./authReducer";

const fetchNewToken = async () => {
  const res = await api.post(
    endpoints["auth_refresh"],
    {},
    { withCredentials: true },
  );
  return res.data.access_token;
};

const handleAuthError = (dispatch, error) => {
  localStorage.removeItem("isAuth");
  dispatch({ type: "AUTH_FAILED" });
  return Promise.reject(error);
};

const setupInterceptors = (dispatch, accessTokenRef) => {
  const reqIntercept = api.interceptors.request.use(
    (config) => {
      if (accessTokenRef.current) {
        config.headers["Authorization"] = `Bearer ${accessTokenRef.current}`;
      }
      return config;
    },
    (error) => Promise.reject(error),
  );

  const resIntercept = api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const prevRequest = error?.config;
      const isAuth = localStorage.getItem("isAuth") === "true";

      if (
        error?.response?.status !== 401 ||
        !prevRequest ||
        prevRequest.sent ||
        !isAuth
      ) {
        return Promise.reject(error);
      }

      prevRequest.sent = true;
      try {
        const newAccessToken = await fetchNewToken();
        dispatch({
          type: "REFRESH_TOKEN_SUCCESS",
          payload: { accessToken: newAccessToken },
        });
        prevRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(prevRequest);
      } catch (err) {
        return handleAuthError(dispatch, err);
      }
    },
  );

  return { reqIntercept, resIntercept };
};

const initializeUser = async (dispatch, accessTokenRef) => {
  if (localStorage.getItem("isAuth") !== "true") {
    dispatch({ type: "AUTH_FAILED" });
    return;
  }

  dispatch({ type: "SET_LOADING", payload: true });

  let activeToken = accessTokenRef.current;
  if (!activeToken) {
    try {
      activeToken = await fetchNewToken();
      dispatch({
        type: "REFRESH_TOKEN_SUCCESS",
        payload: { accessToken: activeToken },
      });
    } catch {
      localStorage.removeItem("isAuth");
      dispatch({ type: "AUTH_FAILED" });
      return;
    }
  }

  try {
    const headers = activeToken
      ? { Authorization: `Bearer ${activeToken}` }
      : undefined;
    const response = await api.get(endpoints["auth_current_user"], { headers });
    dispatch({
      type: "LOGIN_SUCCESS",
      payload: { user: response.data.user, accessToken: activeToken },
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
      return { success: false, message: error.response?.data?.message };
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
      return { success: false, message: error.response?.data?.message };
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
    const { reqIntercept, resIntercept } = setupInterceptors(
      dispatch,
      accessTokenRef,
    );
    initializeUser(dispatch, accessTokenRef);
    return () => {
      api.interceptors.request.eject(reqIntercept);
      api.interceptors.response.eject(resIntercept);
    };
  }, []);

  const authActions = useMemo(() => createAuthActions(dispatch), []);

  return (
    <AuthContext.Provider value={{ ...state, ...authActions, api }}>
      {children}
    </AuthContext.Provider>
  );
};
