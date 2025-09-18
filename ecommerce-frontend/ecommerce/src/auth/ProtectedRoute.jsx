// src/auth/ProtectedRoute.jsx
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const [sessionError, setSessionError] = useState(null);

  useEffect(() => {
    const errorMsg = localStorage.getItem("sessionError");
    if (errorMsg) {
      setSessionError(errorMsg);
      localStorage.removeItem("sessionError");
    }
  }, []);

  if (!isAuthenticated) {
    // Pass error message to login page via state
    return <Navigate to="/login" replace state={{ error: sessionError }} />;
  }

  return children;
};

export default ProtectedRoute;
