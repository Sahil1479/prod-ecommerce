import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  access: localStorage.getItem("access") || null,
  refresh: localStorage.getItem("refresh") || null,
  isAuthenticated: !!localStorage.getItem("access"),
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login: (state, action) => {
      console.log("Login action payload:", action.payload);
      const { access, refresh } = action.payload;
      state.access = access;
      state.refresh = refresh;

      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.access = null;
      state.refresh = null;

      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      state.isAuthenticated = false;
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
