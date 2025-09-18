import React from "react";
import { Box, Typography } from "@mui/material";

function Unauthorized() {
  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 5 }}>
      <Typography variant="h4" color="error">Unauthorized</Typography>
      <Typography sx={{ mt: 2 }}>You do not have permission to view this page.</Typography>
    </Box>
  );
}

export default Unauthorized;
