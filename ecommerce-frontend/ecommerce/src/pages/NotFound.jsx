import React from "react";
import { Box, Typography } from "@mui/material";

function NotFound() {
  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 5 }}>
      <Typography variant="h4" color="error">404 - Not Found</Typography>
      <Typography sx={{ mt: 2 }}>The page you are looking for does not exist.</Typography>
    </Box>
  );
}

export default NotFound;
