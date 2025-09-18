import React, { createContext, useReducer, useContext, useEffect } from "react";
import api from "../services/api";

const AuthStateContext = createContext();
const AuthDispatchContext = createContext();

const initialState = {
  user: null,
  access: null,
  refresh: null,
};

function reducer(state, action) {
  switch (action.type) {
    case "LOGIN":
      return {
        ...state,
        user: action.payload.user,
        access: action.payload.access,
        refresh: action.payload.refresh,
      };
    case "LOGOUT":
      return { ...initialState };
    case "SET_USER":
      return { ...state, user: action.payload };
    case "SET_ACCESS":
      return { ...state, access: action.payload };
    default:
      return state;
  }
}

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    // Try to load tokens from localStorage on app start
    const access = localStorage.getItem("access");
    const refresh = localStorage.getItem("refresh");
    const user = localStorage.getItem("user");
    if (access && refresh) {
      dispatch({
        type: "LOGIN",
        payload: { user: user ? JSON.parse(user) : null, access, refresh },
      });
      api.setAuth(access, refresh);
    }
  }, []);

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    api.clearAuth();
    dispatch({ type: "LOGOUT" });
  };

  const value = {
    user: state.user,
    access: state.access,
    refresh: state.refresh,
    dispatch,
    logout,
  };

  return (
    <AuthStateContext.Provider value={value}>
      <AuthDispatchContext.Provider value={dispatch}>
        {children}
      </AuthDispatchContext.Provider>
    </AuthStateContext.Provider>
  );
}

export const useAuth = () => useContext(AuthStateContext);
