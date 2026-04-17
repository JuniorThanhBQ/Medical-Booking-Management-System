export const initialState = {
  user: null,
  accessToken: null,
  isAuthenticated: false,
  isLoading: true,
};

const payload_result = {
  LOGIN_SUCCESS: (state, action) => ({
    ...state,
    user: action.payload.user,
    accessToken: action.payload.accessToken,
    isAuthenticated: true,
    isLoading: false,
  }),
  REFRESH_TOKEN_SUCCESS: (state, action) => ({
    ...state,
    accessToken: action.payload.accessToken,
    isAuthenticated: true,
    isLoading: true,
  }),
  AUTH_FAILED: () => ({
    ...initialState,
    isLoading: false,
  }),
  LOGOUT: () => ({
    ...initialState,
    isLoading: false,
  }),
  SET_LOADING: (state, action) => ({
    ...state,
    isLoading: action.payload,
  }),
};

export const authReducer = (state, action) => {
  const reducer = payload_result[action.type];
  return reducer ? reducer(state, action) : state;
};

export default authReducer;
