import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import API from "../services/api";
import { login } from "../store/authSlice";
import { Box, TextField, Button, Typography, Alert } from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  useEffect(() => {
    // Check for session expiration message in localStorage or navigation state
    const sessionError = localStorage.getItem("sessionError") || location.state?.error;
    if (sessionError) {
      setError(sessionError);
      localStorage.removeItem("sessionError");
    }
    if (isAuthenticated) {
      navigate("/profile");
    }
  }, [isAuthenticated, navigate, location.state]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post("/users/token/", { username, password });
      const { access, refresh } = res.data;
      dispatch(login({ access, refresh }));
      // navigation will happen automatically via useEffect
    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 5 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Login
      </Typography>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          margin="normal"
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <TextField
          fullWidth
          margin="normal"
          type="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
          Login
        </Button>
      </form>
    </Box>
  );
}

export default Login;
