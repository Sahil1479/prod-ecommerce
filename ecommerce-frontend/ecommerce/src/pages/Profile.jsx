import { useSelector, useDispatch } from "react-redux";
import { logout } from "../store/authSlice";
import { Button, Box, Typography } from "@mui/material";

function Profile() {
  const { user } = useSelector((state) => state.auth);
  const dispatch = useDispatch();

  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 5 }}>
      <Typography variant="h5">Profile</Typography>
      {user ? (
        <>
          <Typography>Email: {user.email}</Typography>
          <Typography>Username: {user.username}</Typography>
        </>
      ) : (
        <Typography>No user data</Typography>
      )}
      <Button
        variant="outlined"
        color="secondary"
        fullWidth
        sx={{ mt: 2 }}
        onClick={() => dispatch(logout())}
      >
        Logout
      </Button>
    </Box>
  );
}

export default Profile;
