import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// Attach access token from localStorage
API.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem("accessToken") || localStorage.getItem("access");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token expiration and refresh
// API.interceptors.response.use(
//   (response) => {
//     console.log("API response (success):", response);
//     return response;
//   },
//   async (error) => {
//     console.log("API response:", error.response);
//     const status = error?.response?.status;
//     const originalRequest = error.config;
//     if (status >= 200 && status < 300) {
//       return Promise.resolve(error.response);
//     } else if (status === 401) {
//       // Try refresh token if available
//       if (!originalRequest._retry && localStorage.getItem("refresh")) {
//         originalRequest._retry = true;
//         try {
//           console.log("Attempting token refresh");
//           const refreshToken = localStorage.getItem("refresh");
//           const res = await axios.post(
//             "http://127.0.0.1:8000/api/v1/users/token/refresh/",
//             {
//               refresh: refreshToken,
//             }
//           );
//           const { access } = res.data;
//           localStorage.setItem("access", access);
//           // Update Authorization header and retry original request
//           originalRequest.headers["Authorization"] = `Bearer ${access}`;
//           console.log("Token refreshed, retrying original request");
//           return API(originalRequest);
//         } catch (refreshError) {
//           console.error("Refresh token expired, redirecting to login");
//           // Remove both tokens from localStorage
//           localStorage.removeItem("access");
//           localStorage.removeItem("refresh");
//           localStorage.setItem(
//             "sessionError",
//             "Session expired, please log in again."
//           );
//           window.location.href = "/login";
//           return Promise.reject(refreshError);
//         }
//       } else {
//         // No refresh token or already retried, force logout
//         localStorage.removeItem("access");
//         localStorage.removeItem("refresh");
//         localStorage.setItem(
//           "sessionError",
//           "Session expired, please log in again."
//         );
//         window.location.href = "/login";
//         return Promise.reject(error);
//       }
//     } else if (status === 403) {
//       window.location.href = "/unauthorized";
//       return Promise.reject(error);
//     } else if (status === 404) {
//       window.location.href = "/notfound";
//       return Promise.reject(error);
//     } else if (status >= 500 && status < 600) {
//       window.location.href = "/error";
//       return Promise.reject(error);
//     }
//     return Promise.reject(error);
//   }
// );

API.interceptors.response.use(
  (response) => {
    console.log("API response:", response);
    return response;
  },
  (error) => {
    console.error("API response error:", error);
    const status = error.response ? error.response.status : null;

    if (status === 401) {
      // Handle unauthorized access
    } else if (status === 404) {
      // Handle not found errors
    } else {
      // Handle other errors
    }

    return Promise.reject(error);
  }
);

export default API;
