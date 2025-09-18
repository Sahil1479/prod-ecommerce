import React from "react";
import { Box, Typography } from "@mui/material";

function ErrorPage() {
  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 5 }}>
      <Typography variant="h4" color="error">Something is wrong</Typography>
      <Typography sx={{ mt: 2 }}>An unexpected error occurred. Please try again later.</Typography>
    </Box>
  );
}

export default ErrorPage;
