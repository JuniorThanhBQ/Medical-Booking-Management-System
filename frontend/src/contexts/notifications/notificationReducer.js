export const initialState = {
  notifications: [],
  unreadCount: 0,
  loading: false,
  error: null,
  pagination: {
    page: 1,
    per_page: 10,
    total_pages: 0,
    total_items: 0,
    has_next: false,
    has_prev: false,
  },
};

const actionHandlers = {
  SET_LOADING: (state, action) => ({
    ...state,
    loading: action.payload,
  }),
  SET_NOTIFICATIONS: (state, action) => ({
    ...state,
    notifications: action.payload.items,
    pagination: action.payload.meta,
    unreadCount: action.payload.items.filter((n) => !n.is_read).length,
    loading: false,
    error: null,
  }),
  ADD_NOTIFICATION: (state, action) => ({
    ...state,
    notifications: [action.payload, ...state.notifications],
    unreadCount: state.unreadCount + (action.payload.is_read ? 0 : 1),
  }),
  MARK_AS_READ: (state, action) => ({
    ...state,
    notifications: state.notifications.map((n) =>
      n.id === action.payload ? { ...n, is_read: true } : n,
    ),
    unreadCount: Math.max(0, state.unreadCount - 1),
  }),
  MARK_ALL_AS_READ: (state) => ({
    ...state,
    notifications: state.notifications.map((n) => ({ ...n, is_read: true })),
    unreadCount: 0,
  }),
  DELETE_NOTIFICATION: (state, action) => {
    const remaining = state.notifications.filter(
      (n) => n.id !== action.payload,
    );
    return {
      ...state,
      notifications: remaining,
      unreadCount: remaining.filter((n) => !n.is_read).length,
    };
  },
  SET_ERROR: (state, action) => ({
    ...state,
    error: action.payload,
    loading: false,
  }),
  CLEAR_NOTIFICATIONS: () => initialState,
};

export const notificationReducer = (state, action) => {
  const handler = actionHandlers[action.type];
  return handler ? handler(state, action) : state;
};

export default notificationReducer;
